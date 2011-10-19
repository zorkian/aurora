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
from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
