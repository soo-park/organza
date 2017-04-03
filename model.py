""" Database model file

* Data Model
employee_company table connects Employee to Title and Company
employee_company - Title  - Department_title - Department - Company_department - Company
employee_company - Title  - Department_title - Department - Office_department - Office

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
    photo_URL = db.Column(db.String(1000))
    birthday = db.Column(db.DateTime)
    personal_email = db.Column(db.String(100))
    first_name = db.Column(db.String(50))
    mid_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
### FIXME: unicode problem in seed.py & model.py -> after, try seeding db
    nickname = db.Column(db.Unicode(50))
    k_name = db.Column(db.Unicode(50))
    kanji_name = db.Column(db.Unicode(50))
    phone = db.Column(db.Integer)
    mobile = db.Column(db.Integer)
    address_line1 = db.Column(db.String(50))
    address_line2 = db.Column(db.String(50))
    city = db.Column(db.String(30))
    country = db.Column(db.String(50))
    postal_code = db.Column(db.Integer)
    emergency_name = db.Column(db.Unicode(50))
    emergency_phone = db.Column(db.Integer)

    # Relations
    employee_companies = db.relationship('Employee_company')
    
    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Employee employee_id=%s first_name=%s>" %(self.employee_id, self.first_name)


class Employee_company(db.Model):
    """Middle table between employee, dept, office."""

    __tablename__ = "employee_companies"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    office_email = db.Column(db.Unicode(50))
    password = db.Column(db.Integer)
    date_employeed = db.Column(db.DateTime)
    date_departed = db.Column(db.DateTime)
    job_description = db.Column(db.String(200))
    office_phone = db.Column(db.Integer)

    employee_id = db.Column(db.Integer, db.ForeignKey('employees.employee_id'))
    title_id = db.Column(db.Integer, db.ForeignKey('titles.title_id'))
    company_id = db.Column(db.Integer, db.ForeignKey('companies.company_id'))

    employees = db.relationship('Employee')
    titles = db.relationship('Title')
    companies = db.relationship('Company')

    def __repr__(self):
        return "<employee_company id=%s>" %self.id


class Title(db.Model):
    """Offices around the globe."""

    __tablename__ = "titles"

    title_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(50))
    k_title = db.Column(db.Unicode(50))

    employee_companies = db.relationship('Employee_company')
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
    name = db.Column(db.String(50))
    doing_business_as = db.Column(db.String(50))
    abbreviation = db.Column(db.String(50))

    employee_companies = db.relationship('Employee_company')
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
    name = db.Column(db.String(50))
    phone = db.Column(db.Integer)
    address_line1 = db.Column(db.String(50))
    address_line2 = db.Column(db.String(50))
    city = db.Column(db.String(30))
    country = db.Column(db.String(50))
    postal_code = db.Column(db.Integer)
    fax = db.Column(db.Integer)

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
    