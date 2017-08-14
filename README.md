template-tweeter
====

Tweet with tweepy and Jinja2.

## Description
This is a wrapper module that tweets using tweepy and Jinja2.

## Requirement

    $ pip install tweepy
    $ pip install jinja2

## Usage
1. Prepare authentication information (token) to connect to Twitter API.
    - Consumer Key (API Key)
    - Consumer Secret (API Secret)
    - Access Token
    - Access Token Secret

2. Add Twitter information to the setting file.
template-tweeter/template_tweeter/configure.py

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
        "shorten_suffix": "…"
    }

3. run

    from template_tweeter import configure
    from template_tweeter import TemplateTweeter as template_tweeter

    tt = template_tweeter.TemplateTweeter(configure.options, configure.twitter_options, jinja_options)
    result = tt.post('test.html', {
        "body": "test",
        "url": "http://google.com",
        "hash_tag": "#test"
    })


## Install

## Contribution

## Licence

[MIT](https://github.com/tcnksm/tool/blob/master/LICENCE)

## Author

[dsonoda](https://github.com/dsonoda)
