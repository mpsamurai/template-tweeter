template-tweeter
====
This is a wrapper module that posts to twitter using <a href="http://tweepy.readthedocs.io/en/v3.5.0/index.html" target="_blank">tweepy</a> and <a href="http://jinja.pocoo.org/docs/dev/" target="_blank">Jinja2</a>.  
When using a template engine like jinja 2, it is convenient when you want to assign a different value for each post to a template, and post it as follows.  
  
**<span id="anker1">template (post.html)</span>**
```html:post.html
Hello, Today we will hold an event {{ event_name }}.
Summary: {{ summary }}
url: {{ url }}
{{ hash_tag }}
```

## Install
Install the following tools in Python v3.* environment (like virtualenv).

    $ pip install tweepy
    $ pip install jinja2

## Usage
Prepare authentication information (token) to connect to Twitter API.  
To get API keys go to <a href="https://apps.twitter.com" target="_blank">https://apps.twitter.com</a>  

    Consumer Key (API Key)
    Consumer Secret (API Secret)
    Access Token
    Access Token Secret

Add Twitter information to the setting file(/configure.py).  
```python
twitter_options = {
    # API key
    "consumer_key": "Consumer Key (API Key)",
    # API secret
    "consumer_secret": "Consumer Secret (API Secret)",
    # access token
    "access_token": "Access Token",
    # access token secret
    "access_token_secret": "Access Token Secret",
    # Whether to insert a space between data items when posting
    #   True: insert / False: not insert
    "separator_flg": True,
    # Suffix for posting data shortening twitter
    "shorten_suffix": "..."
}
```

prepare a [template](#anker1).  
  
script run.  
```python
from template_tweeter import configure
from template_tweeter import TemplateTweeter as template_tweeter

tt = template_tweeter.TemplateTweeter(configure.options, configure.twitter_options, jinja_options)
result = tt.post('test.html', {
    "event_name": "event-AAA",
    "summary": "aaaaaaa",
    "url": "http://aaaaa.com?event=aaa"
    "hash_tag": "#eventAAA"
})
```

edit settings file(/configure.py).  

| column | type | about | value |
|:---|:---|:---|:---|
|options.log_flg |bool |Output log flg |True: output log file / False: not output |
|options.log_dir |string |Output log directory absolute path |default: /log |
|twitter_options.separator_flg |bool |Whether to insert a space between data items when posting |True: insert / False: not insert |
|twitter_options.shorten_suffix |string |Ellipsis when the contribution content exceeds 140 characters |default: '...' |
|jinja_options.template_use [*1](#anker2) |bool |Flag to assign value using template file |True: use template file in 'template_dir' / False: use only template data |
|jinja_options.template_dir [*1](#anker2) |string |templates directory absolute path |default: "" |
|jinja_options.assign_item_list [*2](#anker3) |list |List of items to assign to the template |default: [] |
|jinja_options.exclusion_shorten_item_list [*3](#anker4) |list |If the post data can not fit within 140 characters, a list of assignment items that will not be abbreviated |default: [] |

<span id="anker2">*1</span>  
If you specify `jinja_options.template_use = True`, you will get an error unless you specify a path with `jinja_options.template_dir`.  
If you specify `jinja_options.template_use = False`, in the first argument of `TemplateTweeter::post()`, it is necessary to specify an assign character string.
```python
result = tt.post('Hello, Today we will hold an event {{ event_name }}.Summary: {{ summary }}url: {{ url }}{{ hash_tag }}', {
    "event_name": "event-AAA",
    "summary": "aaaaaaa",
    "url": "http://aaaaa.com?event=aaa"
    "hash_tag": "#eventAAA"
})
```
<span id="anker3">*2</span>  
It is necessary to enumerate all the item names to be assigned to the template.  
```
    "assign_item_list": ['event_name', 'summary', 'url', 'hash_tag'],
```
<span id="anker4">*3</span>  
It is necessary to enumerate all excluded items from the abbreviated targets. For example, URL and hash tags that make sense if shortened.  
```
    "exclusion_shorten_item_list": ['url', 'hash_tag'],
```

## Licence
[MIT](https://github.com/tcnksm/tool/blob/master/LICENCE)

## Author
[dsonoda](https://github.com/dsonoda)
