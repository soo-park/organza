# -*- coding: utf-8 -*-
# Line one is necessary to have utf-8 recognized
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import os
import datetime

# Execute Flask object
from flask import (Flask, jsonify, render_template, request, flash, redirect,
                   session, url_for, send_from_directory)
from flask_debugtoolbar import DebugToolbarExtension
app = Flask(__name__)

# for SQLAlchemy to load only certain columns
from sqlalchemy.orm import Load, load_only

# for file upload
from werkzeug.utils import secure_filename 
UPLOAD_FOLDER = 'static/img'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # limits upload to 16mb

# import employee related models
from model import (Employee, Employee_company, Company, Department,Title,
                   Office, Company_department, Department_title,
                   Office_department, connect_to_db, db)
from employee_query import *
from utilities import (get_map_from_sqlalchemy, change_sql_obj_into_dic, 
                        change_sql_sub_obj_into_dic, merge_dicts)

# "source secret.sh" to run flask server prior to "python server.py"
# content of the sercret.sh: export secret_key="<your secret key>"
app.secret_key = os.environ['secret_key']

# undefined variable in Jinja2, not fails silently but raises an error
from jinja2 import StrictUndefined
app.jinja_env.undefined = StrictUndefined


##################### END IMPORTS START HOME FEATURE ###########################


@app.route('/')
def index():
    """Homepage."""

    # return render_template('index.html')
    return render_template('index.html')


#################### END HOME START OF LOGIN FEATURE ###########################


#*# making session work with Flask2
# have session key along with the app.secret_key line above, import request, session
# TODO: when browser has session cache, when browser restarts
# the button shows as user logged in, the page is default
# find a way to match the two
# TODO: load a script that makes all pages load by checking admin/employee or not

@app.route('/login', methods=['POST'])
def login():
    """Login user to the user specific information."""

    username = request.form.get('username')
    password = request.form.get('password')
    db_employees = Employee.query.filter_by(username=username).all()
    print db_employees
    if len(db_employees) > 1:
        flash("More than one user for the email found. Contact admin.")
        return redirect("/")
    elif len(db_employees) == 1:
        db_employee = db_employees[0]
        db_employee_id = db_employee.employee_id
        db_password = db_employee.password
        db_employee_company_info = Employee_company.query.filter_by(employee_id=db_employee_id).all()[0]

        if (str(password) == str(db_password)):
            session['logged_in'] = True
            session['username'] = username
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

    return render_template('home/general.html') # (date_employeed and date_departed)


@app.route('/employee_logged')
def employee_logged():
    """Login as an employee"""

    return render_template('home/employee.html')


@app.route('/admin_logged')
def admin_logged():
    """Login as an admin"""

    return render_template('home/admin.html')
    

#*# Session log out
# TODO: Find a way to delete the login info when the window is closed
# request, redirect, url_for, session are needed to be imported
@app.route('/logout', methods=['POST'])
def logout():
    session['logged_in'] = False
    session.pop('username', None)
    return redirect('/')
 

################# END LOGIN START EMPLOYEE SEARCH FEATURE ######################

@app.route('/employee/data/<int:offset>/<int:limit>')
def limit_list(offset, limit):
    """limits the amount of employees loaded up on HTML"""

    employees = Employee.query.options(
                            Load(Employee)
                            .load_only(Employee.first_name,
                                       Employee.last_name,
                                       Employee.employee_id)
                            ).offset(offset).limit(limit).all()

    print({'employees':[{'first_name': employee.first_name, 'last_name': employee.last_name, 'employee_id': employee.employee_id} for employee in employees]})
    return jsonify({'employees':[{'first_name': employee.first_name, 'last_name': employee.last_name, 'employee_id': employee.employee_id} for employee in employees]}), 200


@app.route('/employee/all')
def list_employees():
    """Show list of employees."""

    employees = Employee.query.options(
                            Load(Employee)
                            .load_only(Employee.first_name,
                                       Employee.last_name,
                                       Employee.employee_id)
                            ).all()

    companies = (Company.query.options(
                            Load(Company)
                            .load_only(Company.company_id, Company.company_name)
                            )
                         .all()
                        )
    departments = (Department.query.options(
                        Load(Department)
                        .load_only(Department.department_id, Department.department_name)
                        )
                     .all()
                    )

    return render_template('employee/list.html', employees=employees[:9],
                                                 employees_length=len(employees),
                                                 companies=companies,
                                                 departments=departments
                                                 )


@app.route('/search_employees.json')
def search_employees():
    """Search the query result for the right employees for criteria"""

    # Get search input and make a dictionary out of it
    criteria = {}
    for key, value in request.args.iteritems():
        if value != '':
            criteria[key]=value
        else:
            pass
    print criteria

    # Lazy load employees
    query_employees = (Employee.query.options(Load(Employee)
                            .load_only(Employee.employee_id,
                                       Employee.first_name,
                                       Employee.last_name)
                            )
                        )

    # Lazy add filters if the condision exists
    # TODO: currently search is case sensitive. Make it not so
    if 'first_name' in criteria:
        query_employees = query_employees.filter_by(first_name=criteria['first_name'])

    if 'last_name' in criteria:
        query_employees = query_employees.filter_by(last_name=criteria['last_name'])

    if 'company_name' in criteria:
        query_employees = (query_employees.outerjoin(Employee_company)
                                        .outerjoin(Company)
                                        .filter_by(company_name=criteria['company_name'])
                            )
    if 'department_name' in criteria:
        query_employees = (query_employees.outerjoin(Company_department)
                                        .outerjoin(Department)
                                        .filter_by(department_name=criteria['department_name'])
                            )

    # Do the actual query by calling the query into the python space
    query_employees = query_employees.all()

    # Get the employee first/last names of the search result
    result = {}

    if query_employees:
        for i in range(0, len(query_employees)):
            result[query_employees[i].employee_id] = { 
                'first_name': query_employees[i].__dict__['first_name'].lower(),
                'last_name': query_employees[i].__dict__['last_name'].lower() 
            }

    # Make JSON of the employee list to send back to static/js/employee_list.js
    return jsonify(result)


#*# receiving parameter in broweser: default <post_info> will be string  
# <int: post_id> enforces integer value input to be an integer
@app.route('/employee/<employee_id>')
def show_employee(employee_id):
    """Show an individual emp"""

    # query all table data related to the employee
    employee = (db.session.query(Employee, Employee_company, Company, Department, Title)
                          .filter(Employee.employee_id==employee_id)
                          .outerjoin(Employee_company)
                          .outerjoin(Company)
                          .outerjoin(Company_department)
                          .outerjoin(Department)
                          .outerjoin(Department_title)
                          .outerjoin(Title)
                          .first())

    # load the content of each table
    employee_result = change_sql_obj_into_dic(employee)
    company = change_sql_sub_obj_into_dic(employee.Company)
    employee_company = change_sql_sub_obj_into_dic(employee.Employee_company)
    department = change_sql_sub_obj_into_dic(employee.Department)
    company = change_sql_sub_obj_into_dic(employee.Company)
    title = change_sql_sub_obj_into_dic(employee.Title)
    
    # merge the contents into one dictionary
    employee_info = merge_dicts(employee_result, employee_company, company, department, title)

    # pass the dictionary to HTML
    return render_template('employee/info.html', employee_info=employee_info)


######### END EMPLOYEE SEARCH FEATURE START ADD EMPLOYEE FEATURE ###############


@app.route('/employee/add')
def add_employee_page():
    """Load add_employee page db."""

    # TODO: make the query name specific, and make the list sorted 
    companies = Company.query.all()
    departments = Department.query.all()
    titles = Title.query.all()
    offices = Office.query.all()

    # pass the query values to HTML
    return render_template('employee/add.html', companies=companies,
                                                departments=departments,
                                                titles=titles,
                                                offices=offices)


# http://flask.pocoo.org/docs/0.12/patterns/fileuploads/
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# TODO: In homepage, add sign-up page that uses this + session[username] to 
# generate new user AND log into session right away
# TODO: separate generate new person page into two, and have "User"
# that has nothing to do with the deep details into company - have this form as sign-up
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

    if result['username']==None or result['password']==None or result['first_name']==None:
        session.pop('_flashes', None)
        flash ("Please input all required fields.")
        return redirect('/employee/add')

    # TODO: change the admin to status, and have drop down menu that has admin, employee, other
    new_employee = Employee(
                            birthday= result['birthday'],
                            personal_email= result['personal_email'],
                            first_name= result['first_name'],
                            mid_name= result['mid_name'],
                            last_name= result['last_name'],
                            username= result['username'],
                            password= result['username'],
                            k_name= result['k_name'],
                            kanji_name= result['kanji_name'],
                            phone= result['phone'],
                            mobile= result['mobile'],
                            address= result['address'],
                            country_code= result['country_code'],
                            city= result['city'],
                            state= result['state'],
                            country= result['country'],
                            postal_code= result['postal_code'],
                            emergency_name= result['emergency_name'],
                            emergency_phone= result['emergency_phone'],
                            admin= request.form.get('admin')
                            )
    # add employee to db
    db.session.add(new_employee)
    db.session.commit()

    ########################## For Flask image upload ##########################
    # code below, along with the allowed_file function defined above, saves img
    # A <form> tag is marked with enctype=multipart/form-data and 
    # an <input type=file> is placed in that form.
    # TODO:  write try except for RequestEntityTooLarge 16mb up
    #
    # The following conditions did not stop the process and thus raised error
    if request.files.keys() or 'file' in request.files or file.filename != '':
        new_employee_query = Employee.query.all()[-1]
        file = request.files['file']

        if file and allowed_file(file.filename):
            filename = unicode(str(new_employee.employee_id)
                       + str(secure_filename(file.filename))[-4:])
        
            # change the global upload path to this file specific path
            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER + '/employee_info_photo/'
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('Employee photo and information submitted successfully.')
        
        new_employee_query.photo_url = UPLOAD_FOLDER + '/employee_info_photo/' + filename
        db.session.commit()
    #    
    # The following will catch the error but will stop the following tables submit
    # try:
    # except UnboundLocalError:
    #     pass
    ########################## For Flask file upload end #######################

    # add company to DB if there was a user input that has to do with the table
    company_name = result['company_name']

    if company_name != None:
        # get the company with that name
        # TODO: company/title/dept name should be unique. enforce it in the model
        #       and test the case user input the same company name without selecting 
        query_company = (Company.query.options(
                                Load(Company)
                                .load_only(Company.company_id, Company.company_name)
                                )
                             .filter_by(company_name=company_name)
                             .first()
                            )
        # if the name user input exists in the database
        if query_company:
            # set the company_id to be used later on relational tables 
            company_id = query_company.company_id
        else:
            # generate new company, and set the company_id to be used later
            new_company = Company(company_name=company_name, short_name=None)
            db.session.add(new_company)
            db.session.commit()
            company_id = new_company.company_id
    else:
        company_id = 6

    # add title to DB is there was a user input has to do with the table
    title = result['title']

    if title != None:
        query_title = (Title.query.options(
                                Load(Title)
                                .load_only(Title.title_id, Title.title)
                                )
                             .filter_by(title=title)
                             .first()
                            )
        if query_title:
            title_id = query_title.title_id
        else:
            new_title = Title(title=title)
            db.session.add(new_title)
            db.session.commit()
            title_id = new_title.title_id
    else:
        title_id = 46

    # add department to DB is there was a user input has to do with the table
    department_name= result['department_name']

    if department_name != None:
        query_department = (Department.query.options(
                                Load(Department)
                                .load_only(Department.department_id, Department.department_name)
                                )
                             .filter_by(department_name=department_name)
                             .first()
                            )
        # if the name user input exists in the database
        if query_department:
            # set the company_id to be used later on relational tables 
            department_id = query_department.department_id
        else:
            # generate new company, and set the company_id to be used later
            new_department = Department(department_name=department_name)
            db.session.add(new_department)
            db.session.commit()
            department_id = new_department.department_id
    else:
        department_id = 7

    # add employee_company data with metadata input
    office_email= result['office_email']
    password= result['password']
    date_employeed= result['date_employeed']
    date_departed= result['date_departed'],
    job_description= result['job_description']
    office_phone= result['office_phone']

    db.session.add(Employee_company(office_email=office_email,
                                    password=password,
                                    date_employeed=date_employeed,
                                    date_departed=date_departed,
                                    job_description=job_description,
                                    office_phone=office_phone))
    db.session.commit()

    # add office to DB is there was a user input has to do with the table
    office_name = result['office_name']

    if office_name != None:
        query_office_name = (Office.query
                             .filter_by(office_name=office_name)
                             .first()
                            )
        if query_office_name:
            office_id = query_office_name.office_id
        else:
            new_office_name = Office(office_name=office_name)
            db.session.add(new_office_name)
            #TODO: prompt user to enter the office info
            db.session.commit()
            office_id = new_office_name.office_id
    else:
        office_id = 13

    # add department_title data
    query_department_title = (Department_title.query
                             .filter_by(department_id=department_id,
                                        title_id=title_id)
                             .first()
                            )
    if query_department_title == None:
        db.session.add(Department_title(
                                        department_id=department_id,
                                        title_id=title_id
                                        )
                        )
        db.session.commit()

    # add office_department data
    query_office_department = (Office_department.query
                                .filter_by(department_id=department_id,
                                           office_id=office_id)
                         .first()
                        )
    if query_office_department == None:
        db.session.add(Office_department(
                                         department_id=department_id,
                                         office_id=office_id
                                        ))
        db.session.commit()

    # add company_department data
    query_company_department = (Company_department.query
                                .filter_by(department_id=department_id,
                                           company_id=company_id)
                         .first()
                        )
    if query_company_department == None:
        db.session.add(Company_department(
                                          department_id=department_id,
                                          company_id=company_id
                                         ))
        db.session.commit()

    # add employee to db
    db.session.add(new_employee)
    db.session.commit()

    # TODO: modal window of the added employee data with
    #       enter more/back to home page selection button
    return redirect("/employee/add")


############### END ADD EMPLOYEE START CHANGE EMPLOYEE FEATURE ################# 


# @app.route('/employee/edit')
# def edit_employee(employee_id):
#     """Show an individual emp"""


# @app.route('/employee/edit/<employee_id>')
# def edit_employee(employee_id):
#     """Show an individual emp"""



############## END CHANGE EMPLOYEE START LOAD EXCEL FEATURE #################### 


@app.route('/employee_excel', methods=['GET'])
def employee_excel_loading():
    """Load Excel file and save"""

    return render_template('employee/excel.html')


@app.route('/employee_excel/submit', methods=['POST'])
def employee_excel():
    """Process the Excel data into DB"""

    # the file object is in python space to be used
    file = request.files['emp_xls']
    print file
    return ""


############ END LOAD EXCEL FEATURE START ORGANIZATON CHART FEATURE ############


@app.route('/company/all')
def list_companies():
    """Show organizational structure."""

    company_name = request.form.items()

    query_companies = (Company.query.options(
                                Load(Company)
                                .load_only(Company.company_id, Company.company_name)
                                )
                )
    companies = [company.company_name for company in query_companies]

    return render_template('charts/org_chart.html', companies=companies)


############ END LOAD EXCEL FEATURE START ORGANIZATON CHART FEATURE ############


@app.route('/company/all', method="POST")
def list_companies():
    """Show organizational structure."""

    if company_name:
        company = query_companies.filter_by(company_name=company_name).first()
        company_id = company.company_id
        company_name = company.company_name
        print company_id, company_name, "all of this"
    else:
        company_id = 1
        company_name = Company.query.filter_by(company_id=company_id).first().company_name
        print company_id, company_name, "all of that"

    result = {
                'name': company_name,
                'title': 'Company'}
                # 'children': []}

    # # do things in relational tables to get departments - titles - employee
    # company_departments = Company_department.query.filter_by(company_id=company_id).all()
    # for i, company_department in enumerate(company_departments):
    #     result['children'].append( {'name': company_department.departments.department_name,
    #                                 'title': 'Department',
    #                                 'children': []} )
    #     department_id = company_department.department_id
    #     department_titles = Department_title.query.filter_by(department_id=department_id).all() 
        
    #     for department_title in set(department_titles):
    #         title_id = department_title.title_id 
    #         title = department_title.titles.query.filter_by(title_id=title_id).first().title

    #         print result['children'][i]['children'].append( {
    #             'name': title,
    #             'title': 'Title'
    #             })

    structure = jsonify(result)
    # #
    # employees = Employee.query.filter_by(employee_company_id=employee_company_id).all()
    # for employee in employees:
    #     result['name'] = depatment_titiles.titiles.title
    # structure=jsonify(structure)
    return structure


############### END ORGANIZATON CHART START ADD COMPANY FEATURE ################


@app.route('/company/add')
def add_company_form():
    """Display add_company form."""

    companies = Company.query.all()

    return render_template('company/add_company.html', companies=companies)


@app.route('/add_company', methods=['POST'])
def add_company():
    """Adds company."""

    all_input = request.form.items()
    result = {}
    for key, value in all_input:
        if value == '':
            result[key] = None
        else:
            result[key] = value

    if result['company_name']==None:
        session.pop('_flashes', None)
        flash ("Please input at least the company name field.")
        return redirect('/company/add')

    query_company = (Company.query.options(
                            Load(Company)
                            .load_only(Company.company_id, Company.company_name)
                            )
                         .filter_by(company_name=result['company_name'])
                         .first()
                        )
    # if the name user input exists in the database
    if query_company:
        # set the company_id to be used later on relational tables 
        flash ("The company name is already in the database.")
        return redirect('/company/add')
    else:
        # generate new company, and set the company_id to be used later
        new_company = Company(company_name=result['company_name'], short_name=result['short_name'])
        db.session.add(new_company)
        db.session.commit()
        company_id = new_company.company_id
        flash ("The company has been added.")
        return redirect('/company/add')


############### END ADD COMPANY START ADD DEPARTMENT FEATURE ################


@app.route('/department/add')
def add_department_form():
    """Display add_department form."""

    companies = Department.query.all()

    return render_template('department/add_department.html', companies=companies)


@app.route('/add_department', methods=['POST'])
def add_department():
    """Adds department."""

    all_input = request.form.items()
    result = {}
    for key, value in all_input:
        if value == '':
            result[key] = None
        else:
            result[key] = value

    if result['department_name']==None:
        session.pop('_flashes', None)
        flash ("Please input at least the department name field.")
        return redirect('/company/add')

    query_department = (Department.query.options(
                            Load(Department)
                            .load_only(Department.department_id, Department.department_name)
                            )
                         .filter_by(department_name=result['department_name'])
                         .first()
                        )
    # if the name user input exists in the database
    if query_department:
        # set the department_id to be used later on relational tables 
        flash ("The department name is already in the database.")
        return redirect('/company/add')
    else:
        # generate new department, and set the department_id to be used later
        new_department = Department(department_name=result['department_name'], short_name=result['short_name'])
        db.session.add(new_department)
        db.session.commit()
        department_id = new_department.department_id
        flash ("The department has been added.")
        return redirect('/company/add')


############### END ADD COMPANY START ADD title FEATURE ################


@app.route('/title/add')
def add_title_form():
    """Display add_title form."""

    companies = title.query.all()

    return render_template('title/add_title.html', companies=companies)


@app.route('/add_title', methods=['POST'])
def add_title():
    """Adds title."""

    all_input = request.form.items()
    result = {}
    for key, value in all_input:
        if value == '':
            result[key] = None
        else:
            result[key] = value

    if result['title']==None:
        session.pop('_flashes', None)
        flash ("Please input at least the title name field.")
        return redirect('/company/add')

    query_title = (Title.query.options(
                            Load(Title)
                            .load_only(Title.title_id, Title.title)
                            )
                         .filter_by(title=result['title'])
                         .first()
                        )
    # if the name user input exists in the database
    if query_title:
        # set the title_id to be used later on relational tables 
        flash ("The title name is already in the database.")
        return redirect('/company/add')
    else:
        # generate new title, and set the title_id to be used later
        new_title = title(title=result['title'])
        db.session.add(new_title)
        db.session.commit()
        title_id = new_title.title_id
        flash ("The title has been added.")
        return redirect('/company/add')


################ END ADD DEPARTMENT START GOOGLE MAP FEATURE ################### 


@app.route('/map')
def map():
    """Show a map with markers to pin the office locations."""

    # Practice: Using global varialbe 
    # Google Map key secret. import os is used with this code.
    # Also, in terminal, use the following command to make sure you have the key 
    # source the file that contanins <export GOOGLE_MAP_KEY="key value">
    api_key = os.environ['GOOGLE_MAP_KEY']
    return render_template('charts/map.html', api_key=api_key)

    # return render_template('map.html') # if you decide to hardcode your api_key


################### END GOOGLE MAP START STATISTICS FEATURE ###################


@app.route('/statistics')
def statistics():
    """Show statistics and charts."""

    return render_template('charts/statistics.html')


@app.route('/temp')
def temp():
    """Show statistics and charts."""

    return render_template('temp.html')


################### END STATISTICS START LOADING APP ##########################


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
