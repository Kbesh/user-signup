#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import re


USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASSWORD_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASSWORD_RE.match(password)

EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email(email):
    return not email or EMAIL_RE.match(email)

def show_page(username, error_username, error_password, error_verify, email, error_email):
    username_label = "<label>Username:</label>"
    username_input = "<input type='text' name='username' value=" + username + "><td class = 'error'>" + error_username + "</td>"

#ask me about html tags for errors
    password_label = "<label>Password:</label>"
    password_input = "<input type='text' name='password' value=''/><td class = 'error'>" + error_password + "</td>"

    verify_password_label = "<label>Confirm Password:</label>"
    verify_password_input = "<input type='text' name='verify' value=''/><td class ='error'>" + error_verify + "</td>"

    email_label = "<label>Email:</label>"
    email_input = "<input type='text' name='email' value=" + email +"><td class = 'error'>" + error_email + "</td>"

    submit = "<input type='submit'/>"

    form = ("<form action='/validation' method='post'>"
        + username_label + username_input + "<br>"
        + password_label+ password_input + "<br>"
        + verify_password_label+ verify_password_input + "<br>"
        + email_label+ email_input + "<br>"
        + submit
        + "</form>")

    return form



def welcome_page(confirmed_username):
    welcome = """
    <html>
        <head>
            <title>Signup Page</title>
        </head>
        <body>""" + "<h2>Welcome, " + confirmed_username + "</h2></body><html>"

    return welcome

class FormHandler(webapp2.RequestHandler):
    def get(self):
        params = {'username': "", 'email': "", 'error_username': "", 'error_password': "", 'error_verify': "", 'error_email': ""}
        #intialize with empty values
        #username, error_username, password, error_password, verify, error_verify, email, error_email
        content = show_page(params['username'], params['error_username'], params['error_password'], params['error_verify'], params['email'], params['error_email'])
        self.response.write(content)

class ValidationHandler(FormHandler):
        def post(self):
            params ={}
            username = self.request.get("username")
            params['username'] = username
            password = self.request.get("password")
            verify = self.request.get("verify")
            email = self.request.get("email")
            params['email'] = email

            # params = {"username" : username,
                            # "email" : email)
    # if then shit


            have_error = False

            params['error_verify'] = ""
            params['error_email'] = ""
            params['error_password'] = ""
            params['error_username'] = ""

            if not valid_username(username):
                params['error_username'] = "That is not a valid username."
                have_error = True


            if not valid_password(password):
                params['error_password'] = "That is not a valid password."
                have_error = True

            elif password != verify:
                params['error_verify'] = "Your passwords do not match."
                have_error = True


            if not valid_email(email):
                params['error_email'] = "That is not a valid email."
                have_error = True





    #within if then call validation method
            if have_error == True:
                content = show_page(params['username'], params['error_username'], params['error_password'], params['error_verify'], params['email'], params['error_email'])
                self.response.write(content)
            else:
                self.response.write(welcome_page(username))

app = webapp2.WSGIApplication([
    ('/', FormHandler),
    ('/validation', ValidationHandler)
], debug=True)
