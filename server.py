"""department Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, jsonify, render_template, request, flash, redirect,
                   session)
from flask_debugtoolbar import DebugToolbarExtension

from model import Employee, connect_to_db

import os

# import employee related models
from model import Employee
from model import Employee_company

# import company related models
from model import Title
from model import Department_title
from model import Department
from model import Company_department
from model import Company
from model import Office_department
from model import Office

from model import connect_to_db, db
import datetime

#*# the "#*#" marks is thanks to: 
# https://www.slideshare.net/ssusercf5d12/ss-40104301
#!/usr/bin/python
# coding: utf-8 to prevent asian characters from breaking using Flask
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# Execute Flask object
app = Flask(__name__)

# when running the environment, the secret key file has to be sourced as well
app.secret_key = os.environ['secret_key']

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template('index.html')


#*# receiving parameter in browser: string
# receive user name value and print
@app.route('/user/<username>')
def show__profile(username):
    return 'User %s' % username


#*# receiving parameter in broweser: integer  
# <int: post_id> enforces integer value input
@app.route('/port/<int:post_id>')
def show_post(post_id):
    return 'Post %d' % post_id


#*# logging
# used for marking on console for developer to print needed info
@app.route('/logging')
def logging_test():
    test = 1
    app.logger.debug('debuggin needed')
    app.logger.warning(str(test) + ' line')
    app.logger.error('error occured')
    return 'end logging'


#*# making session work with Flask2
# must have session key along with the app.secret_key line above
# must import request, session
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        if (request.form['email'] == 'abc@abc.com'
                and request.form['password'] == '1234'):
            session['logged_in'] = True
            session['email'] = request.form['email']
            return redirect('logged')
        else:
            return 'Incorrect login information.'
    else:
        return 'Incorrect method.'


@app.route('/logged')
def logged():
    return render_template('index.html')


#*# Understanding get method 1
# Due to security reasons, get method should not be used for logins
# If get were to be used, the code would be as follows
# @app.route('/get_test', methods=['GET'])
# def get_test():
#     if request.method == 'GET':
#         if (request.args.get('email') == 'abc@abc.com'
#                 and request.args.get('password') == '1234'):
#             return 'Welcome ' + request.args.get('username') + '!'
#         else:
#             return 'Incorrect login information.'
#     else:
#         return 'Incorrect method'


#*# Session log out
# request, redirect, url_for, session are needed to be imported
@app.route('/logout', methods=['POST'])
def logout():
    session['logged_in'] = False
    session.pop('email', None)
    return redirect('/')
 

@app.route('/employee')
def employee_list():
    """Show list of employees."""

    employees = employees.query.all()
    return render_template('employee_list.html', employees=employees)


if __name__ == '__main__':
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    # Run internal server
    app.run(port=5000, host='0.0.0.0')
