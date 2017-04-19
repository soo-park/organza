# Before running the test
# In your virtual environment, type in the following to the terminal
# pip install coverage

# Test things along the way of building test as well
# <How to test the test>
# ipython -i server.py # to go into the interactive mode
# ctrl + c # to quit server from running

# <Test example1>
# tc = app.test_client(); tc
# expected result >>> <FlaskClient <Flask 'server'>
# indicates that now you can generate a test client

# <Test example2>
# resp = tc.get('/'); resp
# expected result >>> <Response streamed [200 OK]>
# indicates the route '/' is returning 200 on client
# So if the browser will be running, you will get a page

import unittest
from unittest import TestCase
from server import app

class HomepageIntegrationTest(TestCase):
    """A smote test."""


    def setUp(self):
        """Setsup a temporary ground for testing"""

        # make a test client <FlaskClient <Flask u'server'>>
        tc = app.test_client()
        self.client = tc


    def test_homepage(self):
        """Tests the viability of the homepage"""

        resp = self.client.get('/')
        # make request to / route <Response streamed [200 OK]>

        # in interactive mode, try dir(resp) to see possible commands
        # data gets a string of the entire body of the HTML page
        # put whatever string you expect from that data on 
        # '/' page to check. In this case, something from index.html
        self.assertIn("Employee Roster", resp.data)

    def tearDown(self):
        """Clean up"""

        db.session.close()
        db.drop_all()


class DatabaseIntegrationTest(TestCase):

    def setUp(self):
        # Connect to our testdb
        connect_to_db(app, "postgresql:///testdb")
        db.create_all()

        # possibly seed it with example_data()

        # make test_client

    def tearDown(self):
        """Clean up"""

        db.session.close()
        db.drop_all()

    def test_login(self):
        """Tests if the login/logout is working"""

        rest = self.client.get('/logged')

    def test_employees(self):
        # make request to /employees route

        resp = self.client.get('/employees')
        self.assertEqual(200, resp.status_code)
        self.assertNotEqual(404, resp.status_code)
        self.assertIn("Employee Search", resp.data)


# "add emloyee" test

# before change, make tests & commit before 

# For login feature, user the following id & password to check the model.
# a@seahusa.com pass: aaa123 (admin=’true’)
# b@seahusa.com pass: bbb123 (yes date_employeed, no date_departed, admin=’false’)
# c@seahusa.com pass: ccc123 (yes date_employeed, no date_departed, admin=’false’)
# d@seahusa.com pass: ddd123(yes date_employeed, no date_departed, admin=’false’)


if __name__ == "__main__":
    unittest.main()

        
