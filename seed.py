"""Utility file to seed ratings database from MovieLens data in seed_data/"""

from sqlalchemy import func

from model import Employee
# from model import Nickname
# from model import Employee_phone
# from model import Emergency_contact_person
# from model import Contact
# from model import Address
# from model import Office
# from model import Company
# from model import Title
# from model import Department
# from model import Employee_dept_office
# from model import Department_title
# from model import Office_department

from model import connect_to_db, db
from server import app
import datetime


def load_employees():
    """Load employees from u.employee into database."""

    print 'employees'

    # Delete all rows in table, so if we need to run this a second time,
    Employee.query.delete()
    # Nickname.query.delete()

    file = open('static/doc/employee.csv')
    for row in file:
        first_name, mid_name, last_name, personal_email = row.rstrip().split(',')
        employee = Employee(
                            first_name=first_name, 
                            mid_name=mid_name, 
                            last_name=last_name, 
                            personal_email=personal_email,
                            )

        # add to the session and commit the employee line
        db.session.add(employee)
        db.session.commit()

        # # add after unicode issue has been resolved
        # nickname = Nickname(
        #                     nickname=nickname,
        #                     k_name=k_name, 
        #                     kanji_name=kanji_name
        #                     )
        # db.session.add(employee)
        # db.session.commit()
    

    # ### Unicode issue ###
    # solution 1
    # Python csv helper better in reading CSV (Hannah Schafer)
    # import csv; csv_file = csv.reader(open('static/doc/employee.csv', 'rU'))
    # Python csv helper better in reading CSV (Hannah Schafer)
    #'rU' makes the record unicode
    # import csv
    # csv_file = csv.reader(open('static/doc/employee.csv'), 'rU')

    # # Set prev_id+1 as a starting point, and add the employees
    # for row in csv_file:
    #     first_name, mid_name, last_name, personal_email =\
    #                 row[0], row[1], row[2], row[3]
    #     print first_name
    # # problem: csv does not save chinese characters

    # # solution 2
    # # http://stackoverflow.com/questions/491921/unicode-utf-8-reading-and-writing-to-files-in-python
    # # unicode_file = codecs.open('static/doc/employee.txt', 'r', 'utf-8')
    # # unicode_file = open('static/doc/employee_nickname.txt',"r").read().decode("utf-8")

    # # problem: all of the solutions make one long string, and thus need to get words.
    # import codecs # imports python codecs for unicode characters
    # decode_file = open('static/doc/employee_nickname.txt').read().decode('string-escape').decode("utf-8")
    # print [word for word in decode_file.rstrip()]

    # # problem: retriving word is possible with re, but it also eliminate empty sting
    # import re
    # print re.compile('\w+').findall(decode_file)

    # solution 3: TODO
    # work with openpyxl to use Excel directly
    # use employee_nickname.txt file
    # setup nickname, k_name, kanji_name with the employee file
    # have the employee add commit line by line
    # have the nickname per person adds after the commit of employee



# def employee_phones():
#     """Load employee_phones from u.item into database."""

#     # Delete all rows in table, so if we need to run this a second time,
#     # we won't be trying to add duplicate employees
#     Movie.query.delete()

#     for row in open('seed_data/u.item'):
#         row = row.rstrip()

#         (movie_id,
#          title,
#          released_str,
#          video_release_date,
#          imdb_url,
#          ) = row.split('|')[:5]

#         # Change release_date to Python datetime
#         if released_str:
#             released_at = datetime.datetime.strptime(released_str, '%d-%b-%Y')
#         else:
#             released_at = None

#         # Remove parenthetical date from the title.
#         # TODO : remove parenthetical date with regex
#         # TODO : anything that has digits in it
#         # if len(title) <= 7:
#         #     print 'This title is going to disappear: {}'.format(title)

#         title = title[:-7].decode('latin-1')

#         movie = Movie(movie_id=movie_id,
#                       title=title,
#                       released_at=released_at,
#                       imdb_url=imdb_url,
#                       )

#         # Read u.employee file and insert data
#         # We need to add to the session or it won't ever be stored
#         db.session.add(movie)

#     # Once we're done, we should commit our work
#     db.session.commit()


# def load_ratings():
#     """Load ratings from u.data into database."""
#     # employee_id \t movie_id \t score \t timestamp.
#     Rating.query.delete()

#     for row in open('seed_data/u.data'):
#         row = row.rstrip()

#         employee_id, movie_id, score = row.split('\t')[:3]

#         rating = Rating(employee_id=employee_id,
#                         movie_id=movie_id,
#                         score=score,
#                         )

#         db.session.add(rating)
#         # print "Successfully added " + str(rating)

#     db.session.commit()




if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_employees()
    # load_movies()
    # load_ratings()
    # set_val_employee_id()
