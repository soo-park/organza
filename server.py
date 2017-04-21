# -*- coding: utf-8 -*-
# Line one is necessary to have utf-8 recognized
import sys, json
reload(sys)
sys.setdefaultencoding('utf8')

import os
import datetime

# Execute Flask object
from flask import (Flask, jsonify, render_template, request, flash, redirect,
                   session, url_for, send_from_directory)
# from flask_debugtoolbar import DebugToolbarExtension
app = Flask(__name__)

# for SQLAlchemy to load only certain columns
from sqlalchemy.orm import Load, load_only
from sqlalchemy.sql import func

# for file upload
from werkzeug.utils import secure_filename 
UPLOAD_FOLDER = 'static/img'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # limits upload to 16mb

# import employee related models
from model import (Employee, Employee_company, Company, Department,Title,
                   Office, Company_department, Department_title, Hierarchy,
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

    if "permission" in session.keys():
        if session["permission"] == "admin":
            return redirect('/admin_logged')
        elif  session["permission"] == "employee":
            return redirect('/employee_logged')
        else:
            return redirect('/logged')
    else:
        return render_template('index.html')


#################### END HOME START OF LOGIN FEATURE ###########################


@app.route('/login', methods=['POST'])
def login():
    """Login user to the user specific information."""

    username = request.form.get('username')
    password = request.form.get('password')
    db_employees = Employee.query.filter_by(username=username).all()
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
            if db_employee.admin == True:
                session["permission"] = "admin"
                return redirect('/admin_logged')
            if date_employeed and not date_departed:
                session["permission"] = "employee"
                return redirect("/employee_logged")
            elif date_employeed and date_departed:
                session["permission"] = "user"
                flash('Welcome, general user. If you are an employee, please contact the admin.')
                return redirect("/logged")
            else:
                session["permission"] = "user"
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
    if session["permission"] == "user":
        return render_template('home/general.html') # (date_employeed and date_departed)
    return redirect('/')


@app.route('/employee_logged')
def employee_logged():
    """Login as an employee"""
    if session["permission"] == "employee":
        return render_template('home/employee.html')
    return redirect('/')


@app.route('/admin_logged')
def admin_logged():
    """Login as an admin"""
    if session["permission"] == "admin":
        return render_template('home/admin.html')
    return redirect('/')


#*# Session log out
@app.route('/logout', methods=['POST'])
def logout():
    del session["permission"]
    session['logged_in'] = False
    session.pop('username', None)
    return redirect('/')
 

################# END LOGIN START EMPLOYEE SEARCH FEATURE ######################


@app.route('/employee/data/<int:offset>/<int:limit>')
def limit_list(offset, limit):
    """limits the amount of employees loaded up on HTML"""

    employees = (Employee.query.options(
                            Load(Employee)
                            .load_only(Employee.first_name,
                                       Employee.last_name,
                                       Employee.employee_id)
                            )
                            .order_by(Employee.employee_id)
                            .offset(offset)
                            .limit(limit).all()
                        )
    return jsonify({'employees':[{'first_name': employee.first_name,
                                  'last_name': employee.last_name, 
                                  'employee_id': employee.employee_id} 
                                  for employee in employees]}), 200


@app.route('/employee/all')
def listba_employees():
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
                                                 employee_count=len(employees),
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

    # Lazy load employees
    query_employees = (Employee.query.options(Load(Employee)
                            .load_only(Employee.employee_id,
                                       Employee.first_name,
                                       Employee.last_name)
                            )
                        )

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
                'first_name': query_employees[i].__dict__['first_name'],
                'last_name': query_employees[i].__dict__['last_name'] 
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

    return redirect("/employee/add")


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
    return ""


############ END LOAD EXCEL FEATURE START ORGANIZATON CHART FEATURE ############


@app.route('/company/all')
def list_companies():
    """Show organizational structure."""

    query_companies = (Company.query.options(
                                Load(Company)
                                .load_only(Company.company_id, Company.company_name)
                                )
                )
    companies = [company.company_name for company in query_companies]

    company_name = request.form.items()

    query_companies = (Company.query.options(
                                Load(Company)
                                .load_only(Company.company_id, Company.company_name)
                                )
                )

    if company_name:
        company = query_companies.filter_by(company_name=company_name).first()
        company_id = company.company_id
        company_name = company.company_name
    else:
        company_id = 1
        company_name = Company.query.filter_by(company_id=company_id).first().company_name

    employees = Employee.query.join(Employee_company).filter_by(company_id=company_id)

    ceo_title_id = 11
    ceo = employees.join(Title).filter_by(title_id=ceo_title_id).first()

    result = {
                "name": "CEO",
                "title": ceo.first_name + " " + ceo.last_name,
                'className': 'top-level',
                "children": []
            }

    departments = Department.query.all()
    for i, department in enumerate(departments):
        if department.department_name != "C-level":
            result['children'].append( {"name": department.department_name,
                                        "title": "Department Head",
                                        'className': 'middle-level',
                                        "children": []} )


    titles = Title.query.all()
    all_employee = employees.all()
    department_titles = Department_title.query.all()

    ####### Below code is to display sudo names to view the org chart ##########
    # titles_per_department = {
    #     1: [11, 30], 
    #     2: [2, 5, 6, 7, 10, 13, 16, 17, 20, 21, 22, 23, 25, 26, 27, 28, 34, 35, 36, 37, 38, 39, 41, 42, 46], 
    #     3: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 13, 14, 15, 16, 17, 20, 22, 23, 25, 26, 27, 35, 38, 39, 41, 42, 46], 
    #     4: [2, 6, 38, 7, 41, 42, 39, 13, 46, 16, 17, 20, 22, 23, 25, 26, 27, 10, 5], 
    #     5: [2, 5, 6, 7, 10, 12, 13, 16, 17, 18, 19, 20, 22, 23, 24, 25, 26, 27, 29, 31, 32, 33, 38, 39, 40, 41, 42, 43, 44, 45, 46], 
    #     6: [2, 5, 6, 7, 38, 41, 42, 39, 13, 46, 16, 17, 20, 22, 23, 25, 26, 27, 10], 
    #     7: [2, 5, 6, 39, 38, 41, 10, 7, 13, 46, 16, 17, 20, 22, 23, 25, 26, 27, 42]
    #     }

    # for key in titles_per_department:
    #     for i, number in enumerate(titles_per_department[key]):
    #         for title in titles:
    #             if number == title.title_id:
    #                 titles_per_department[key][i] = title.title

    # print titles_per_department
    count = 1
    for title in titles:
        title_id = title.title_id
        title = title.title
        for item in result['children']:
            if title != 'CEO': 
                employee_name = all_employee[count].first_name + " " + all_employee[count].last_name
                item['children'].append( {
                    "name": title,
                    "title": employee_name,
                    'className': 'bottom-level'
                    })
            count += 1


    for item in result['children']:
        item['title'] = all_employee[count].first_name + " " + all_employee[count].last_name
        count+=1

    ####### Above code is to display sudo names to view the org chart ##########

    structure = json.dumps(result, ensure_ascii=False)

    return render_template('charts/org_chart.html', companies=companies,
                                                    structure=structure)


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

    # Google Map key secret. import os is used with this code.
    # in terminal, source the file that contanins <export GOOGLE_MAP_KEY="key value">
    api_key = os.environ['GOOGLE_MAP_KEY']

    return render_template('charts/map.html', api_key=api_key)


@app.route('/data/companies')
def map_company_data():
    """Get map company data"""

    offices = (Office.query.join(Office_department)
                        .join(Department)
                        .join(Company_department)
                        .join(Company)
                        .all()
                    )
    result = {"data": []}

    for i, office in enumerate(offices):
        office_data = change_sql_sub_obj_into_dic(office)
        if office_data['address']:
            result["data"].append({ 'office_name': office_data['office_name'].split(",")[0],
                                   'address': office_data['address'],
                                   'city': office_data['city'],
                                   'state': office_data['state'],
                                   'country': office_data['country'],
                                   'postal_code': office_data['postal_code'],
                                   'phone': office_data['phone'],
                                   'fax': office_data['fax']
                                  })

    return jsonify(result)


################### END GOOGLE MAP START STATISTICS FEATURE ###################


@app.route('/statistics')
def statistics():
    """Show statistics and charts."""

    background_color = {
                        0: 'rgba(255, 99, 132, 0.2)',
                        1: 'rgba(54, 162, 235, 0.2)',
                        2: 'rgba(255, 206, 86, 0.2)',
                        3: 'rgba(75, 192, 192, 0.2)',
                        4: 'rgba(153, 102, 255, 0.2)',
                        5: 'rgba(255, 159, 64, 0.2)'
                        }

    border_color = {
                    0: 'rgba(255,99,132,1)',
                    1: 'rgba(54, 162, 235, 1)',
                    2: 'rgba(255, 206, 86, 1)',
                    3: 'rgba(75, 192, 192, 1)',
                    4: 'rgba(153, 102, 255, 1)',
                    5: 'rgba(255, 159, 64, 1)'
                    }

    ################################################################
    # number of people in a company bar chart data
    employee_companies = Employee_company.query.options(
                            Load(Employee_company)
                            .load_only(Employee_company.company_id)
                            ).all()
    
    result = {}
    for employee_company in employee_companies:
        if employee_company.company_id in result:
            result[employee_company.company_id] += 1
        else:
            result[employee_company.company_id] = 1

    companies = Company.query.options(
                            Load(Company)
                            .load_only(Company.company_id, Company.company_name)
                            ).all()

    company_names = {}
    for company in companies:
        company_names[company.company_id] = company.company_name

    labels = []
    data = []
    background = []
    border = []

    for label, value in result.iteritems():
        if label in company_names:
            label = str(company_names[label])
        labels.append(label)
        data.append(value)
        color_key = len(data)%6
        background.append(background_color[color_key])
        border.append(border_color[color_key])

    ################################################################
    # same calculation with dif query can be repeated with the rest of three charts
    ################################################################

    background= json.dumps(background, ensure_ascii=False)
    labels = json.dumps(labels, ensure_ascii=False)
    data = json.dumps(data, ensure_ascii=False)

    # return result
    return render_template('charts/statistics.html', data=data
                                                   , labels=labels
                                                   , background=background
                                                   , border=border)


@app.route('/temp')
def temp():
    """Show statistics and charts."""

    return render_template('temp.html')


################### END STATISTICS START LOADING APP ##########################


if __name__ == '__main__':
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # # Use the DebugToolbar
    # DebugToolbarExtension(app)

    # Run internal server
    app.run(port=5000, host='0.0.0.0')
