A final project at HB to generate an employee roster web app

Back: Python, JavaScript, SQL
Front: JavaScript, HTML, CSS

Webframe: Flask
DB: PostgreSQL, SQLAlchemy
Other: Jinja, JQuery, AJAX, Angular
openpyxl, virtualenv

Non-tech:
Git, GitHub, Jira, Photoshop, Illustrator


<<<How to see a test run of this site>>>

1. Open your terminal

Reason: you want web frame "Flask" and other requirements to run in your computer to test the code, but you do not want to install everything needed to your global environment

2. Run your virtual environment

Command: virtualenv env
Reason: to make the installation run in a limited space

3. Install requirements

Command: pip install -r requirements.txt
Reason: all needed installations are saved in requirements.txt. pip is command for Python to pick up necessary packages and install them.

4. Generate db

Command: createdb intranet
Reason: createdb command will generate the database that will store the data. The database is named "intranet" inside the model.py file. 

5. Run model

Command: python model.py
Reason: the model will be a base template for your db

6. Run seed.py

Command: python seed.py
Reason: generate stating point for your db for testing
# Caution1: this will delete the existing data from your db. If you want to "add" data, and not start a new, do not do this.
# Caution2: if you have generated a database previously and want to eliminate all data, you have to "dropdb intranet" before you start all over from 1. This will delete all things in intranet db.

7. Check if the db is loaded correctly

Command: psql intranet
         \dt
Reason: you want to see if the tables are generated. If the are generated, a chart containing the list of them wil show.

8. Run server

Command: python server.py
Reason: have your server running, so that what you interact with server-client will be viewable on your browser

9. Run your Flask on browser

Command: localhost:5000 on your browser address bar
Reason: Because your server is running, you can see the site

