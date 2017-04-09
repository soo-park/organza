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

# TODO: write some unit tests. Currently it is all integration tests

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


    def test_brands(self):

        # make request to /employees route

        pass



        
