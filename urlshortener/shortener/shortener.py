#!/usr/bin/env python
from uuid import uuid4

from flask import Flask, abort, redirect, render_template, request
from redis.sentinel import Sentinel

app = Flask(__name__)
app.sentinel = Sentinel([('127.0.0.1', 26379)], socket_timeout=0.1)
app.store = app.sentinel.master_for('mymaster', socket_timeout=0.1)


def get_code():
    num = int(uuid4())
    alphabet = ("0123456789abcdefghijklmnopqrstuvwxyz"
                "ABCDEFGHIJKLMNOPQRSTUVWXYZ-_")
    if num == 0:
        return alphabet[0]
    arr = []
    base = len(alphabet)
    while num:
        num, rem = divmod(num, base)
        arr.append(alphabet[rem])
    arr.reverse()
    code = ''.join(arr)
    if app.store.get(code):
        return get_code()
    return code


def store_url(url):
    code = get_code()
    if not app.store.setnx(code, url):
        return store_url(url)
    return code


@app.route("/", methods=['GET', 'POST'])
def index():
    global ID
    if request.method == "POST":
        if 'url' not in request.form:
            abort(400)
        try:
            code = store_url(request.form['url'])
            return render_template("result.html", url=request.url + code)
        except RuntimeError:
            return abort(500)
    return render_template("index.html")


@app.route("/<url>")
def redir(url):
    redirect_url = app.store.get(url)
    if redirect_url:
        return redirect(redirect_url)
    else:
        abort(404)


if __name__ == '__main__':
    app.run(debug=True)
