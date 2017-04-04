# -*- coding: utf-8 -*-
# Line one is necessary to have utf-8 recognized
import sys
reload(sys)
sys.setdefaultencoding('utf8')

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
    birthday = db.Column(db.DateTime)
    personal_email = db.Column(db.String(100))
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50))
    k_name = db.Column(db.Unicode(50))

    # Relations
    employee_companies = db.relationship('Employee_company')
    
    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Employee employee_id=%s first_name=%s>" %(self.employee_id, self.first_name)


    ### TODO: Build a function for importing Excel (below code imports one cell)
    # def import_Excel():
        # import openpyxl
        # from openpyxl import load_workbook
        # wb = load_workbook(filename = 'static/doc/employee.xlsx')
        # sheet_ranges = wb['test'] #use the workbook tab name
        # print(sheet_ranges['A2'].value)


class Employee_company(db.Model):
    """Middle table between employee, dept, office."""

    __tablename__ = "employee_companies"

    employee_company_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    office_email = db.Column(db.String(50))
    password = db.Column(db.String(50))

    employee_id = db.Column(db.Integer, db.ForeignKey('employees.employee_id'))
    company_id = db.Column(db.Integer, db.ForeignKey('companies.company_id'))

    employees = db.relationship('Employee')
    companies = db.relationship('Company')

    def __repr__(self):
        return "<employee_company employee_company_id=%s>" %self.employee_company_id


class Company(db.Model):
    """All subsidiaries around the globe."""

    __tablename__ = "companies"

    company_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(50))

    employee_companies = db.relationship('Employee_company')

    def __repr__(self):
        return "<Company company_id=%s>" %self.company_id


# Helper functions

def connect_to_db(app):

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///intranet'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":

    from server import app
    connect_to_db(app)
    print "Connected to DB."