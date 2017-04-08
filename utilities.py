# -*- coding: utf-8 -*-
# Line one is necessary to have utf-8 recognized
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from jinja2 import StrictUndefined
from flask import (Flask, jsonify, render_template, request, flash, redirect,
                   session)
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy import func
from server import app

import os
import datetime

# import employee related models
from model import Employee, Employee_company, Company, connect_to_db, db


## TODO: Build a function for importing Excel (below code imports one cell)
def import_Excel():
    import openpyxl
    from openpyxl import load_workbook
    wb = load_workbook(filename = 'static/doc/employee.xlsx')
    sheet_ranges = wb['test'] #use the workbook tab name
    print(sheet_ranges['A2'].value)


def set_val_employee_id():
    """Set value for the next employee_id after seeding database"""

    # Get the Max employee_id in the database
    result = db.session.query(func.max(Employee.employee_id)).one()
    max_id = int(result[0])

    # Set the value for the next employee_id to be max_id + 1
    query = "SELECT setval('employees_employee_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    import_Excel()
    set_val_employee_id()


def get_map_from_sqlalchemy(a_object):

    result = {}

    # # this can be done at the front-end side using node.js and JS
    # # if the programming was done at the front-end
    # from sqlalchemy import inspect
    print a_object
    # for a_object in objects:

    #     # A code to let you see all the attributes usable for the item
    #     print "\nObject", a_object
    #     inst = inspect(a_object)
    #     attr_names = [c_attr.key for c_attr in inst.mapper.column_attrs]
        
    #     for i in attr_names:
    #         result[i] = "testing"

    return a_object

