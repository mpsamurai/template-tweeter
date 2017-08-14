# -*- coding: utf-8 -*-

import sys
import datetime
import copy
import tweepy
from jinja2 import Environment, FileSystemLoader


class TemplateTweeter():
    """
    Rapper module of tweepy and Jinja2
        tweepy: http://tweepy.readthedocs.io/en/v3.5.0/index.html
        Jinja2: http://jinja.pocoo.org/docs/dev/
    """

    # log settings
    __log_flg = True
    __log_dir_path = "log"

    # tweepy
    __tweepy = None
    __twitter_str_max = 140
    __twitter_separator_flg = True
    __twitter_shorten_suffix = '…'
    __twitter_exclusion_shorten_list = ['url', 'hash_tag']

    # jinja
    __jinja = None
    __jinja_templates_dir_path = 'templates'
    __jinja_assign_item_list = ['body', 'url', 'hash_tag']


    def __init__(
        self,
        option,
        twitter_options,
        jinja_options
    ):
        """
        Initialization
        :param option:
            log_flg: Output log flg
        :param twitter_options: About Twitter API settings
            consumer_key: API key
            consumer_secret: API secret
            access_token: access token
            access_token_secret: access token secret
            separator_flg: Whether to insert a space between data items when posting
                True: insert / False: not insert
            shorten_suffix: Suffix for posting data shortening twitter
            exclusion_shorten_list: If the post data can not fit within 140 characters, a list of assignment items that will not be abbreviated
        :param jinja_options: About Jinja template engine settings
            template_dir: templates directory path
            assign_item_list: List of items to assign to the template
        """
        try:
            # settings
            if 'log_flg' in option and isinstance(option['log_flg'], bool):
                self.__log_flg = option['log_flg']

            self.log('Error! Not match assign item list.')

            # OAuth Authentication
            auth = tweepy.OAuthHandler(twitter_options['consumer_key'], twitter_options['consumer_secret'])
            auth.set_access_token(twitter_options['access_token'], twitter_options['access_token_secret'])
            # authentication configuration.
            redirect_url = auth.get_authorization_url()

            # settings tweepy
            self.__tweepy = tweepy.API(auth)
            if 'separator_flg' in twitter_options and isinstance(twitter_options['separator_flg'], bool):
                self.__twitter_separator_flg = twitter_options['separator_flg']
            if 'shorten_suffix' in twitter_options and isinstance(twitter_options['shorten_suffix'], str):
                self.__twitter_shorten_suffix = twitter_options['shorten_suffix']
            if 'exclusion_shorten_list' in twitter_options and isinstance(twitter_options['exclusion_shorten_list'], list):
                self.__twitter_exclusion_shorten_list = twitter_options['exclusion_shorten_list']

            # settings jinja
            if 'template_dir' in jinja_options and isinstance(jinja_options['template_dir'], str):
                self.__jinja_templates_dir_path = jinja_options['template_dir']
            self.__jinja = Environment(loader=FileSystemLoader(jinja_options['template_dir'], encoding='utf8'))
            if 'assign_item_list' in jinja_options and isinstance(jinja_options['assign_item_list'], list):
                self.__jinja_assign_item_list = jinja_options['assign_item_list']
        except tweepy.TweepError:
            self.log('Error! Failed OAuth authentication.')


    def log(self, msg):
        """
        Output log
        :param msg:
        :return:
        """
        if self.__log_flg:
            now = datetime.datetime.now()
            f = open(self.__log_dir_path+"/"+now.strftime("%Y%m%d")+".log", 'a')
            f.write("["+now.strftime("%Y/%m/%d %H:%M:%s")+"] "+msg+"\n")
            f.close()


    def post(self, template, data_dict):
        """
        Twitter Post
        :param template: Relative path from 'self.__jinja_templates_dir_path' directory.
        :param data_dict: Template assignment items dict.
        :return: bool
            True: post success / False post failed
        """
        # check assign items num in template
        if self.__checkMatchAssignItemList(data_dict) == False:
            self.log('Error! Not match assign item list.')
            return False
        self.__tweepy.update_status(self.__getTemplateAssignedData(template, data_dict))
        return True


    def __checkMatchAssignItemList(self, data_dict):
        """
        check assign items list key match
        :param data_dict:
        :return:
        """
        cnt = 0
        for key in data_dict:
            if key in self.__jinja_assign_item_list:
                cnt += 1
        if cnt != len(self.__jinja_assign_item_list):
            return False
        return True


    def __getTemplateAssignedData(self, template, data_dict):
        """
        Assign items to template and return data
        :param template: template file path
        :param data_dict: assign items
        :return:
        """
        # formatting data for output
        data_dict = self.__formattingDataDictForOutput(template, data_dict)
        # assign items in template
        tpl = self.__jinja.get_template(template)
        msg = tpl.render(data_dict)
        output_data = msg.encode('utf-8')
        if self.__checkPostLen(output_data) == False:
            # If the number of characters is over, return abbreviated data
            output_data = self.__getShortenData(template, data_dict)
        return output_data


    def __checkPostLen(self, val):
        """
        check post character count
        :param val:
        :return: true: 140 characters or less / false: More than 140 characters
        """
        if self.__twitter_str_max < len(u""+val):
            return False
        return True


    def __formattingDataDictForOutput(self, template, data_dict):
        """
        Formatting data for output
        :param data_dict:
        :return:
        """
        cdata_dict = copy.deepcopy(data_dict)
        i = 1
        for key in cdata_dict:
            # strip value
            cdata_dict[key] = cdata_dict[key].strip()
            # insert separator(space)
            if self.__twitter_separator_flg and i != 1:
                cdata_dict[key] = " " + cdata_dict[key]
            i += 1
        return cdata_dict


    def __getShortenData(self, template, data_dict):
        """
        Return output data with only abbreviated items shortened
        :param template:
        :param data_dict:
        :return:
        """
        # Assign only items not to be abbreviated to the template and obtain the number of characters
        exclusion_shorten_data_dict = copy.deepcopy(data_dict)
        shorten_data_dict = copy.deepcopy(data_dict)
        exclusion_shorten_first_flg = True
        shorten_first_flg = True
        for key in data_dict:
            if key not in self.__twitter_exclusion_shorten_list:
                # Empty assignment items not included in exclusion list
                exclusion_shorten_data_dict[key] = ''
                # Remove half-width space of separator from the beginning of the first item in shorten list
                if shorten_first_flg:
                    shorten_data_dict[key] = shorten_data_dict[key].strip(' ')
                    shorten_first_flg = False
            else:
                # Empty assignment items included in exclusion list
                shorten_data_dict[key] = ''
                # Remove half-width space of separator from the beginning of the first item in exclusion list
                if exclusion_shorten_first_flg:
                    exclusion_shorten_data_dict[key] = exclusion_shorten_data_dict[key].strip(' ')
                    exclusion_shorten_first_flg = False
        output_exclusion_shorten_data = self.__getTemplateAssignedData(template, exclusion_shorten_data_dict)
        output_shorten_data = self.__getTemplateAssignedData(template, shorten_data_dict)
        # Number of characters of exclusion items to shorten
        exclusion_shorten_data_len = len(u"" + output_exclusion_shorten_data)
        # Number of characters of items to shorten
        shorten_data_len = len(u"" + output_shorten_data)
        # The remaining number of characters obtained by subtracting the number of separator and suffix characters from the number of characters of the shortening target item
        allowed_str_num = self.__twitter_str_max - exclusion_shorten_data_len - len(' ') - len(u"" + self.__twitter_shorten_suffix)

        if exclusion_shorten_data_len > self.__twitter_str_max:
            # If the item to be abbreviated is over the number of Twitter post characters, return empty
            return ''
        elif shorten_data_len > allowed_str_num:
            return output_shorten_data[0:allowed_str_num] + ' ' + output_exclusion_shorten_data
        else:
            return output_shorten_data + ' ' + output_exclusion_shorten_data
