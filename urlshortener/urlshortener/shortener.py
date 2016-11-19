#!/usr/bin/env python

from flask import Flask, render_template, request, abort, redirect, url_for
from redis.sentinel import Sentinel
app = Flask(__name__)
app.sentinel = Sentinel([('192.168.100.9', 26379)], socket_timeout=0.1)
app.store = app.sentinel.master_for('mymaster', socket_timeout=0.1)

ID = 0

def encode(num):
    alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if num == 0:
        return alphabet[0]
    arr = []
    base = len(alphabet)
    while num:
        num, rem = divmod(num, base)
        arr.append(alphabet[rem])
    arr.reverse()
    return ''.join(arr)

@app.route("/", methods=['GET', 'POST'])
def index():
    global ID
    if request.method == "POST":
        if 'url' not in request.form:
            abort(400)
        code = encode(ID)
        ID += 1
        app.store.set(code, request.form['url'])
        return render_template("result.html", url=request.url + code)
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
