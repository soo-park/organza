A final project at HB to generate an employee roster web app

### Features

Multi-language support including asian characters (ASCII, Unicode, UTF8)
DB based auto 1) form menu & 2) organizational structure map updates
Subsidiary supports - many to many relations between employee/company/department/title
Google Map corporate locations
Multi level logins

### Languages
Python, JavaScript, SQL, HTML, CSS

### Technologies
Flask, PostgreSQL, SQLAlchemy, JQuery, AJAX, Jinja
Angular, Bootstrap, openpyxl, virtualenv

### Industry
Git, GitHub, Jira, Photoshop, Illustrator,
Ponyorm online editor


## Data model
![Alt text](/NOT_FOR_DEPLOYMENT/model.jpg?raw=true "Data Model")

## How to see a test run of this site

#### Use bash script given

In terminal window in the folder downloaded, run the following command

source roster_bash.sh

#### Shortcut

Copy the entire paragraph of the following inside the forked folder to run the web app

virtualenv env; source env/bin/activate; dropdb intranet; createdb intranet; pip install -r requirements.txt; echo export secret_key='abc' > secret.sh; source secret.sh; python model.py; python seed.py; open 'http://localhost:5000'; python server.py;

### OR

#### 1. Open your terminal, make secret.sh file

Command: echo "export secret_key='abc'" >> secret.sh
Reason: you want web frame "Flask" and other requirements to run in your computer to test the code, but you do not want to install everything needed to your global environment. Secret.sh file will contain the key for the app to run.

#### 2. Run your virtual environment

Command: virtualenv env; source env/bin/activate; source secret.sh
Reason: to make the installation run in a limited space


#### 3. Install requirements

Command: pip install -r requirements.txt
Reason: all needed installations are saved in requirements.txt. pip is command for Python to pick up necessary packages and install them.

#### 4. Generate db

Command: dropdb intranet; createdb intranet
Reason: createdb command will generate the database that will store the data. The database is named "intranet" inside the model.py file. (if ERROR "Database "intranet" already exists" raised: dropdb intranet is needed. Just to make sure that there is no pre-existing db, you can always go with dropdb intranet)
Caution: this will delete the existing data from your db. If you want to "add" data, and not start a new, do not do this.

#### 5. Run model

Command: python model.py
Reason: the model will be a base template for your db

#### 6. Run seed.py

Command: python seed.py
Reason: generate stating point for your db for testing

#### 7. Check if the db is loaded correctly

Command: psql intranet
         \dt
Reason: you want to see if the tables are generated. If the are generated, a chart containing the list of them wil show.

#### 8. Run server

Command: python server.py
Reason: have your server running, so that what you interact with server-client will be viewable on your browser

#### 9. Run your Flask on browser

Command: localhost:5000 on your browser address bar
Reason: Because your server is running, you can see the site


## Production Screen Shots

### Homepage
![Alt text](/NOT_FOR_DEPLOYMENT/production_screen_shots/localhost5000.png?raw=true "Optional Title")


### Employee list
![Alt text](/NOT_FOR_DEPLOYMENT/production_screen_shots/employees.png?raw=true "Optional Title")


### Multiple search
![Alt text](/NOT_FOR_DEPLOYMENT/production_screen_shots/employees_multiple_search.png?raw=true "Optional Title")


### Employee information
![Alt text](/NOT_FOR_DEPLOYMENT/production_screen_shots/employees1_employee_info.png?raw=true "Optional Title")
