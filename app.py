'''aurora -- a simple, rest easy blog

The idea for this software was taken directly from toto:

    https://github.com/cloudhead/toto

I loved the idea of a Git powered blog, but being the Python guy that I am
it didn't seem right to be running something in Ruby.  Also, much harder
and slower for me to work with.

Thus: Aurora.

Written by Mark Smith <mark@qq.is>.

'''

import os
import re
import pprint
from flask import Flask, render_template, redirect
from markdown import markdown
from time import time


ARCHIVE = {}  # Yr -> Mo -> [ list of articles ]
ARTICLE_CACHE_TIMER = None
ARTICLES = {}  # slug => filename
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/article/<slug>')
def article(slug=None):
    global ARTICLES
    if slug is None:
        return redirect('/')
    if not slug in ARTICLES:
        return error_404()

    with open(ARTICLES[slug], 'r') as f:
        md = markdown(f.read())
    return render_template('article.html', article=md)


def error_404():
    '''Return a 404 page.

    '''
    return render_template('404.html')


@app.before_request
def refresh_article_list():
    '''Read through the filesystem and find articles.

    '''
    global ARTICLES, ARTICLE_CACHE_TIMER, ARCHIVE
    if ARTICLE_CACHE_TIMER is not None and time() < ARTICLE_CACHE_TIMER:
        return
    ARTICLE_CACHE_TIMER = time() + 10

    if not os.path.isdir('articles'):
        return
    for fn in os.listdir('articles'):
        ffn = os.path.join('articles', fn)
        if not os.path.isfile(ffn):
            continue
        match = re.match(r'^(\d\d\d\d)-(\d\d)-(\d\d)-(.+)\.md$', fn)
        if match is None:
            continue
        yr, mo, da, slug = match.groups()
        ARTICLES[slug] = ffn

        if not yr in ARCHIVE:
            ARCHIVE[yr] = {}
        if not mo in ARCHIVE[yr]:
            ARCHIVE[yr][mo] = []
        ARCHIVE[yr][mo].append(ffn)
        ARCHIVE[yr][mo].sort()
        ARCHIVE[yr][mo].reverse()


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
