"""Models and database functions for intranet project.
Skeleton codes generated with stacks from Hackbright.
"""

from flask_sqlalchemy import SQLAlchemy
import correlation
from datetime import datetime

# Connection to the PostgreSQL database comes through the Flask-SQLAlchemy
# helper library. There is a `session` object, where interactions are done.
db = SQLAlchemy()


##############################################################################
# Employee definitions

class Employee(db.Model):
    """Employee of the group."""

    __tablename__ = "employees"

    employee_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String(20))
    mid_name = db.Column(db.String(20), nullable=True)
    last_name = db.Column(db.String(20))
    ### TODO ###
    # if the personal email is nullable, 
    # and the office email belongs to the form
    # how are you going to log-in and authentificate?
    personal_email = db.Column(db.String(20), nullable=True)
    photo_URL = db.Column(db.String(1000), nullable=True)
    birthyear = db.Column(db.Datetime, nullable=True)
    birthday = db.Column(db.Datetime, nullable=True)

    ### TODO ###
    # Figure out what kind of relationship is good
    nickname = Relationship('Nickname', nullable=True)
    home_addresses = Relationship('Address', nullable=True)
    employee_phones = Relationship('Employee_phone', nullable=True)
    Employee_dept_office = Relationship('Employee_dept_office')
    emergency_contact_person = Relationship('Emergency_contact_person', nullable=True)
    
    ### TODO ###
    # A field that wil be feeding off of email for the employee?
    # Generate the log_in table?
    # login = Required('Login')


    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Employee employee_id=%s first_name=%s>" 
                                            %(self.employee_id, self.first_name)


class Nickname(db.Entity):
   """Offices around the globe."""

    __tablename__ = "nicknames"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    k_first_name = db.Column(db.Unicode(50), nullable=True)
    k_last_name = db.Column(db.Unicode(50), nullable=True)
    nickname = db.Column(db.Unicode(50), nullable=True)
    kanji_name = db.Column(db.Unicode(50), nullable=True)

    employee = Relationship(Employee)

    def __repr__(self):
    """Provide helpful representation when printed."""

    return "<Employee employee_id=%s first_name=%s>" 
                                        %(self.employee_id, self.first_name)


##############################################################################
# Employee association and middle tables


class Employee_phone(db.Entity):
   """Offices around the globe."""

    __tablename__ = "offices"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    employee = Relationship(Employee)
    contact = Relationship(Contact)



    def __repr__(self):
    """Provide helpful representation when printed."""

    return "<Employee employee_id=%s first_name=%s>" 
                                        %(self.employee_id, self.first_name)



class Emergency_contact_person(db.Entity):
   """Offices around the globe."""

    __tablename__ = "offices"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.Unicode(50), nullable=True)

    employee = Relationship(Employee)
    contacts = Relationship(Contact)
    addresses = Relationship(Address)


    def __repr__(self):
    """Provide helpful representation when printed."""

    return "<Employee employee_id=%s first_name=%s>" 
                                        %(self.employee_id, self.first_name)


##############################################################################
# Optional information formatting tables (nickname, contact, phone)


class Contact(db.Entity):
   """Offices around the globe."""

    __tablename__ = "offices"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    conntry_code = db.Column(db.String, nullable=True)
    area_code = db.Column(db.Integer, nullable=True)
    number = db.Column(db.Integer, nullable=True)
    ## make the form separate the ara codes, and then receive collected input
    mobile = db.Column(db.Integer, nullable=True)
    k_country_code = db.Column(db.Integer, nullable=True)
    k_phone = db.Column(db.Integer, nullable=True)
    k_mobile = db.Column(db.Integer, nullable=True)
    email = db.Column(db.Unicode(50), nullable=True)
    Fax = db.Column(db.Integer, nullable=True)

    office = Required(Office)
    emergency_contact_person = Relationship('Emergency_contact_person')
    employee_phones = Relationship('Employee_phone')


    def __repr__(self):
    """Provide helpful representation when printed."""

    return "<Employee employee_id=%s first_name=%s>" 
                                        %(self.employee_id, self.first_name)



class Address(db.Entity):
   """Offices around the globe."""

    __tablename__ = "offices"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    street_number = db.Column(db.Integer, nullable=True)
    address_1st_line = db.Column(db.String(50), nullable=True)
    address_2nd_line = db.Column(db.String(50), nullable=True)
    country = db.Column(db.String(50), nullable=True)

    offices = Relationship(Office)
    employee = Relationship(Employee)
    emergency_contact_person = Relationship('Emergency_contact_person')


    def __repr__(self):
    """Provide helpful representation when printed."""

    return "<Employee employee_id=%s first_name=%s>" 
                                        %(self.employee_id, self.first_name)


##############################################################################
# Office/Company/Title/Department definitions


class Office(db.Model):
    """Offices around the globe."""

    __tablename__ = "offices"

    office_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(50))

    Employee_dept_office = Relationship('Employee_dept_office')
    contacts = Relationship('Contact')
    address = Relationship('Address')
    compnay_offices = Relationship('Office_department')
    company = Relationship('Company')


    def __repr__(self):
    """Provide helpful representation when printed."""

    return "<Employee employee_id=%s first_name=%s>" 
                                        %(self.employee_id, self.first_name)



class Company(db.Entity):
    """Offices around the globe."""

    __tablename__ = "companies"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    shrot_name = db.Column(db.String(50), nullable=True)

    Employee_dept_office = Relationship('Employee_dept_office')
    offices = Relationship(Office)


    def __repr__(self):
    """Provide helpful representation when printed."""

    return "<Employee employee_id=%s first_name=%s>" 
                                        %(self.employee_id, self.first_name)



class Title(db.Entity):
   """Offices around the globe."""

    __tablename__ = "titles"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(50), nullable=True)
    k_title = db.Column(db.Unicode(50), nullable=True)
    department_titles = Relationship('Department_title')
    Employee_dept_office = Relationship('Employee_dept_office')


    def __repr__(self):
    """Provide helpful representation when printed."""

    return "<Employee employee_id=%s first_name=%s>" 
                                        %(self.employee_id, self.first_name)



class Department(db.Entity):
   """Offices around the globe."""

    __tablename__ = "departments"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(50), nullable=True)

    Employee_dept_office = Relationship(Employee_dept_office)
    department_titles = Relationship('Department_title')
    compnay_offices = Relationship('Office_department')


    def __repr__(self):
    """Provide helpful representation when printed."""

    return "<Employee employee_id=%s first_name=%s>" 
                                        %(self.employee_id, self.first_name)



##############################################################################
# Company association and middle tables


class Employee_dept_office(db.Entity):
   """Offices around the globe."""

    __tablename__ = "Employee_dept_offices"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    job_description = db.Column(db.unicode, nullable=True)
    date_employeed = db.Column(db.unicode, nullable=True)
    date_departed = db.Column(db.unicode, nullable=True)

    employee = Relationship(Employee)
    title = Relationship(Title)
    office = Relationship(Office)
    company = Relationship(Company)
    department = Relationship('Department')


    def __repr__(self):
    """Provide helpful representation when printed."""

    return "<Employee employee_id=%s first_name=%s>" 
                                        %(self.employee_id, self.first_name)


class Department_title(db.Entity):
   """Offices around the globe."""

    __tablename__ = "offices"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    title = Relationship(Title)
    department = Relationship(Department)


    def __repr__(self):
    """Provide helpful representation when printed."""

    return "<Employee employee_id=%s first_name=%s>" 
                                        %(self.employee_id, self.first_name)



class Office_department(db.Entity):
   """Offices around the globe."""

    __tablename__ = "offices"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    
    department = Relationship(Department)
    office = Relationship(Office)


    def __repr__(self):
    """Provide helpful representation when printed."""

    return "<Employee employee_id=%s first_name=%s>" 
                                        %(self.employee_id, self.first_name)



### TODO ###
# # Build a log-in feature
# class Login(db.Entity):
#    """Offices around the globe."""

#     __tablename__ = "offices"

#     id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     type = db.Column(db.unicode)
#     email = db.Column(db.unicode)
#     password = db.Column(db.unicode)

#     customers = Relationship('Customer')
#     employees = Relationship(Employee)


    # def __repr__(self):
    # """Provide helpful representation when printed."""

    # return "<Employee employee_id=%s first_name=%s>" 
    #                                     %(self.employee_id, self.first_name)



### TODO ###
# # Build customer log-in features
# class Customer(db.Entity):
#    """Customer log-in."""

#     __tablename__ = "offices"

#     id = db.Column(db.Integer, autoincrement=True, primary_key=True)

#     login = Relationship('Login')

# db.bind("postgres", host="", user="", password="", database="")
# db.generate_mapping(create_tables=True)


    # def __repr__(self):
    # """Provide helpful representation when printed."""

    # return "<Employee employee_id=%s first_name=%s>" 
    #                                     %(self.employee_id, self.first_name)



##############################################################################
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
