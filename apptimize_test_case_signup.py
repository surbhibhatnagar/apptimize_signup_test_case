import poplib
import random
import re
import string
import time
import unittest
import os
import sys
from email import parser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

"""Test suite to verify whether an apptimize user has sucessfully registered 
and received confirmation mail or not. This test case first signs up a user 
with different variations of a single gmail account on apptimize platform and 
then verifies whether user has received confirmation email from apptimize or not
to their original gmail account or not"""
class SignUp(unittest.TestCase):

    def setUp(self):
        gecko_path = os.path.dirname(os.path.abspath(__file__))
        sys.path.append(gecko_path)
        os.environ["PATH"] += os.pathsep + gecko_path
        #print os.environ["PATH"]
        # create a new Firefox session to submit new sign up form
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(5)
        self.driver.maximize_window()
        # create a new Firefox session to verify if user can login using new
        # credentials
        self.second_driver = webdriver.Firefox()
        # Define original gmail id
        self.original_email = 'surbhiapptimize@gmail.com'
        self.uname = 'surbhiapptimize'
        # Define signn up url and test values
        self.signup_URL = 'http://www.apptimize.com/'
        self.first_name = 'Surbhi'
        self.last_name = 'Bhatnagar'
        self.email = 'surbhiapptimize+' + ''.join(random.choice(
            string.ascii_lowercase + string.digits) for _ in
                                                  range(5)) + '@gmail.com'
        self.company_name = 'Apptimize Candidate'
        self.password = '@pptimize'
        # Define UI ids of apptimize sign-up page
        self.signup_btn_id = 'Sign Up'
        self.signup_first_name_id = 'fname'
        self.signup_last_name_id = 'lname'
        self.signup_email_id = 'email'
        self.company_id = 'company'
        self.password_id = 'password'
        self.purchased_radio_id = "input[type='radio'][value='Yes'][name='purchased']"
        self.eula_id = 'eula'
        self.submit_id = 'submit'
        # Define UI ids of login page
        self.login_email_id = 'zet-login-email'
        self.login_password_id = 'zet-login-password'
        self.login_btn_id = 'zet-loginbtn'
        # Define values related to Google email
        self.receiver_name = 'Surbhi'

    """New Apptimize account creation """
    def test_1(self):
        # navigate to the application home page
        self.driver.get(self.signup_URL)
        # To do: check if correct page is loaded
        # click on the signup button
        self.driver.find_element_by_link_text(self.signup_btn_id).click()
        # To do: check if correct page is loaded
        time.sleep(10)
        # Find all ids on sign up page
        first_name = self.driver.find_element_by_id(self.signup_first_name_id)
        last_name = self.driver.find_element_by_id(self.signup_last_name_id)
        email = self.driver.find_element_by_id(self.signup_email_id)
        company = self.driver.find_element_by_id(self.company_id)
        password = self.driver.find_element_by_id(self.password_id)
        radio = self.driver.find_element_by_css_selector(
            self.purchased_radio_id)
        eula = self.driver.find_element_by_id(self.eula_id)
        signup = self.driver.find_element_by_id(self.submit_id)
        # Fill sign up form
        first_name.send_keys(self.first_name)
        last_name.send_keys(self.last_name)
        email.send_keys(self.email)
        company.send_keys(self.company_name)
        password.send_keys(self.password)
        radio.click()
        eula.click()
        signup.click()
        self.driver.delete_all_cookies
        time.sleep(10)
        # Check if confirmation email has been sent to original email
        pop_conn = poplib.POP3_SSL('pop.gmail.com')
        pop_conn.user(self.uname)
        pop_conn.pass_(self.password)
        # Get messages from server:
        messages = [pop_conn.retr(i) for i in
                    range(1, len(pop_conn.list()[1]) + 1)]
        # Concat message pieces:
        messages = ["\n".join(mssg[1]) for mssg in messages]
        # Parse message intom an email object:
        messages = [parser.Parser().parsestr(mssg) for mssg in messages]
        for message in messages:
            to = self.receiver_name + ' <' + self.email + '>'
            if message['to'] == to:
                # extract URL
                url = re.search("(?P<url>https?://[^\s]+)", str(message)).group(
                    "url")
                break
        pop_conn.quit()
        self.second_driver.get(url)
        # check if you can successfully log in on Apptimize platform using
        # confirmation mail
        login_email = self.second_driver.find_element_by_id(self.login_email_id)
        login_email.send_keys(self.original_email)
        pwd = self.second_driver.find_element_by_id(self.login_password_id)
        pwd.send_keys(self.password)
        btn = self.second_driver.find_element_by_id(self.login_btn_id)
        btn.click()

    def tearDown(self):
        # close the browser window
        self.driver.quit()
        self.second_driver.quit()


if __name__ == '__main__':
    unittest.main()
