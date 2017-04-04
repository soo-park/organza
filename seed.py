import datetime
from sqlalchemy import func

from model import Employee, Employee_company, Company, connect_to_db, db
from server import app


def load_employees():
    """Load employees from u.employee into database."""

    print "employees"

    for i, row in enumerate(open("seed_data/u.employee")):
        row = row.rstrip()
        (employee_id, photo_URL, birthday, personal_email,
            first_name, last_name, k_name) = row.split("|")

        employee = Employee(employee_id=employee_id,
                            photo_URL=photo_URL,
                            birthday=birthday,
                            personal_email=personal_email,
                            first_name=first_name,
                            last_name=last_name,
                            k_name=k_name)

        # We need to add to the session or it won't ever be stored
        db.session.add(employee)

        # provide some sense of progress
        if i % 100 == 0:
            print i

    # Once we're done, we should commit our work
    db.session.commit()


def load_companys():
    """Load companys from u.item into database."""

    print "companys"

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
            print i

    # Once we're done, we should commit our work
    db.session.commit()


def load_employee_companys():
    """Load employee_companys from u.data into database."""

    print "employee_companys"

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
            print i

            # An optimization: if we commit after every add, the database
            # will do a lot of work committing each record. However, if we
            # wait until the end, on computers with smaller amounts of
            # memory, it might thrash around. By committing every 1,000th
            # add, we'll strike a good balance.

            db.session.commit()

    # Once we're done, we should commit our work
    db.session.commit()


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

    load_employees()
    load_companys()
    load_employee_companys()
    set_val_employee_id()