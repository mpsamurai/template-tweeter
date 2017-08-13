import tweepy
from jinja2 import Environment, FileSystemLoader

class TemplateTweeter():
    """
    tweepy, Jinja のラッパークラス
        tweepy: http://tweepy.readthedocs.io/en/v3.5.0/index.html
        Jinja: http://jinja.pocoo.org/docs/dev/
    """

    # tweepy object
    __tweepy = None
    # jinja object
    __jinja = None

    # twitter投稿文字制限数
    __twitter_str_max = 140

    def __init__(
        self,
        twitter_options,
        jinja_options
    ):
        """
        初期化
        :param twitter_options: Twitter API設定項目
            consumer_key: API key
            consumer_secret: API secret
            access_token: access token
            access_token_secret: access token secret
        :param jinja_options: Jijja 設定項目
            dir: テンプレートディレクトリパス
        """
        try:
            # OAuth Authentication
            auth = tweepy.OAuthHandler(twitter_options['consumer_key'], twitter_options['consumer_secret'])
            auth.set_access_token(twitter_options['access_token'], twitter_options['access_token_secret'])
            # authentication configuration
            redirect_url = auth.get_authorization_url()
            self.__tweepy = tweepy.API(auth)
            self.__jinja = Environment(loader=FileSystemLoader(jinja_options['dir'], encoding='utf8'))
        except tweepy.TweepError:
            print('Error! Failed OAuth authentication.')

    def tweet(self, template_path, data_dict):
        """
        ツイート
        :param template_path: テンプレートディレクトリからの相対パス
        :param data_dict: アサイン項目値
        :return:
        """
        tpl = self.__jinja.get_template(template_path)
        msg = tpl.render(data_dict)
        self.__tweepy.update_status(msg.encode('utf-8'))

    def checkStringLen(self, val):
        """
        ツイート文字数チェック
        :param val:
        :return: false:140字よりも多い / true:140字以下
        """
        if self.__twitter_str_max < len(u""+val):
            return false
        return true
