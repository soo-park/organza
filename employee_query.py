# reusable code for queires

from model import (Employee, Employee_company, Company, Department,Title,
                   Office, Company_department, Department_title,
                   Office_department, connect_to_db, db)

# # join query - one filter criterion
# id_of_first_employee_that_fits_filter = (Employee.query
#                                         .join(Employee_company)
#                                         .all())[0].employee_id


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
    return result


def search_by_company_name(**kwargs):
    result = (db.session.query(Employee)
                       .join(Employee_company)
                       .join(Company)
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


#need work
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