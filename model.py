"""Models and database functions for intranet project.
Skeleton codes generated with stacks from Hackbright.
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Connection to the PostgreSQL database comes through the Flask-SQLAlchemy
# helper library. There is a `session` object, where interactions are done.
db = SQLAlchemy()



### TODO: Foreign keys are set as relationships. See DB model and change.
# Employee definitions

class Employee(db.Model):
    """Employee of the group."""

    __tablename__ = "employees"

    employee_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String(50))
    mid_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50))

    ### TODO ###
    # if the personal email is nullable, 
    # and the office email belongs to the form
    # how are you going to log-in and authentificate?
    personal_email = db.Column(db.String(100), nullable=True)
    birthyear = db.Column(db.DateTime, nullable=True)
    birthday = db.Column(db.DateTime, nullable=True)
    photo_URL = db.Column(db.String(100), nullable=True)

    ### TODO ###
    # Figure out what kind of db.relationship is good
    # nicknames = db.relationship('Nickname')
    # home_addresses = db.relationship('Address')
    # employee_phones = db.relationship('Employee_phone')
    # Employee_dept_offices = db.relationship('Employee_dept_office')
    # emergency_contact_people = db.relationship('Emergency_contact_person')
    
    ### TODO ###
    # A field that wil be feeding off of email for the employee?
    # Generate the log_in table?
    # login = Required('Login')

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Employee employee_id=%s first_name=%s>" %(self.employee_id, self.first_name)


    # import openpyxl

    from openpyxl import load_workbook
    wb2 = load_workbook('static/doc/test.xlsx')
    print wb2.get_sheet_names()


# # TODO: finish unicode problem in seed.py to add these fields
# class Nickname(db.Model):
#     """Nickname for a person."""

#     __tablename__ = "nicknames"

#     # one to one relationship to employee: OK for a ForeignKey as primary key
#     # nickname_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     employee_id = db.Column(db.Integer, db.ForeignKey('employees.employee_id'), primary_key=True)
#     nickname = db.Column(db.Unicode(50), nullable=True)
#     k_name = db.Column(db.Unicode(50), nullable=True)
#     kanji_name = db.Column(db.Unicode(50), nullable=True)

#     employees = db.relationship('Employee')

#     def __repr__(self):
#         """Provide helpful representation when printed."""

#         return "<Nickname k_name=%s kanji_name=%s>" %(self.k_name, self.kanji_name)


## Employee association and middle tables

# class Employee_phone(db.Model):
#     """Middle table btw Employee and Phone."""

#     __tablename__ = "employee_phones"

#     id = db.Column(db.Integer, autoincrement=True, primary_key=True)

#     employees = db.relationship('Employee')
#     contacts = db.relationship('Contact')

#     def __repr__(self):
#         """Provide helpful representation when printed."""

#         return "<Employee employee_id=%s first_name=%s>" %(self.employee_id, self.first_name)


# class Emergency_contact_person(db.Model):
#     """Emergency contact for an employee."""

#     __tablename__ = "emergency_contact_people"

#     id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     name = db.Column(db.Unicode(50), nullable=True)

#     employees = db.relationship('Employee')
#     contacts = db.relationship('Contact')
#     addresses = db.relationship('Address')

#     def __repr__(self):
#         """Provide helpful representation when printed."""

#         return "<Employee employee_id=%s first_name=%s>" %(self.employee_id, self.first_name)


### Optional information formatting tables (nickname, contact, phone)


# class Contact(db.Model):
#     """A table that saves contacts."""

#     __tablename__ = "contacts"

#     contact_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     conntry_code = db.Column(db.String, nullable=True)
#     area_code = db.Column(db.Integer, nullable=True)
#     number = db.Column(db.Integer, nullable=True)
#     ## make the form separate the ara codes, and then receive collected input
#     mobile = db.Column(db.Integer, nullable=True)
#     k_country_code = db.Column(db.Integer, nullable=True)
#     k_phone = db.Column(db.Integer, nullable=True)
#     k_mobile = db.Column(db.Integer, nullable=True)
#     email = db.Column(db.Unicode(50), nullable=True)
#     Fax = db.Column(db.Integer, nullable=True)

# #     offices = db.relationship('Office')
# #     emergency_contact_people = db.relationship('Emergency_contact_person')
# #     employee_phones = db.relationship('Employee_phone')

#     def __repr__(self):
#         """Provide helpful representation when printed."""

#         return "<Contact contact_id=%s email=%s>" %(self.contact_id, self.email)


# class Address(db.Model):
#     """Offices around the globe."""

#     __tablename__ = "addresses"

#     id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     street_number = db.Column(db.Integer, nullable=True)
#     address_1st_line = db.Column(db.String(50), nullable=True)
#     address_2nd_line = db.Column(db.String(50), nullable=True)
#     country = db.Column(db.String(50), nullable=True)

#     offices = db.relationship('Office')
#     employee = db.relationship('Employee')
#     emergency_contact_person = db.relationship('Emergency_contact_person')


#     def __repr__(self):
#         """Provide helpful representation when printed."""

#         return "<Employee employee_id=%s first_name=%s>" %(self.employee_id, self.first_name)


# ### Office/Company/Title/Department definitions


# class Office(db.Model):
#     """Offices around the globe."""

#     __tablename__ = "offices"

#     office_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     name = db.Column(db.String(50))

#     Employee_dept_office = db.relationship('Employee_dept_office')
#     contacts = db.relationship('Contact')
#     address = db.relationship('Address')
#     compnay_offices = db.relationship('Office_department')
#     company = db.relationship('Company')


#     def __repr__(self):
#         """Provide helpful representation when printed."""

#         return "<Employee employee_id=%s first_name=%s>" %(self.employee_id, self.first_name)



# class Company(db.Model):
#     """Offices around the globe."""

#     __tablename__ = "companies"

#     id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     name = db.Column(db.String(50), nullable=True)
#     shrot_name = db.Column(db.String(50), nullable=True)

#     Employee_dept_office = db.relationship('Employee_dept_office')
#     offices = db.relationship('Office')


#     def __repr__(self):
#         """Provide helpful representation when printed."""

#         return "<Employee employee_id=%s first_name=%s>" %(self.employee_id, self.first_name)



# class Title(db.Model):
#     """Offices around the globe."""

#     __tablename__ = "titles"

#     id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     title = db.Column(db.String(50), nullable=True)
#     k_title = db.Column(db.Unicode(50), nullable=True)

#     department_titles = db.relationship('Department_title')
#     Employee_dept_office = db.relationship('Employee_dept_office')


#     def __repr__(self):
#         """Provide helpful representation when printed."""

#         return "<Employee employee_id=%s first_name=%s>" %(self.employee_id, self.first_name)



# class Department(db.Model):
#     """Offices around the globe."""

#     __tablename__ = "departments"

#     id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     name = db.Column(db.String(50), nullable=True)

#     Employee_dept_office = db.relationship('Employee_dept_office')
#     department_titles = db.relationship('Department_title')
#     compnay_offices = db.relationship('Office_department')


#     def __repr__(self):
#         """Provide helpful representation when printed."""

#         return "<Employee employee_id=%s first_name=%s>" %(self.employee_id, self.first_name)



# ### Company association and middle tables


# class Employee_dept_office(db.Model):
#     """Middle table between employee, dept, office."""

#     __tablename__ = "Employee_dept_offices"

#     id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     job_description = db.Column(db.TEXT, nullable=True)
#     date_employeed = db.Column(db.DateTime, nullable=True)
#     date_departed = db.Column(db.DateTime, nullable=True)

#     employee = db.relationship('Employee')
#     title = db.relationship('Title')
#     office = db.relationship('Office')
#     company = db.relationship('Company')
#     department = db.relationship('Department')


#     def __repr__(self):
#         """Provide helpful representation when printed."""

#         return "<Employee employee_id=%s first_name=%s>" %(self.employee_id, self.first_name)


# class Department_title(db.Model):
#     """Middle table between department and title."""

#     __tablename__ = "department_titles"

#     id = db.Column(db.Integer, autoincrement=True, primary_key=True)

#     title = db.relationship('Title')
#     department = db.relationship('Department')


#     def __repr__(self):
#         """Provide helpful representation when printed."""

#         return "<Employee employee_id=%s first_name=%s>" %(self.employee_id, self.first_name)


# class Office_department(db.Model):
#     """Middle table between office and department."""

#     __tablename__ = "office_departments"

#     id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    
#     department = db.relationship('Department')
#     office = db.relationship('Office')


#     def __repr__(self):
#         """Provide helpful representation when printed."""

#         return "<Employee employee_id=%s first_name=%s>" %(self.employee_id, self.first_name)


### TODO ###
# # Build a log-in feature
# class Login(db.Model):
#    """Offices around the globe."""

#     __tablename__ = "offices"

#     id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     type = db.Column(db.unicode)
#     email = db.Column(db.unicode)
#     password = db.Column(db.unicode)

#     customers = db.relationship('Customer')
#     employees = db.relationship(Employee)


    # def __repr__(self):
    # """Provide helpful representation when printed."""

    # return "<Employee employee_id=%s first_name=%s>" 
    #                                     %(self.employee_id, self.first_name)



### TODO ###
# # Build customer log-in features
# class Customer(db.Model):
#    """Customer log-in."""

#     __tablename__ = "offices"

#     id = db.Column(db.Integer, autoincrement=True, primary_key=True)

#     login = db.relationship('Login')

# db.bind("postgres", host="", user="", password="", database="")
# db.generate_mapping(create_tables=True)


    # def __repr__(self):
    # """Provide helpful representation when printed."""

    # return "<Employee employee_id=%s first_name=%s>" 
    #                                     %(self.employee_id, self.first_name)


# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///intranet'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
