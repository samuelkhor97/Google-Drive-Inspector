'''
This is proposed to be the real main.py in the far future
It will do:
- start a local web server (bottle framework)
- load another file that handle web requests
-- that file will call functions from current main.py (propose to be renamed)
Requires: bottle
* read README.md for more instruction *
'''

import bottle
from bottle import route, run, template, static_file
import os

# add template directory
viewpath = os.path.abspath(os.path.join(os.path.dirname(__file__), "../web"))
bottle.TEMPLATE_PATH.insert(0, viewpath)

# DEV:
from main import WIP_request_handler as request_list_all_users


@route("/static/<filepath>")
def css(filepath):
    return static_file(filepath, root=viewpath + "/static/")


@route('/')
def index():
    return template('index', content="Dynamically added content")


@route('/main')
def main():
    return request_list_all_users()


run(host='localhost', port=7878)
