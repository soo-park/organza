import datetime
from sqlalchemy import func

from model import Employee, Employee_company, Company, connect_to_db, db
from server import app


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
                            nickname=nickname,
                            k_name=unicode(k_name),
                            kanji_name=unicode(kanji_name),
                            phone=phone,
                            mobile=mobile,
                            address_line1=address_line1,
                            address_line2=address_line2,
                            city=city,
                            state=state,
                            country=country,
                            postal_code=postal_code,
                            emergency_name=emergency_name,
                            emergency_phone=emergency_phone)

        # We need to add to the session or it won't ever be stored
        db.session.add(employee)

        # provide some sense of progress
        if i % 100 == 0:
            print i, "left till completion."

    # Once we're done, we should commit our work
    db.session.commit()
    print "employees seeding completed.\n"


def load_companies():
    """Load companies from u.item into database."""

    print "companies"

    for i, row in enumerate(open("seed_data/u.company")):
        row = row.rstrip()

        # clever -- we can unpack part of the row!
        company_id, name = row.split("|")

        company = Company(company_id=company_id,
                          name=name)

        # We need to add to the session or it won't ever be stored
        db.session.add(company)

        # provide some sense of progress
        if i % 100 == 0:
            print i, "left till completion."

    # Once we're done, we should commit our work
    db.session.commit()
    print "companies seeding completed.\n"


def load_employee_companies():
    """Load employee_companies from u.data into database."""

    print "employee_companies"

    for i, row in enumerate(open("seed_data/u.data")):
        row = row.rstrip()

        (employee_company_id, office_email, password, 
            employee_id, company_id) = row.split("|")

        employee_company_id = int(employee_company_id)
        employee_id = int(employee_id)
        company_id = int(company_id)

        # We don't care about the timestamp, so we'll ignore this

        employee_company = Employee_company(employee_company_id=employee_company_id,
         office_email=office_email, password=password, employee_id=employee_id,
         company_id=company_id)

        # We need to add to the session or it won't ever be stored
        db.session.add(employee_company)

        # provide some sense of progress
        if i % 1000 == 0:
            print i, "left till completion."

            # An optimization: if we commit after every add, the database
            # will do a lot of work committing each record. However, if we
            # wait until the end, on computers with smaller amounts of
            # memory, it might thrash around. By committing every 1,000th
            # add, we'll strike a good balance.

            db.session.commit()

    # Once we're done, we should commit our work
    db.session.commit()
    print "employee_company seeding completed\n"


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    load_employees()
    load_companies()
    load_employee_companies()