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


def load_employees():
    """Load employees from static/doc/employee.csv into database."""

    Employee.query.delete()  # Delete all rows in table in case some data's there
    Nickname.query.delete()
    Emergency_contact.delete()
    K_contact.delete()
    Employee_department.delete()

    # indicates the process
    print 'Employee related tables cleared. Employees seeding'

    file = open('static/doc/employee.csv')
    for row in file:
        first_name, mid_name, last_name, personal_email = row.rstrip().split(',')
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
        # nickname = Nickname(
        #                     nickname=nickname,
        #                     k_name=k_name, 
        #                     kanji_name=kanji_name
        #                     )
        # db.session.add(employee)
        # db.session.commit()


    print 'Employee seeding compeleted.'


def load_companies():


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_employees()
