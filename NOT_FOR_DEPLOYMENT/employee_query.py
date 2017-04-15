#### STUDY: Doing only one query with existing/non existing search criteria #####

# reusable code for queires

from model import (Employee, Employee_company, Company, Department,Title,
                   Office, Company_department, Department_title,
                   Office_department, connect_to_db, db)

# # join query - one filter criterion
# id_of_first_employee_that_fits_filter = (Employee.query
#                                         .join(Employee_company)
#                                         .all())[0].employee_id

# keyword arguments must come in the form of 
# {'email' : 'a@seahusa.com', 'first_name': 'firsta'}
# the result will be a list of query object of the employee of that criteria
# [<Employee employee_id=1, first_name=firsta>, <Employee employee_id=2, first_name=firstb>]

# depends on the argument received, the dictionary length will differ
# because there are multiple tables to join to do query AND
# the table name has to be combined into the query name OUTSIDE the HTML
# ('Company.company_name' is not accepted as an argument of kwargs)
# used funamental theorem of arithmetic to assign different cases to cases
def query_selector(kwargs):

    rank = 1

    if "company_name" in kwargs.keys():
        rank*=2
    if "department_name" in kwargs.keys():
        rank*=3
    if "first_name" in kwargs.keys():
        rank*=5
    if "last_name" in kwargs.keys():
        rank*=7
    if "email" in kwargs.keys():
        rank*=11

    queries= {
             1 : search_no_criteria,
             2 : search_by_company_name,
             3 : search_by_department_name,
             5 : search_by_first_name,
             7 : search_by_last_name,
             11 : search_by_email,
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

    # returns list of query objects
    queried_employees = queries[rank](**kwargs)
    # print queried_employees

    return queried_employees

#no argument need work
def search_no_criteria(**kwargs):
    result = (db.session.query(Employee)
                       .join(Employee_company)
                       .join(Company)
                       .join(Company_department)
                       .join(Department)
                       .join(Department_title)
                       .join(Title)
                       .distinct()
                       .all())
    print "No search criteria"
    return result


def search_by_company_name(**kwargs):
    result = (db.session.query(Employee)
                       .join(Employee_company)
                       .join(Company)
                       .filter_by(company_name = kwargs['company_name'])
                       .join(Company_department)
                       .join(Department)
                       .join(Department_title)
                       .join(Title)
                       .distinct()
                       .all())
    return result


def search_by_department_name(**kwargs):
    result = (db.session.query(Employee)
                         .join(Employee_company)
                         .join(Company)
                         .join(Company_department)
                         .join(Department)
                         .filter_by(department_name = kwargs['department_name'])
                         .join(Department_title)
                         .join(Title)
                         .distinct()
                         .all())
    return result


def search_by_first_name(**kwargs):
    result = (db.session.query(Employee)
                         .filter_by(first_name = kwargs['first_name'])
                         .join(Employee_company)
                         .join(Company)
                         .join(Company_department)
                         .join(Department)
                         .join(Department_title)
                         .join(Title)
                         .distinct()
                         .all())
    return result


def search_by_last_name(**kwargs):
    result = (db.session.query(Employee)
                         .filter_by(last_name = kwargs['last_name'])
                         .join(Employee_company)
                         .join(Company)
                         .join(Company_department)
                         .join(Department)
                         .join(Department_title)
                         .join(Title)
                         .distinct()
                         .all())
    return result


def search_by_email(**kwargs):
    result = (db.session.query(Employee)
                         .join(Employee_company)
                         .filter_by(office_email = kwargs['email'])
                         .join(Company)
                         .join(Company_department)
                         .join(Department)
                         .join(Department_title)
                         .join(Title)
                         .distinct()
                         .all())
    return result


def search_by_company_name_department_name(**kwargs):
    result = (db.session.query(Employee)
                         .join(Employee_company)
                         .join(Company)
                         .filter_by(company_name = kwargs['company_name'])
                         .join(Company_department)
                         .join(Department)
                         .filter_by(department_name = kwargs['department_name'])
                         .join(Department_title)
                         .join(Title)
                         .distinct()
                         .all())
    return result


def search_by_company_name_first_name(**kwargs):
    result = (db.session.query(Employee)
                         .filter_by(first_name = kwargs['first_name'])
                         .join(Employee_company)
                         .join(Company)
                         .filter_by(company_name = kwargs['company_name'])
                         .join(Company_department)
                         .join(Department)
                         .join(Department_title)
                         .join(Title)
                         .distinct()
                         .all())
    return result


def search_by_company_name_last_name(**kwargs):
    result = (db.session.query(Employee)
                         .filter_by(last_name = kwargs['last_name'])
                         .join(Employee_company)
                         .join(Company)
                         .filter_by(company_name = kwargs['company_name'])
                         .join(Company_department)
                         .join(Department)
                         .join(Department_title)
                         .join(Title)
                         .distinct()
                         .all())
    return result


def search_by_department_name_first_name(**kwargs):
    result = (db.session.query(Employee)
                         .filter_by(first_name = kwargs['first_name'])
                         .join(Employee_company)
                         .join(Company)
                         .join(Company_department)
                         .join(Department)
                         .filter_by(department_name = kwargs['department_name'])
                         .join(Department_title)
                         .join(Title)
                         .distinct()
                         .all())
    return result


def search_by_department_name_last_name(**kwargs):
    result = (db.session.query(Employee)
                         .filter_by(last_name = kwargs['last_name'])
                         .join(Employee_company)
                         .join(Company)
                         .join(Company_department)
                         .join(Department)
                         .filter_by(department_name = kwargs['department_name'])
                         .join(Department_title)
                         .join(Title)
                         .distinct()
                         .all())
    return result


def search_by_first_name_last_name(**kwargs):
    result = (db.session.query(Employee)
                         .filter(Employee.last_name == kwargs['last_name'],
                                 Employee.first_name == kwargs['first_name'])                         
                         .join(Employee_company)
                         .join(Company)
                         .join(Company_department)
                         .join(Department)
                         .join(Department_title)
                         .join(Title)
                         .distinct()
                         .all())
    return result


def search_by_company_name_department_name_first_name(**kwargs):
    result = (db.session.query(Employee)
                        .filter_by(first_name = kwargs['first_name'])
                        .join(Employee_company)
                        .join(Company)
                        .filter_by(company_name = kwargs['company_name'])
                        .join(Company_department)
                        .join(Department)
                        .join(Department_title)
                        .join(Title)
                        .distinct()
                        .all())
    return result


def search_by_company_name_department_name_last_name(**kwargs):
    result = (db.session.query(Employee)
                        .filter_by(last_name = kwargs['last_name'])
                        .join(Employee_company)
                        .join(Company)
                        .filter_by(company_name = kwargs['company_name'])
                        .join(Company_department)
                        .join(Department)
                        .filter_by(department_name = kwargs['department_name'])
                        .join(Department_title)
                        .join(Title)
                        .distinct()
                        .all())
    return result


def search_by_company_name_first_name_last_name(**kwargs):
    result = (db.session.query(Employee)
                        .filter(Employee.last_name == kwargs['last_name'],
                                Employee.first_name == kwargs['first_name'])                         
                        .join(Employee_company)
                        .join(Company)
                        .filter_by(company_name = kwargs['company_name'])
                        .join(Company_department)
                        .join(Department)
                        .join(Department_title)
                        .join(Title)
                        .distinct()
                        .all())
    return result


def search_by_department_name_first_name_last_name(**kwargs):
    result = (db.session.query(Employee)
                        .filter(Employee.last_name == kwargs['last_name'],
                                Employee.first_name == kwargs['first_name'])                         
                        .join(Employee_company)
                        .join(Company)
                        .join(Company_department)
                        .join(Department)
                        .filter_by(department_name = kwargs['department_name'])
                        .join(Department_title)
                        .join(Title)
                        .distinct()
                        .all())
    return result


def search_by_all_four(**kwargs):
    result = (db.session.query(Employee)
                        .filter(Employee.last_name == kwargs['last_name'],
                                Employee.first_name == kwargs['first_name'])
                        .join(Employee_company)
                        .join(Company)
                        .filter_by(company_name = kwargs['company_name'])
                        .join(Company_department)
                        .join(Department)
                        .filter_by(department_name = kwargs['department_name'])
                        .join(Department_title)
                        .join(Title)
                        .distinct()
                        .all())
    return result


# def new_search_criteria(**kwargs):
#     pass
#     raise NotImplementedError


################################################################################
# The code below can be used in server.py to do the search

def company_department_first_last_search():
    """Search the query result for the right employees for criteria"""
    ############################################################################
    # FIXME: if an employee have fields that are empty, the search result is incorrect
    ############################################################################
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
    print kwargs

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
        result[employee.employee_id] = attr_all_added

        # When jasonifying, you cannot use date(time) object
        # thus need to strftime the object to be read as a string
        result[employee.employee_id]['birthday']=result[employee.employee_id]['birthday'].strftime("%Y/%m/%d")
        
    print result
    return jsonify(result)