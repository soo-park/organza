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
from model import (Employee, Employee_company, Company, Department,Title,
                   Office, Company_department, Department_title,
                   Office_department, connect_to_db, db)
from employee_query import *
from utilities import *


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


@app.route('/search_employees.json')
def search_employees():
    """Search the query result for the right employees for criteria"""

    # a parameter was saved in DOM, so no need to get par in route
    # request.args brings in the arguments that are passed in by AJAX
    # form result dictionary with key-value-pair items in a list
    # print request.args >>> ImmutableMultiDic([('first-name', u'whatever input')])
    # this code will get what is in the dictionary passed in by AJAX
    kwargs = {}
    for item in request.args:
        if request.args[item]:
            kwargs[item] = request.args[item]
    queried_employees = query_selector(kwargs)

    result = {}

    # iterate through the employees to add them one by one to the map format
    for employee in queried_employees:


        # # To get something from the joined tables, you have to write the names
        # # Below code will bring the name of the first company the person is working
        # print employee.employee_companies[0].companies.company_name
        
        # TODO: iterate through employee_companies to save the company/dep/title of each one
        # Below code will bring all the iter items from the first company and make a dictionary out of it
        # Here the attributes of the employees from each tables are retrieved 
        employees_tables = employee
        employees_attributes = get_map_from_sqlalchemy(employee)

        companies_tables = employee.employee_companies[0].companies
        companies_attributes = get_map_from_sqlalchemy(companies_tables)
        
        departments_tables = companies_tables.company_departments[0].departments
        departments_attributes = get_map_from_sqlalchemy(departments_tables)
        
        titles_tables = employee.employee_companies[0].titles
        titles_attributes = get_map_from_sqlalchemy(titles_tables)

        # if to pass as one dictionary, the following will combine the three dictionaries
        attr_two_added = dict(list(companies_attributes.items()) + list(departments_attributes.items()))
        attr_three_added = dict(list(attr_two_added.items()) + list(titles_attributes.items()))
        attr_all_added =  dict(list(attr_three_added.items()) + list(employees_attributes.items()))

        # now we add the employee dictionary to the result dictionary
        # print attr_all_added, '\n\n\n\n'
        result[employee.employee_id] = attr_all_added


    print result
    return jsonify(result)


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
