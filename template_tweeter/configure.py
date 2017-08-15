"""
Settings by environment
"""
import os

module_dir = os.path.dirname(os.path.abspath(__file__))

"""
settings
"""
options = {
    # Output log flg
    "log_flg": True,
    # Output log directory path
    "log_dir": module_dir + "/log",
}

"""
twitter & tweepy settings
"""
twitter_options = {
    # API key
    "consumer_key": "CONSUMER_KEY",
    # API secret
    "consumer_secret": "CONSUMER_SECRET",
    # access token
    "access_token": "ACCESS_TOKEN",
    # access token secret
    "access_token_secret": "ACCESS_SECRET",
    # Whether to insert a space between data items when posting
    #   True: insert / False: not insert
    "separator_flg": True,
    # Suffix for posting data shortening twitter
    "shorten_suffix": "..."
}

"""
jinja settings
"""
jinja_options = {
    # use template file
    #   True: use template file in 'template_dir'
    #   False: use only template data ( http://jinja.pocoo.org/docs/2.9/api/#jinja2.Template )
    "template_use": False,
    # templates directory path
    "template_dir": "",
    # List of items to assign to the template
    "assign_item_list": [],
    # If the post data can not fit within 140 characters, a list of assignment items that will not be abbreviated
    "exclusion_shorten_item_list": []
}