# reusable code for queires

from model import (Employee, Employee_company, Company, Department,Title,
                   Office, Company_department, Department_title,
                   Office_department, connect_to_db, db)

# # join query - one filter criterion
# id_of_first_employee_that_fits_filter = (Employee.query
#                                         .join(Employee_company)
#                                         .all())[0].employee_id

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


# def search_by_name(**kwargs):
#     pass
#     raise NotImplementedError

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