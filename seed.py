"""Utility file to seed intranet database from initial data file in static/doc folder"""

from sqlalchemy import func

# import employee related models
from model import Employee
from model import Employee_company

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


def purge_tables():
    """Purges existing data to prevent data overlap."""

    # TODO: ask user if the user is sure to purge all data in intranet db
    print 'Existing data on tables will be purged.'

    # Delete all rows in employee related table in case some data's there
    Employee_company.delete()
    Department_title.delete()
    Company_department.delete()
    Office_department.delete()

    # After middle table, delete the others
    Employee.query.delete()  
    Title.delete()
    Department.delete()
    Company.delete()
    Office.delete()

    # add to the session and commit the employee line
    db.session.add(employee)
    db.session.commit()

    print 'Talbes purged.'

# # TODO: finish separating data to seed
# def open_file():
#     """FIXME: open as unicode"""

#     # list of dictionaries that has 
#     # [employee1: {first_name, mid_name, last_name, personal_email}, 
#     # employee2: {first_name, mid_name, last_name, personal_email} ... ]

#     result = {}
#     file = open('static/doc/_employee_seed_sample.csv')
#     for row in file:
#         first_name, mid_name, last_name, personal_email = row.rstrip().split(',')

#     return result


def load_employees():
    """Load employees from static/doc/employee.csv into database."""

    # TODO: bring in open_file to do seeding
    # indicates the process
    print 'Employees seeding'

    file = open_file
    open('static/doc/_employee_seed_sample.csv')
    for row in file:
        first_name, mid_name, last_name, personal_email = row.rstrip().split(',')
        employee = Employee(
                            photo_URL=photo_URL,
                            birthday=birthday,
                            personal_email=personal_email,
                            first_name=first_name,
                            mid_name=mid_name,
                            last_name=last_name,
                            nickname=nickname,
        # # FIXME: test unicode save & import from csv, txt, excel
                            k_name=k_name,
                            kanji_name=kanji_name,
                            phone=phone,
                            mobile=mobile,
                            address_line1=address_line1,
                            address_line2=address_line2,
                            city=city,
                            country=country,
                            postal_code=postal_code,
                            emergency_name=emergency_name,
                            emergency_phone=emergency_phone,
                            )

        # add to the session and commit the employee line
        db.session.add(employee)
        db.session.commit()

    file = open('static/doc/_employee_seed_sample.csv')
    for row in file:
        first_name, mid_name, last_name, personal_email = row.rstrip().split(',')
        employee_company = Employee_company(
                                            office_email=office_email,
                                            password=office_email_password,
                                            date_employeed=date_employeed,
                                            date_departed=date_departed,
                                            job_description=job_description,
                                            office_phone=office_phone
                                            )
        db.session.add(employee_company)
        db.session.commit()

    print 'Employee seeding compeleted.'


def load_titles():

    # TODO: bring in open_file to do seeding
    print 'title seeding'

    file = open('static/doc/_employee_seed_sample.csv')
    for row in file:
        first_name, mid_name, last_name, personal_email = row.rstrip().split(',')
        title = title(
                      title=title,
                      k_title=k_title
                     )
        db.session.add(title)
        db.session.commit()

    print 'title seeding compeleted.'


def load_departments():

    # TODO: bring in open_file to do seeding
    print 'department seeding'

    file = open('static/doc/_employee_seed_sample.csv')
    for row in file:
        first_name, mid_name, last_name, personal_email = row.rstrip().split(',')

        department = department(
                                name=name
                               )
        db.session.add(department)
        db.session.commit()

    print 'department seeding compeleted.'

# get all of the same title and add that to a relationship


def load_companies():

    # TODO: bring in open_file to do seeding
    print 'company seeding'

    file = open('static/doc/_employee_seed_sample.csv')
    for row in file:
        first_name, mid_name, last_name, personal_email = row.rstrip().split(',')

        company = company(
                          name=name,
                          doing_business_as=doing_busniess_as,
                          abbreviation=abbreviation
                         )
        db.session.add(company)
        db.session.commit()

    print 'company seeding compeleted.'


def load_offices():

    # TODO: bring in open_file to do seeding
    print 'office seeding'

    file = open('static/doc/_employee_seed_sample.csv')
    for row in file:
        first_name, mid_name, last_name, personal_email = row.rstrip().split(',')

        office = office(
                        name=name,
                        phone=phone,
                        address_line1=address_line1,
                        address_line2=address_line2,
                        city=city,
                        country=country,
                        postal_code=postal_code,
                        fax=fax
                       )
        db.session.add(office)
        db.session.commit()

    print 'office seeding compeleted.'


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    purge_tables()
    # open_file()
    load_titles()
    load_departments()
    load_companies()
    load_offices()