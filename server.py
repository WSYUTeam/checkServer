#!/usr/bin/python
#-*-coding:utf-8 -*-

#http://oa.wsyu.edu.cn:8080/edoas2/tip_api.jsp?name=xubin1

import os
import sys
import re
import urllib
from flask import Flask, session, redirect, url_for, escape, request, Response, jsonify
from flask import render_template

app = Flask(__name__)

URL_REG = re.compile(r'(http://[^/\\]+)', re.I)
IMG_REG = re.compile(r'<img[^>]*?src=([\'"])([^\1]*?)\1', re.I)

@app.route('/checkMessage/<username>')
def check(username):
    url = 'http://oa.wsyu.edu.cn:8080/edoas2/tip_api.jsp?name=%s' % username
    return Response(checkMessage(url), mimetype='application/xml')

def checkMessage(url):

    global URL_REG, IMG_REG

    m = URL_REG.match(url)
    if not m:
        print '[Error]Invalid URL: ', url
        return

    html = urllib.urlopen(url).read()
    return html


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
