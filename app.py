'''aurora -- a simple, rest easy blog

The idea for this software was taken directly from toto:

    https://github.com/cloudhead/toto

I loved the idea of a Git powered blog, but being the Python guy that
I am (now) it didn't seem right to be running something in Ruby. Also,
much harder and slower for me to work with.

Thus: Aurora.

Written by Mark Smith <mark@qq.is>.

'''

import os
import re
import pprint
from flask import Flask, render_template, redirect, Markup
from markdown import markdown
from time import time
from aurora import *

CONFIG = {
    'title':    "Mark's Blog",
    'subtitle': "technical meanderings of Mark 'xb95' Smith",
}

ARTICLE_CACHE_TIMER = None
ARTICLES = None  # Articles object
app = Flask(__name__)


def template(tmpl, **args):
    '''Render a template by name with the given arguments.

    '''
    global CONFIG
    args['config'] = CONFIG
    return render_template(tmpl, **args)


@app.route('/')
def index():
    '''The index page contains the most recent articles.

    '''
    global ARTICLES
    return template('index.html', articles=ARTICLES)


@app.route('/article/<slug>')
def article(slug=None):
    global ARTICLES
    if slug is None:
        return redirect('/')
    if not slug in ARTICLES.by_slug:
        return error_404()
    return template('article.html', article=ARTICLES.by_slug[slug])


@app.errorhandler(404)
def error_404(error=None):
    return template('404.html')


@app.before_request
def refresh_article_list():
    '''Read through the filesystem and find articles.

    '''
    global ARTICLES, ARTICLE_CACHE_TIMER
    if ARTICLE_CACHE_TIMER is not None and time() < ARTICLE_CACHE_TIMER:
        return
    ARTICLE_CACHE_TIMER = time() + 10

    def formatter(content):
        return Markup(markdown(content))

    ARTICLES = Articles('articles', formatter)  # Articles!


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.debug = True
    app.run(host='0.0.0.0', port=port)
