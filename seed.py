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
                            photo_URL=photo_URL,
                            birthyear=birthyear,
                            birthday=birthday,
                            personal_email=personal_email,
                            first_name=first_name,
                            mid_name=mid_name,
                            last_name=last_name,
                            country_code=country_code,
                            phone=phone,
                            mobile=mobile,
                            address_1st_line=address_1st_line,
                            address_2nd_line=address_2nd_line,
                            country=country,
                            postal_code=postal_code,
                            fax=fax,
                            comment=comment
                            )

        # add to the session and commit the employee line
        db.session.add(employee)
        db.session.commit()

        # # FIXME: test unicode save & import from csv, txt, excel
        nickname = Nickname(
                            nickname=nickname,
                            k_name=k_name,
                            kanji_name=kanji_name
                            )
        db.session.add(nickname)
        db.session.commit()

        emergency_contact = Emergency_contact(
                                               emergency_name=emergency_name,
                                               emergency_phone=emergency_phone,
                                               emergency_comment=emergency_comment
                                               )
        db.session.add(emergency_contact)
        db.session.commit()

        k_contact = K_contact(
                               k_country_code=k_country_code,
                               k_phone=k_phone,
                               k_mobile=k_mobile,
                               k_address_1st_line=k_address_1st_line,
                               k_address_2nd_line=k_address_2nd_line,
                               k_country=k_country,
                               k_postal_code=k_postal_code,
                               k_email=k_email,
                               k_fax=k_fax,
                               k_title=k_title,
                               k_comment=k_comment
                               )
        db.session.add(k_contact)
        db.session.commit()


        employee_department = Employee_department(
                                                    job_description=job_description,
                                                    date_employeed=date_employeed,
                                                    date_departed=date_departed,
                                                    office_email=office_email,
                                                    office_email_password=office_email_password,
                                                    office_pc=office_pc,
                                                    office_pc_password=office_pc_password,
                                                    office_phone=office_phone,
                                                    office_comment=office_comment
                                                   )
        db.session.add(employee_department)
        db.session.commit()

    print 'Employee seeding compeleted.'


def load_companies():

    print 'Company seeding'

        title = Title(
                      title=title,
                      k_title=k_title
                     )
        db.session.add(title)
        db.session.commit()

        department = Department(
                                department_name=department_name
                               )
        db.session.add(department)
        db.session.commit()

        company = Company(
                          company_name=company_name,
                          shrot_name=shrot_name
                         )
        db.session.add(company)
        db.session.commit()

        office = Office(
                        Office=Office,
                        office_name=office_name,
                        c_country_code=c_country_code,
                        c_area_code=c_area_code,
                        c_phone=c_phone,
                        c_mobile=c_mobile,
                        c_address_1st_line=c_address_1st_line,
                        c_address_2nd_line=c_address_2nd_line,
                        c_country=c_country,
                        c_postal_code=c_postal_code,
                        c_fax=c_fax,
                        c_comment=c_comment
                       )
        db.session.add(office)
        db.session.commit()

    print 'Company seeding compeleted.'


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    purge_tables()
    read_file_in()
    load_employees()
    load_companies()