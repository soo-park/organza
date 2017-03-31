"""Utility file to seed intranet database from initial data file in static/doc folder"""

from sqlalchemy import func

# import employee related models
from model import Employee
from model import Nickname
from model import Emergency_contact
from model import K_contact
from model import Employee_department

# import company related models
from model import Title
from model import Department_title
from model import Department
from model import Company_department
from model import Company
from model import Office_department
from model import Office

from model import connect_to_db, db
from server import app
import datetime


### TODO ###
# Build a function for importing Excel (below code imports one cell)
# def import_Excel():
    # import openpyxl
    # from openpyxl import load_workbook
    # wb = load_workbook(filename = 'static/doc/employee.xlsx')
    # sheet_ranges = wb['test'] #use the workbook tab name
    # print(sheet_ranges['A2'].value)


def purge_tables():
    """Purges existing data to prevent data overlap."""

    # TODO: ask user if the user is sure to purge all data in intranet db
    print 'Existing data on tables will be purged.'

    # Delete all rows in employee related table in case some data's there
    Employee.query.delete()  
    Nickname.query.delete()
    Emergency_contact.delete()
    K_contact.delete()
    Employee_department.delete()
    Title.delete()
    Department_title.delete()
    Department.delete()
    Company_department.delete()
    Company.delete()
    Office_department.delete()
    Office.delete()

    print 'Talbes purged.'


def read_file_in():
    """Reads in data file."""

    print 'Reading in the data file.'

    file = open('static/doc/employee.csv')
    for row in file:
        first_name, mid_name, last_name, personal_email = row.rstrip().split(',')


# Load employees, nickname, emergency_contact, k_contact, department, 
def load_employees():
    """Load employees from static/doc/employee.csv into database."""

    # indicates the process
    print 'Employees seeding'

        employee = Employee(
                            first_name=first_name, 
                            mid_name=mid_name, 
                            last_name=last_name, 
                            personal_email=personal_email,
                            )

        # add to the session and commit the employee line
        db.session.add(employee)
        db.session.commit()

        # # add after unicode issue has been resolved
        nickname = Nickname(
                            nickname=nickname,
                            k_name=k_name, 
                            kanji_name=kanji_name
                            )
        db.session.add(employee)
        db.session.commit()

        emergency_contacts = Emergency_contact(
                                               nickname=nickname,
                                               k_name=k_name, 
                                               kanji_name=kanji_name
                                               )
        db.session.add(employee)
        db.session.commit()

        k_contacts = K_contact(
                               nickname=nickname,
                               k_name=k_name, 
                               kanji_name=kanji_name
                               )
        db.session.add(employee)
        db.session.commit()


        employee_departments = Employee_department(
                                                   nickname=nickname,
                                                   )
        db.session.add(employee)
        db.session.commit()

    print 'Employee seeding compeleted.'


def load_company():

    # Delete all rows in company related table in case some data's there



def load_relations():


    Title
    Department_title
    Department
    Company_department
    Company
    Office_department
    Office





if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    purge_tables()
    read_file_in()
    load_employees()
    load_company()
    load_relations()