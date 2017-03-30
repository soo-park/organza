"""department Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, jsonify, render_template, request, flash, redirect,
                   session)
from flask_debugtoolbar import DebugToolbarExtension

from model import Employee, connect_to_db

# from model import Office


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = 'fygkiybwe468hfjhykutgkjdlkjasll;asdkjfhgfddu8hw9fogiulhfj'

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template('index.html')


@app.route('/employee')
def employee_list():
    """Show list of employees."""

    employees = employees.query.all()
    return render_template('employee_list.html', employees=employees)


# @app.route('/login')
# def login():
#     """login form"""

#     return render_template('login_form.html')


# @app.route('/login', methods=['POST'])
# def process_login():
#     """Process the login form.

#     Flash message confirming login. Add employee to session.
#     """

#     email = request.form.get('email')
#     password = request.form.get('password')

#     # TODO : Consider later
#     # Make sure it is first time for the employee to login

#     # throw an error if the employee is not the ('employee='' part tried)
#     try:
#         employee = employee.query.filter_by(email=email).one()

#         # if it is first time, then check authentification
#         if password == employee.password:
#             flash(email + ' logged in')
#             session['employee'] = email
#             print session
#             return redirect('/employee/' + str(employee.employee_id))

#     # if not authentificated, then do not login the employee
#     except:
#         flash('employee does not exist')
#         return redirect('/')


# @app.route('/logout', methods=['POST'])
# def process_logout():
#     """Logout the employee.

#     Flash a message confirming the logout.
#     """

#     del session['employee']
#     flash('You logged out')

#     return redirect('/')


# @app.route('/employee/<employee_id>')
# def employee_info(employee_id):
#     """Display employee information."""

#     try:
#         employee = employee.query.filter_by(employee_id=employee_id).one()
#         # TODO : use query to order by title
#         ratings = sorted(employee.ratings, cmp=lambda x, y: cmp(x.department.title.lower(), y.department.title.lower()))
#         return render_template('employee_profile.html', employee=employee,
#                                                     ratings=ratings)
#     except:
#         flash('employee does not exist.')
#         return redirect('/')


# @app.route('/departments')
# def departments():
#     """List all departments by alphabetical order."""

#     departments = department.query.order_by(department.title).all()
#     return render_template('department_list.html', departments=departments)


# @app.route('/department/<department_id>')
# def department_info(department_id):
#     """Display department information."""

#     try:
#         department = department.query.filter_by(department_id=department_id).one()
#         return render_template('department_info.html', department=department)
#     except:
#         flash('department does not exist')
#         return redirect('/')


# @app.route('/update_rating', methods=['POST'])
# def update_rating():
#     """Update rating for department."""

#     department_id = request.form.get('department_id')
#     employee_id = employee.query.filter_by(email=session['employee']).one().employee_id

#     try:
#         rating = Rating.query.filter_by(department_id=department_id,
#                                         employee_id=employee_id).one()
#         rating.score = request.form.get('rating')
#         db.session.commit()
#         flash('Rating updated')
#     except:
#         db.session.add(Rating(department_id=department_id,
#                               employee_id=employee_id,
#                               score=request.form.get('rating')))
#         db.session.commit()
#         flash('Rating added')

#     return redirect('/department/' + department_id)


if __name__ == '__main__':
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
