import sys
sys.path.append('../')

from template_tweeter import configure
from template_tweeter import TemplateTweeter as template_tweeter

tt = template_tweeter.TemplateTweeter(configure.settings, configure.twitter_settings, configure.jinja_settings)

tt.post('post.html', {
    'body':'ddd',
    'url':'http://google.com',
    'hash_tag': '#test',
})
