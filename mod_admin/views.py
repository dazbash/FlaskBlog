from flask import session
from . import admin

@admin.route('/')
def index():
    return "Hello Fram admin index"

@admin.route('/login/')
def login():
    session['name']='hello'
    # session.clear()
    # print(session.get('name'))
    print(session)
    return "1"