""" Database model file

* Data Model
Employee table's id is Nickname, K_contact, Emergency_contact's Foreign Primary Key
Employee_department table connects Employee to Title and Company
Employee_department - Title  - Department_title - Department - Company_department - Company
Employee_department - Title  - Department_title - Department - Office_department - Office

* General Naming Guide
Table primary key name: tablename_id
Middle/association table name: table1name_table2name
Middle/association table primary key name: id
Order: fields, foreign key (id) fields, relations, repr function

* Construction
Middle/association tables have foreign keys and relationships
Other tables have relationships
No back references were used

"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Connection to the PostgreSQL database comes through the Flask-SQLAlchemy
db = SQLAlchemy()


### TODO: Use regx to enforce formatting
class Employee(db.Model):
    """Employee of the group."""

    __tablename__ = "employees"

    employee_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    photo_URL = db.Column(db.String(100))
    birthyear = db.Column(db.DateTime)
    birthday = db.Column(db.DateTime)
    personal_email = db.Column(db.String(100))
    first_name = db.Column(db.String(50))
    mid_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    country_code = db.Column(db.Integer)
    phone = db.Column(db.Integer)
    mobile = db.Column(db.Integer)
    address_1st_line = db.Column(db.String(50))
    address_2nd_line = db.Column(db.String(50))
    country = db.Column(db.String(50))
    postal_code = db.Column(db.Integer)
    fax = db.Column(db.Integer)
    comment = db.Column(db.String(50))

    # Relations
    nicknames = db.relationship('Nickname')
    emergency_contacts = db.relationship('Emergency_contact')
    k_contacts = db.relationship('K_contact')
    employee_departments = db.relationship('Employee_department')
    
    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Employee employee_id=%s first_name=%s>" %(self.employee_id, self.first_name)

# TODO: into employee table

### FIXME: unicode problem in seed.py & model.py -> after, try seeding db
class Nickname(db.Model):
    """Nickname for a person."""

    __tablename__ = "nicknames"

    # one to one relationship to employee: OK for a ForeignKey as primary key
    # nickname_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    nickname_id = db.Column(db.Integer, db.ForeignKey('employees.employee_id'), primary_key=True)
    nickname = db.Column(db.Unicode(50))
    k_name = db.Column(db.Unicode(50))
    kanji_name = db.Column(db.Unicode(50))

    employees = db.relationship('Employee')

    def __repr__(self):
        return "<Nickname nickname_id=%s>" %self.nickname_id
# TODO: into employee table


class Emergency_contact(db.Model):
    """Emergency contact for an employee."""

    __tablename__ = "emergency_contacts"

    emergency_conatact_id = db.Column(db.Integer, db.ForeignKey('employees.employee_id'), primary_key=True)
    emergency_name = db.Column(db.Unicode(50))
    emergency_phone = db.Column(db.Integer)
    emergency_comment = db.Column(db.String(100))

    employees = db.relationship('Employee')

    def __repr__(self):
        return "<Emergency_contact emergency_conatact_id=%s>" %self.emergency_conatact_id

# TODO: into employee table

class K_contact(db.Model):
    """A table that saves contacts."""

    __tablename__ = "k_contacts"

    k_contact_id = db.Column(db.Integer, db.ForeignKey('employees.employee_id'), primary_key=True)
    k_country_code = db.Column(db.Integer)
    k_phone = db.Column(db.Integer)
    k_mobile = db.Column(db.Integer)
    k_address_1st_line = db.Column(db.String(50))
    k_address_2nd_line = db.Column(db.String(50))
    k_country = db.Column(db.String(50))
    k_postal_code = db.Column(db.Integer)
    k_email = db.Column(db.String(50))
    k_fax = db.Column(db.Integer)
    k_comment = db.Column(db.Unicode(50))

    employees = db.relationship('Employee')

    def __repr__(self):
        return "<K_contact k_contact_id=%s>" %self.k_contact_id


class Employee_department(db.Model):
    """Middle table between employee, dept, office."""

    __tablename__ = "Employee_departments"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    job_description = db.Column(db.TEXT)
    date_employeed = db.Column(db.DateTime)
    date_departed = db.Column(db.DateTime)
    email = db.Column(db.Unicode(50))
    email_password = db.Column(db.Integer)
    pc = db.Column(db.String(50))
    pc_password = db.Column(db.String(50))
    phone = db.Column(db.Integer)
    comment = db.Column(db.String(50))

    employee_id = db.Column(db.Integer, db.ForeignKey('employees.employee_id'))
    title_id = db.Column(db.Integer, db.ForeignKey('titles.title_id'))
    office_id = db.Column(db.Integer, db.ForeignKey('offices.office_id'))
    company_id = db.Column(db.Integer, db.ForeignKey('companies.company_id'))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.department_id'))

    employees = db.relationship('Employee')
    titles = db.relationship('Title')
    offices = db.relationship('Office')
    companies = db.relationship('Company')
    departments = db.relationship('Department')

    def __repr__(self):
        return "<Employee_department id=%s>" %self.id

class Title(db.Model):
    """Offices around the globe."""

    __tablename__ = "titles"

    title_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(50))
    k_title = db.Column(db.Unicode(50))

    employee_departments = db.relationship('Employee_department')
    department_titles = db.relationship('Department_title')

    def __repr__(self):
        return "<Title title_id=%s>" %self.title_id


class Department_title(db.Model):
    """Middle table between department and title."""

    __tablename__ = "department_titles"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    title_id = db.Column(db.Integer, db.ForeignKey('titles.title_id'))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.department_id'))

    titles = db.relationship('Title')
    departments = db.relationship('Department')

    def __repr__(self):
        return "<Department_title id=%s>" %self.id


class Department(db.Model):
    """Offices around the globe."""

    __tablename__ = "departments"

    department_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    department_name = db.Column(db.String(50))

    department_titles = db.relationship('Department_title')
    office_departments = db.relationship('Office_department')
    company_departments = db.relationship('Company_department')

    def __repr__(self):
        return "<Department department_id=%s>" %self.department_id


class Company_department(db.Model):
    """Middle table between company and department."""

    __tablename__ = "company_departments"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    
    department_id = db.Column(db.Integer, db.ForeignKey('departments.department_id'))
    company_id = db.Column(db.Integer, db.ForeignKey('companies.company_id'))    

    departments = db.relationship('Department')
    companies = db.relationship('Company')

    def __repr__(self):
        return "<Company_department id=%s>" %self.id


class Company(db.Model):
    """All subsidiaries around the globe."""

    __tablename__ = "companies"

    company_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    company_name = db.Column(db.String(50))
    shrot_name = db.Column(db.String(50))

    employee_departments = db.relationship('Employee_department')
    company_departments = db.relationship('Company_department')

    def __repr__(self):
        return "<Company company_id=%s>" %self.company_id


class Office_department(db.Model):
    """Middle table between office and department."""

    __tablename__ = "office_departments"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    department_id = db.Column(db.Integer, db.ForeignKey('departments.department_id'))
    office_id = db.Column(db.Integer, db.ForeignKey('offices.office_id'))
    
    departments = db.relationship('Department')
    offices = db.relationship('Office')

    def __repr__(self):
        return "<Office_department id=%s>" %self.id


class Office(db.Model):
    """Offices around the globe."""

    __tablename__ = "offices"

    office_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    office_name = db.Column(db.String(50))
    c_country_code = db.Column(db.Integer)
    c_phone = db.Column(db.Integer)
    c_mobile = db.Column(db.Integer)
    c_address_1st_line = db.Column(db.String(50))
    c_address_2nd_line = db.Column(db.String(50))
    c_country = db.Column(db.String(50))
    c_postal_code = db.Column(db.Integer)
    c_fax = db.Column(db.Integer)
    c_comment = db.Column(db.String(50))

    office_departments = db.relationship('Office_department')

    def __repr__(self):
        return "<Office office_id=%s>" %self.office_id


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
    