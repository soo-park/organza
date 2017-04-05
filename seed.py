""" Utility code to seed hardcode data into the intranet database
dropdb intranet; createdb intranet; python model.py before running this code
"""

import datetime
from sqlalchemy import func

from model import (Employee, Employee_company, Company, Department, 
                   Title, Company_department, Office, Department_title,
                   Office_department, connect_to_db, db)
from server import app

# TODO: find a way to drop and create the table from SQLAlchemy

def load_employees():
    """Load employees from u.employee into database."""

    print "\nemployees seeding"

    for i, row in enumerate(open("seed_data/u.employee")):
        row = row.rstrip()
        (employee_id, photo_url, birthday, personal_email,
            first_name, mid_name, last_name, nickname, k_name,
            kanji_name, phone, mobile, address_line1,
            address_line2, city, state, country,
            postal_code, emergency_name, emergency_phone
            ) = row.split("|")

        employee = Employee(employee_id=employee_id,
                            photo_url=photo_url,
                            birthday=birthday,
                            personal_email=personal_email,
                            first_name=first_name,
                            mid_name=mid_name,
                            last_name=last_name,
                            nickname=unicode(nickname),
                            k_name=unicode(k_name),
                            kanji_name=unicode(kanji_name),
                            phone=unicode(phone),
                            mobile=unicode(mobile),
                            address_line1=unicode(address_line1),
                            address_line2=unicode(address_line2),
                            city=city,
                            state=state,
                            country=country,
                            postal_code=postal_code,
                            emergency_name=unicode(emergency_name),
                            emergency_phone=emergency_phone)

        # We need to add to the session or it won't ever be stored
        db.session.add(employee)

    # Once we're done, we should commit our work
    db.session.commit()
    print "employees seeding completed.\n"


def load_companies():
    """Load companies from u.item into database."""

    print "companies"

    for i, row in enumerate(open("seed_data/u.company")):
        row = row.rstrip()

        # clever -- we can unpack part of the row!
        company_id, name, dba, short_name = row.split("|")

        company = Company(company_id=company_id,
                          name=name,
                          dba=dba,
                          short_name=short_name)

        db.session.add(company)

    db.session.commit()
    print "companies seeding completed.\n"


def load_department():

    print "department seeding"
    for i, row in enumerate(open("seed_data/u.department")):
        row = row.rstrip()

        department_id, name = row.split("|")

        department = Department(department_id=department_id,
                                name=name
                                )

        db.session.add(department)

    db.session.commit()
    print "department seeding completed.\n"


def load_title():

    print "title seeding"
    for i, row in enumerate(open("seed_data/u.title")):
        row = row.rstrip()

        title_id, title, k_title = row.split("|")

        title = Title(title_id=title_id,
                      title=title,
                      k_title=unicode(k_title)
                                )

        db.session.add(title)

    db.session.commit()
    print "title seeding completed.\n"


def load_office():

    print "office seeding"
    for i, row in enumerate(open("seed_data/u.office")):
        row = row.rstrip()

        (office_id, name, phone, address_line1, address_line2,
        city, state, country, postal_code, fax) = row.split("|")

        office = Office(office_id=office_id,
                        name=name,
                        phone=unicode(phone),
                        address_line1=unicode(address_line1), 
                        address_line2=unicode(address_line2),
                        city=city,
                        state=state,
                        country=country,
                        postal_code=postal_code,
                        fax=unicode(fax)
                        )

        db.session.add(office)

    db.session.commit()
    print "office seeding completed.\n"


def load_employee_companies():
    """Load employee_companies from u.data into database."""

    print "employee_companies"

    for i, row in enumerate(open("seed_data/u.data")):
        row = row.rstrip()

        (employee_company_id, office_email, password, 
         date_employeed, date_departed, job_description,
         office_phone, employee_id, company_id, 
        ) = row.split("|")

        employee_company_id = int(employee_company_id)
        employee_id = int(employee_id)
        company_id = int(company_id)

        employee_company = Employee_company(employee_company_id=employee_company_id,
                                            office_email=office_email,
                                            password=password,
                                            date_employeed=date_employeed,
                                            date_departed=date_departed,
                                            job_description=job_description,
                                            office_phone=unicode(office_phone), 
                                            employee_id=employee_id,
                                            company_id=company_id
                                            )

        db.session.add(employee_company)

        if i%1000 == 0:
            # An optimization: if we commit after every add, the database
            # will do a lot of work committing each record. However, if we
            # wait until the end, on computers with smaller amounts of
            # memory, it might thrash around. By committing every 1,000th
            # add, we'll strike a good balance.
            db.session.commit()
            print i*1000

    # commit whatever is left
    db.session.commit()
    print "employee_company seeding completed\n"


def load_company_department():

    print "company_department seeding"
    for i, row in enumerate(open("seed_data/u.company_department")):
        row = row.rstrip()

        company_department_id, department_id, company_id = row.split("|")

        company_department = Company_department(company_department_id=company_department_id,
                                                department_id=department_id,
                                                company_id=company_id
                                                )

        db.session.add(company_department)

    db.session.commit()
    print "company_department seeding completed.\n"


def load_department_title():

    print "department_title seeding"
    for i, row in enumerate(open("seed_data/u.department_title")):
        row = row.rstrip()

        department_title_id, title_id, department_id = row.split("|")

        department_title = Department_title(department_title_id=department_title_id,
                                            title_id=title_id,
                                            department_id=department_id
                                            )

        db.session.add(department_title)

    db.session.commit()
    print "department_title seeding completed.\n"


def load_office_department():

    print "office_department seeding"
    for i, row in enumerate(open("seed_data/u.office_department")):
        row = row.rstrip()

        office_department_id, department_id, office_id = row.split("|")

        office_department = Office_department(office_department_id=office_department_id,
                                              department_id=department_id,
                                              office_id=office_id
                                              )

        db.session.add(office_department)

    db.session.commit()
    print "office_department seeding completed.\n"


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    load_employees()
    load_companies()
    load_department()
    load_title()
    load_office()
    load_employee_companies()
    load_company_department()
    load_department_title()
    load_office_department()