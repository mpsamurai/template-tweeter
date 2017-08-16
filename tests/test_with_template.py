import sys
sys.path.append('../')

import os
module_dir = os.path.dirname(os.path.abspath(__file__))

from template_tweeter import configure
from template_tweeter import TemplateTweeter as template_tweeter


jinja_options = {
    "template_use": True,
    "template_dir": module_dir + "/templates",
    "assign_item_list": ["body", "url", "hash_tag"],
    "exclusion_shorten_item_list": ["url", "hash_tag"]
}
tt = template_tweeter.TemplateTweeter(configure.options, configure.twitter_options, jinja_options)
result = tt.post('test.html', {
    "body": "うあああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああabcdefghijklmnopqrstu",
    "url": "http://google.com",
    "hash_tag": "#test"
})
print(result)


jinja_options = {
    "template_use": True,
    "template_dir": module_dir + "/templates",
    "assign_item_list": ["body", "url", "hash_tag"],
    "exclusion_shorten_item_list": ["hash_tag"]
}
tt = template_tweeter.TemplateTweeter(configure.options, configure.twitter_options, jinja_options)
result = tt.post('test.html', {
    "body": "うああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああabcdefghijklmnopqrstu",
    "url": "http://google.com",
    "hash_tag": "#test"
})
print(result)


jinja_options = {
    "template_use": True,
    "template_dir": module_dir + "/templates",
    "assign_item_list": ["body", "url", "hash_tag"],
    "exclusion_shorten_item_list": ["hash_tag"]
}
tt = template_tweeter.TemplateTweeter(configure.options, configure.twitter_options, jinja_options)
result = tt.post('test2.html', {
    "body": "aaaa",
    "url": "http://google.com",
    "hash_tag": "#test"
})
print(result)
