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
UPLOAD_FOLDER = 'static/img/employee_info_photo'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # limits upload to 16mb

# import employee related models
from model import (Employee, Employee_company, Company, Department,Title,
                   Office, Company_department, Department_title,
                   Office_department, connect_to_db, db)
from employee_query import *
from utilities import get_map_from_sqlalchemy

# "source secret.sh" to run flask server prior to "python server.py"
# content of the sercret.sh: export secret_key="<your secret key>"
app.secret_key = os.environ['secret_key']

# undefined variable in Jinja2, not fails silently but raises an error
from jinja2 import StrictUndefined
app.jinja_env.undefined = StrictUndefined


### TODO: Use regx to enforce formatting
@app.route('/')
def index():
    """Homepage."""

    # return render_template('index.html')
    return render_template('home_admin.html')

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

    return render_template('home_general.html') # (date_employeed and date_departed)


@app.route('/employee_logged')
def employee_logged():
    """Login as an employee"""

    return render_template('home_employee.html')


@app.route('/admin_logged')
def admin_logged():
    """Login as an admin"""

    return render_template('home_admin.html')
    

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

        # When jasonifying, you cannot use date(time) object
        # thus need to strftime the object to be read as a string
        result[employee.employee_id]['birthday']=result[employee.employee_id]['birthday'].strftime("%Y/%m/%d")

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
    # TODO: change the hardcode below to have dynamic variables
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
                            admin= request.form.get('admin')
                            )
    # add employee to db
    db.session.add(new_employee)
    db.session.commit()


    # add company to DB if there was a user input that has to do with the table
################################## ################################## ################################## 
############TODO: refactor lator to a reusable code (get primary key and return)
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
        title_id = None

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
        department_id = None

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
        office_id = None

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
################################## ################################## ################################## 

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

    # Practice: Using global varialbe 
    # Google Map key secret. import os is used with this code.
    # Also, in terminal, use the following command to make sure you have the key 
    # source <the file that contanins GOOGLE_MAP_KEY variable>
    api_key = os.environ['GOOGLE_MAP_KEY']
    # Passing secret key to the html
    return render_template('map.html', api_key=api_key)

    # return render_template('map.html') # if you decide to hardcode your api_key


######################### For Flask file upload ############################
# http://flask.pocoo.org/docs/0.12/patterns/fileuploads/

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/file_upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return render_template('upload_file_image.html', filename=filename)

    print "File upload unsuccessful. Try again."
    return render_template('upload_file.html')

    # FIXME:  write try except for RequestEntityTooLarge 16mb up
    # FIXME: load the image upto the info page without reload using JQuery 
    # A <form> tag is marked with enctype=multipart/form-data and 
    # an <input type=file> is placed in that form.
    # The application accesses the file from the files dictionary on the request object.
    # use the save() method of the file to save the file permanently 
    # somewhere on the filesystem.

######################### For Flask file upload end #########################


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
