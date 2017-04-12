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
from utilities import get_map_from_sqlalchemy, value_is_same_as_db



# Execute Flask object
app = Flask(__name__)

# "source secret.sh" to run flask server prior to "python server.py"
# content of the sercret.sh: export secret_key="<your secret key>"
app.secret_key = os.environ['secret_key']

# undefined variable in Jinja2, not fails silently but raises an error
app.jinja_env.undefined = StrictUndefined


### TODO: Use regx to enforce formatting
@app.route('/')
def index():
    """Homepage."""

    # return render_template('index.html')
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
# TODO: when browser has session cache, when browser restarts
# the button shows as user logged in, the page is default
# find a way to match the two
@app.route('/login', methods=['POST'])
def login():
    """Login user to the user specific information."""

    email = request.form.get('email')
    password = request.form.get('password')
    db_employees = query_selector({'email': email})

    if len(db_employees) > 1:
        flash("More than one user for the email found. Contact admin.")
        return redirect("/")
    elif len(db_employees) == 1:
        db_employee = db_employees[0]
        db_employee_id = db_employee.employee_id
        db_employee_company_info = db_employee.employee_companies[0]
        db_password = db_employee_company_info.password

        if (str(password) == str(db_password)):
            session['logged_in'] = True
            session['email'] = email
            session['password'] = password

            date_employeed = db_employee_company_info.date_employeed
            date_departed = db_employee_company_info.date_departed
            # TODO: When an employee departure date is added, check if admin
            #       if admin, ask if want to delete the admin status
            if db_employee.admin == True:
                return redirect('/admin_logged')

            if date_employeed and not date_departed:
                return redirect("/employee_logged")
            elif date_employeed and date_departed:
                flash('No date employeed found. Please contact the admin for more information.')
                return redirect("/logged")
            else:
                return redirect('/logged')
        else:
            flash('Password incorrect.')
            return redirect('/')
    else:
        flash("Email and/or password incorrect.")
    return redirect("/") 


@app.route('/logged')
def logged():
    """Login as a regular user"""

    return render_template('index.html') # (date_employeed and date_departed)


@app.route('/admin_logged')
def admin_logged():
    """Login as an admin"""

    return render_template('admin_index.html')
    

@app.route('/employee_logged')
def employee_logged():
    """Login as an employee"""

    return render_template('employee_index.html')


#*# Session log out
# TODO: Find a way to delete the login info when the window is closed
# request, redirect, url_for, session are needed to be imported
@app.route('/logout', methods=['POST'])
def logout():
    session['logged_in'] = False
    session.pop('email', None)
    return redirect('/')
 

@app.route('/employee/all')
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
        
        # Below code will bring all the iter items from the first company and make a dictionary out of it
        # Here the attributes of the employees from each tables are retrieved 
        employees_tables = employee
        employees_attributes = get_map_from_sqlalchemy(employee)

        # TODO: make it possible for the employee info to contain
        # all companies the person is working for by iterating 0
        companies_tables = employee.employee_companies[0].companies
        companies_attributes = get_map_from_sqlalchemy(companies_tables)
        
        departments_tables = companies_tables.company_departments[0].departments
        departments_attributes = get_map_from_sqlalchemy(departments_tables)
        
        titles_tables = employee.employee_companies[0].titles
        titles_attributes = get_map_from_sqlalchemy(titles_tables)

        # if to pass as one dictionary, the following will combine the for dictionaries
        # TODO: make lists of things to be combined, and for loop them
        attr_two_added = dict(list(companies_attributes.items()) + list(departments_attributes.items()))
        attr_three_added = dict(list(attr_two_added.items()) + list(titles_attributes.items()))
        attr_all_added =  dict(list(attr_three_added.items()) + list(employees_attributes.items()))

        # now we add the employee dictionary to the result dictionary
        # print attr_all_added, '\n\n\n\n'
        result[employee.employee_id] = attr_all_added

    print result
    return jsonify(result)


@app.route('/employee/add')
def add_employee_page():
    """Load add_employee page db."""

    # TODO: make the query name specific, and make the list sorted 
    companies = Company.query.all()
    departments = Department.query.all()
    titles = Title.query.all()
    offices = Office.query.all()

    return render_template('employee_add.html', companies=companies,
                                                departments=departments,
                                                titles=titles,
                                                offices=offices)


# TODO: In homepage, add sign-up page that uses this + session[email] to 
# generate new user AND log into session right away
# TODO: separate generate new person page into two, and have "User"
# Thant has nothing to do with the deep details into company - have this form as sign-up
@app.route('/add_employee', methods=['POST'])
def add_employee():
    """Add employee to the db."""

    # Unicode/datetime does not accept empty string. When user do not input 
    # anyting, an empty string becomes the value. Thus, iterate to assign None. 
    # Exception: checkbox will not be submitted if off. Thus, receive value directly
    all_input = request.form.items()
    result = {}
    for key, value in all_input:
        if value == '':
            result[key] = None
        else:
            result[key] = value

    # TODO: change the admin to status, and have drop down menu that has admin, employee, other
    # TODO: add web_id --> change across model + login + seed + form
    # TODO: change the hardcode below to have dynamic variables -- request.form.get('admin')
    new_employee = Employee(
                            birthday= result['birthday'],
                            personal_email= result['personal_email'],
                            first_name= result['first_name'],
                            mid_name= result['mid_name'],
                            last_name= result['last_name'],
                            nickname= result['nickname'],
                            k_name= result['k_name'],
                            kanji_name= result['kanji_name'],
                            phone= result['phone'],
                            mobile= result['mobile'],
                            address_line1= result['address_line1'],
                            address_line2= result['address_line2'],
                            city= result['city'],
                            state= result['state'],
                            country= result['country'],
                            postal_code= result['postal_code'],
                            emergency_name= result['emergency_name'],
                            emergency_phone= result['emergency_phone'],
                            admin= result['admin']
                            )

    company_name = result['company_name']
    if company_name != None:
        query_companies = db.session.query(Company.company_name).all()
        company_names = { company.company_name for company in query_companies}
        if company_name in company_names:
            # print db.session.query(func.max(employee_company))
            print company_name
        else:
            # new id company is generated with this particular company name
            # new id in employee_company adds with this new company and the employee
            print company_name, company_names


    # if result['department_name'] != None:
    #     if department_name exists:
    #         # new id in employee_company adds with this employee number to that company id number

    #     else: 
    #         # new id company is generated with this particular company name
            # new id in employee_company adds with this new company and the employee

    #                         department_name= request.form.get('department_name'),
    #                         title= request.form.get('title'),
    #                         office_name= request.form.get('office_name'),
    #                         office_email= request.form.get('office_email'),
    #                         password= request.form.get('password'),
    #                         date_employeed= request.form.get('date_employeed'),
    #                         date_departed= request.form.get('date_departed'),
    #                         job_description= request.form.get('job_description'),
    #                         office_phone= request.form.get('office_phone'),
    #                         title_id= request.form.get('title_id'),
    #                         department_id= request.form.get('department_id'),
    #                         office_id= request.form.get('office_id'),
    #                         department_id= request.form.get('department_id')
    #                         )

    # add user id by query

    # add employee to db
    db.session.add(new_employee)
    db.session.commit()

    # iterate through the employees to add them one by one to the map format
    # print result
    # flash(u"User %s %s added."%(first_name, last_name), 'error')
    return redirect("/employee/add")


@app.route('/employee_excel_loading', methods=['GET'])
def employee_excel_loading():
    """Load Excel file and save"""

    return render_template('employee_excel.html')


@app.route('/employee_excel', methods=['POST'])
def employee_excel():
    """Process the Excel data into DB"""

    # the file object is in python space to be used
    file = request.files['emp_xls']
    print file
    return ""


@app.route('/company/all')
def list_companies():
    """Show organizational structure."""

    companies = Company.query.all()
    return render_template('org_chart.html', companies=companies)


@app.route('/map')
def map():
    """Show organizational structure."""

    # # Practice: Using global varialbe 
    # # Google Map key secret. import os is used with this code.
    # # Also, in terminal, use the following command to make sure you have the key 
    # # source <the file that contanins GOOGLE_MAP_KEY variable>
    # api_key = os.environ['GOOGLE_MAP_KEY']
    # # Passing secret key to the html
    # return render_template('map.html', api_key=api_key)

    return render_template('map.html')


@app.route('/analysis')
def analysis():
    """Show organizational structure."""

    return render_template('analysis.html')


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
