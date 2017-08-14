# -*- coding: utf-8 -*-

"""
module basic settings
"""
settings = {
    # Output log flg: True: output / False: not output
    'log_flg': True,
}

"""
twitter & tweepy settings
"""
twitter_settings = {
    # API key
    'consumer_key': "",
    # API secret
    'consumer_secret': "",
    # access token
    'access_token': "",
    # access token secret
    'access_token_secret': "",
    # Whether to insert a space between data items when posting
    #   True: insert / False: not insert
    'separator_flg': True,
    # Suffix for posting data shortening twitter
    'shorten_suffix': '…',
    # If the post data can not fit within 140 characters, a list of assignment items that will not be abbreviated
    'exclusion_shorten_list': ['url', 'hash_tag'],
}

"""
jinja settings
"""
jinja_settings = {
    # templates directory path
    'template_dir': 'templates',
    # List of items to assign to the template
    'assign_item_list': ['body', 'url', 'hash_tag']
}