""" Utility code to seed hardcode data into the intranet database
dropdb intranet; createdb intranet; python model.py before running this code
"""

import datetime
from sqlalchemy import func

from model import (Employee, Employee_company, Company, Department, 
                   Title, Company_department, Office, Department_title,
                   Office_department, connect_to_db, db)
from server import app

# TODO: put seed.py into NOT_FOR_DEPLOYMENT/seed_data folder and test the code
def purge_db():
    """Delete all data from the intranet and recreate"""

    db.drop_all()
    db.create_all()


def load_employees():
    """Load employees from u.employee into database."""

    print "\nemployees seeding"

    for i, row in enumerate(open("NOT_FOR_DEPLOYMENT/seed_data/u.employee")):

        # Because there are datetime objects, the empty string will throw an error
        # Thus, it is necessary to make things None when seeding to prevent the error
        # Strings and integers will now throw any error
        row = row.rstrip().split("|")
        for j, k in enumerate(row):
            if k == '':
                row[j] = None

        # TODO: id is not needed for the seed base file, because it auto increments
        (employee_id, photo_url, birthday, personal_email,
            first_name, mid_name, last_name, username, password,
            k_name, kanji_name, phone, mobile, address,
            country_code, city, state, country,
            postal_code, emergency_name, emergency_phone, admin
            ) = row

        employee = Employee(
                            photo_url=unicode(photo_url),
                            birthday=birthday,
                            personal_email=personal_email,
                            first_name=unicode(first_name),
                            mid_name=unicode(mid_name),
                            last_name=unicode(last_name),
                            username=username,
                            password=password,
                            k_name=unicode(k_name),
                            kanji_name=unicode(kanji_name),
                            phone=unicode(phone),
                            mobile=unicode(mobile),
                            address=unicode(address),
                            country_code=unicode(country_code),
                            city=unicode(city),
                            state=unicode(state),
                            country=unicode(country),
                            postal_code=unicode(postal_code),
                            emergency_name=unicode(emergency_name),
                            emergency_phone=unicode(emergency_phone),
                            admin=admin
                            )

        # We need to add to the session or it won't ever be stored
        db.session.add(employee)
        if i%1000 == 0:
            # An optimization: if we commit after every add, the database
            # will do a lot of work committing each record. However, if we
            # wait until the end, on computers with smaller amounts of
            # memory, it might thrash around. By committing every 1,000th
            # add, we'll strike a good balance.
            db.session.commit()
            print i*1000, 'employees added'

    # Once we're done, we should commit our work
    db.session.commit()
    print "employees seeding completed.\n"


def load_companies():
    """Load companies from u.item into database."""

    print "companies"

    for i, row in enumerate(open("NOT_FOR_DEPLOYMENT/seed_data/u.company")):
        row = row.rstrip()

        # clever -- we can unpack part of the row!
        company_id, company_name, short_name = row.split("|")

        company = Company(
                          company_name=unicode(company_name),
                          short_name=unicode(short_name)
                          )

        db.session.add(company)

    db.session.commit()
    print "companies seeding completed.\n"


def load_department():

    print "department seeding"
    for i, row in enumerate(open("NOT_FOR_DEPLOYMENT/seed_data/u.department")):
        row = row.rstrip()

        department_id, department_name = row.split("|")

        department = Department(
                                department_name=unicode(department_name)
                                )

        db.session.add(department)

    db.session.commit()
    print "department seeding completed.\n"


def load_title():

    print "title seeding"
    for i, row in enumerate(open("NOT_FOR_DEPLOYMENT/seed_data/u.title")):
        row = row.rstrip()

        title_id, title, k_title = row.split("|")

        title = Title(
                      title=unicode(title),
                      k_title=unicode(k_title)
                     )

        db.session.add(title)

    db.session.commit()
    print "title seeding completed.\n"


def load_office():

    print "office seeding"
    for i, row in enumerate(open("NOT_FOR_DEPLOYMENT/seed_data/u.office")):
        row = row.rstrip()

        (office_id, office_name, phone, address, country_code,
        city, state, country, postal_code, fax) = row.split("|")

        office = Office(
                        office_name=unicode(office_name),
                        phone=unicode(phone),
                        address=unicode(address), 
                        country_code=unicode(country_code),
                        city=unicode(city),
                        state=unicode(state),
                        country=unicode(country),
                        postal_code=unicode(postal_code),
                        fax=unicode(fax)
                        )

        db.session.add(office)

    db.session.commit()
    print "office seeding completed.\n"


def load_employee_companies():
    """Load employee_companies from u.employee_company into database."""

    print "employee_companies"

    for i, row in enumerate(open("NOT_FOR_DEPLOYMENT/seed_data/u.employee_company")):
        row = row.rstrip().split("|")

        for j, k in enumerate(row):
            if k == '':
                row[j] = None

        (employee_company_id, office_email, password, 
         date_employeed, date_departed, job_description,
         office_phone, employee_id, company_id, title_id 
        ) = row

        employee_company_id = int(employee_company_id)
        employee_id = int(employee_id)
        company_id = int(company_id)

        employee_company = Employee_company(
                                            office_email=office_email,
                                            password=unicode(password),
                                            date_employeed=date_employeed,
                                            date_departed=date_departed,
                                            job_description=unicode(job_description),
                                            office_phone=unicode(office_phone), 
                                            employee_id=employee_id,
                                            company_id=company_id,
                                            title_id=title_id
                                            )
        if i%1000 == 0:
            db.session.commit()
            print i*1000, 'employee_compay added'

        db.session.add(employee_company)
        db.session.commit()

    # commit whatever is left
    db.session.commit()
    print "employee_company seeding completed\n"


def load_company_department():

    print "company_department seeding"
    for i, row in enumerate(open("NOT_FOR_DEPLOYMENT/seed_data/u.company_department")):
        row = row.rstrip()

        company_department_id, company_id, department_id = row.split("|")

        company_department = Company_department(
                                                company_id=company_id,
                                                department_id=department_id
                                                )

        db.session.add(company_department)

    db.session.commit()
    print "company_department seeding completed.\n"


def load_department_title():

    print "department_title seeding"
    for i, row in enumerate(open("NOT_FOR_DEPLOYMENT/seed_data/u.department_title")):
        row = row.rstrip()

        department_title_id, title_id, department_id = row.split("|")

        department_title = Department_title(
                                            title_id=title_id,
                                            department_id=department_id
                                            )

        db.session.add(department_title)

    db.session.commit()
    print "department_title seeding completed.\n"


def load_office_department():

    print "office_department seeding"
    for i, row in enumerate(open("NOT_FOR_DEPLOYMENT/seed_data/u.office_department")):
        row = row.rstrip()

        office_department_id, office_id, department_id = row.split("|")

        office_department = Office_department(
                                              office_id=office_id,
                                              department_id=department_id
                                              )

        db.session.add(office_department)

    db.session.commit()
    print "office_department seeding completed.\n"


if __name__ == "__main__":
    connect_to_db(app)


    purge_db()
    load_employees()
    load_companies()
    load_department()
    load_title()
    load_office()
    load_employee_companies()
    load_company_department()
    load_department_title()
    load_office_department()