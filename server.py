# -*- coding: utf-8 -*-
# Line one is necessary to have utf-8 recognized
from query import *
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
from model import (Employee, Employee_company, Company, Department,Title,
                   Office, Company_department, Department_title,
                   Office_department, connect_to_db, db)

# Execute Flask object
app = Flask(__name__)

# "source secret.sh" to run flask server prior to "python server.py"
# content of the sercret.sh: export secret_key="<your secret key>"
app.secret_key = os.environ['secret_key']

# undefined variable in Jinja2, not fails silently but raises an error
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template('index.html')


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
# have session key along with the app.secret_key line above, import request, session
@app.route('/login', methods=['POST'])
def login():
    """Login user to the user specific information."""

    email = request.form.get('email')
    password = request.form.get('password')
    db_employees = Employee_company.query.filter_by(office_email=email).all()

    if len(db_employees)>1:
        # TODO: deal with duplicate email issue
        flash("More than one user for the email found. Contact admin.")
        return redirect("/")
    elif len(db_employees) == 1:
        db_employee_id = db_employees[0].employee_id
        db_password = Employee_company.query.filter_by(employee_id=db_employee_id).first().password

        # TODO: change into AJAX for all pages to be able have login without redirect
        if (str(password) == str(db_password)):
            session['logged_in'] = True
            session['email'] = email
            session['password'] = password
            return redirect('/logged')
        else:
            flash('Password incorrect.')
            return redirect('/')
    else:
        flash("Email and/or password incorrect.")
        return redirect("/") 


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
 

@app.route('/employees')
def list_employees():
    """Show list of employees."""

    employees = Employee.query.all()
    return render_template('employee_list.html', employees=employees)


#*# receiving parameter in broweser: default <post_info> will be string  
# <int: post_id> enforces integer value input to be an integer
@app.route('/employee/<employee_id>')
def show_employee(employee_id):
    """Show an individual emp"""

    employee_info = Employee.query.filter_by(employee_id=employee_id).first()
    employee_company_info = Employee_company.query.filter_by(employee_id=employee_id).first()

    return render_template('employee_info.html', employee_info=employee_info,
                                                 employee_company_info=employee_company_info)


# a parameter was saved in DOM, so no need to get par in route
@app.route('/search_employees.json')
def search_employees():
    """Search the query result for the right employees for criteria"""

    # request.args brings in the arguments that are passed in by AJAX
    # form result dictionary with key-value-pair items in a list
    # print request.args >>> ImmutableMultiDic([('first-name', u'whatever input')])
    # this code will get what is in the dictionary passed in by AJAX
    kwargs = {}

    for item in request.args:
        if request.args[item]:
            kwargs[item] = request.args[item]

    # depends on the argument received, the dictionary length will differ
    # because there are multiple tables to join to do query AND
    # the table name has to be combined into the query name OUTSIDE the HTML
    # ('Company.company_name' is not accepted as an argument of kwargs)
    # used funamental theorem of arithmetic to assign different cases to cases
    rank = 1

    if "company_name" in kwargs.keys():
        rank*=2
    if "department_name" in kwargs.keys():
        rank*=3
    if "first_name" in kwargs.keys():
        rank*=5
    if "last_name" in kwargs.keys():
        rank*=7

    queries= {
             1 : search_no_criteria,
             2 : search_by_company_name,
             3 : search_by_department_name,
             5 : search_by_first_name,
             7 : search_by_last_name,
             6 : search_by_company_name_department_name,
             10 : search_by_company_name_first_name,
             14 : search_by_company_name_last_name,
             15 : search_by_department_name_first_name,
             21 : search_by_department_name_last_name,
             35 : search_by_first_name_last_name,
             30 : search_by_company_name_department_name_first_name,
             42 : search_by_company_name_department_name_last_name,
             70 : search_by_company_name_first_name_last_name,
             105 : search_by_department_name_first_name_last_name,
             210 : search_by_all_four
             }

    employee_queried = queries[rank](**kwargs)
    employees = {}

    for employee in employee_queried:
        employees[employee] = {''}
        # I know I can iterate and make dic of data
        # but is there a way to pass the object, so that the
        # necessary calculation is done when needed?

        # also, how to "limit data" in login feature
        # substitute with AJAX? or route to a compeletely dif page?
        

    return jsonify(employees)
    # # to display the employees wanted send the result to HTML
    # # and wipe up / replace the div of DOM there using AJAX callback function


@app.route('/employee_excel_loading', methods=['GET'])
def employee_excel_loading():
    """"""

    return render_template('employee_excel.html')


@app.route('/employee_excel', methods=['POST'])
def employee_excel():
    """"""

    # the file object is in python space to be used
    file = request.files['emp_xls']
    print file
    return ""


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
