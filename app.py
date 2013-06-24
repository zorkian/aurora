#!/usr/bin/python
'''aurora -- a simple, rest easy blog

The idea for this software was taken directly from toto:

    https://github.com/cloudhead/toto

I loved the idea of a Git powered blog, but being the Python guy that
I am (now) it didn't seem right to be running something in Ruby. Also,
much harder and slower for me to work with.

Thus: Aurora.

Written by Mark Smith <mark@qq.is>.

'''

import datetime
import os
import re
import pprint
import PyRSS2Gen as RSS2
from flask import Flask, render_template, redirect, Markup, make_response, escape, request
from markdown import markdown
from time import time
from aurora import *

CONFIG = {
    'url':      "http://qq.is",
    'title':    "Mark's Blog",
    'subtitle': "technical meanderings of Mark 'xb95' Smith",
    'description': "Technical ramblings somewhere between development and operations.",
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


@app.route('/articles.xml')
def xml_index(slug=None):
    global ARTICLES, CONFIG
    items = []
    for article in ARTICLES.by_recent[-10:]:
        items.append(RSS2.RSSItem(
             title = article.title,
             link = "%s/article/%s" % (CONFIG['url'], article.slug),
             description = markdown(article.raw_content),
             guid = RSS2.Guid("%s/article/%s" % (CONFIG['url'], article.slug)),
             pubDate = datetime.datetime.strptime('%s %s' % (article.date, article.time), '%Y-%m-%d %H:%M')))
    items.reverse()

    rss = RSS2.RSS2(
        title = CONFIG['title'],
        link = CONFIG['url'],
        description = CONFIG['description'],
        lastBuildDate = datetime.datetime.utcnow(),
        items = items)

    response = make_response(rss.to_xml(encoding='utf-8'))
    response.headers['Content-Type'] = 'text/xml; charset=utf-8'
    return response


@app.errorhandler(404)
def error_404(error=None):
    return template('404.html'), 404


@app.before_request
def refresh_article_list():
    '''Read through the filesystem and find articles.

    '''
    global ARTICLES, ARTICLE_CACHE_TIMER
    try:
        app.logger.debug('-> %s' % request.headers['Referer'])
    except:
        pass

    if ARTICLE_CACHE_TIMER is not None and time() < ARTICLE_CACHE_TIMER:
        return
    ARTICLE_CACHE_TIMER = time() + 10

    def formatter(content):
        return Markup(markdown(content))

    ARTICLES = Articles('/home/mark/code/aurora/articles', formatter)  # Articles!


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.debug = True
    app.run(host='0.0.0.0', port=port)
