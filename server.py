# -*- coding: utf-8 -*-
# Line one is necessary to have utf-8 recognized
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from jinja2 import StrictUndefined
from flask import (Flask, jsonify, render_template, request, flash, redirect,
                   session)
from flask_debugtoolbar import DebugToolbarExtension

import os
import datetime

# import employee related models
from model import Employee
from model import Employee_company
from model import Company
from model import connect_to_db, db

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
# TODO: query to check if the email is in
@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    db_employees = Employee_company.query.filter_by(office_email=email).all()

    db_employee_id = Employee_company.query.filter_by(office_email=email).first().employee_id
    db_password = Employee_company.query.filter_by(employee_id=db_employee_id).first().password
    db_employee_id = Employee_company.query.filter_by(office_email=email).first().employee_id
    db_password = Employee_company.query.filter_by(employee_id=db_employee_id).first().password

    print email, password, len(db_employees), db_employee_id, db_password, db_employee_id, db_password

    if len(db_employees)>1:
        flash("More than one user for the email found. Contact admin.")
        return redirect("/login")
    elif len(db_employees) == 1:
        db_employee_id = Employee_company.query.filter_by(office_email=email).first().employee_id
        db_password = Employee_company.query.filter_by(employee_id=db_employee_id).first().password
    else:
        flash("No such user")
        return redirect("/login")

    if request.method == 'POST':
        if (str(password) == str(db_password)):
            session['logged_in'] = True
            session['email'] = email
            session['password'] = password
            return redirect('logged')
        else:
            # TODO: change to JQuery
            return 'Incorrect login information.'
    else:
        return 'Incorrect method.'


@app.route('/logged')
def logged():
    return render_template('index.html')


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
