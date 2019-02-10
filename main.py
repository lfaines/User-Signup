
from flask import Flask, request, redirect
import cgi
import os
import jinja2

app = Flask(__name__)
app.config['DEBUG'] = True

signup = """
<!doctype html>
<html>
    <head>
        <title>User Sign-Up</title>
    </head>
    <body>
        <h1> Sign-Up Form</h1><br>
        <form action = 'validate-submission' method = 'post'>    
           <label> Username:
           {% if username is None %}
           
                <input type = "text" name = "username" value = "{username}"
                {{username_error}}
                {% endif %}
               <!-- <h4 name = "username_error">{username_error}</h4>--> </>
                <br>
                <br>
            <label>Password:
                <input type = "password" name = "password"
                <h4 name = "password_error">{password_error}</h4></>
                <br>
                <br>
            <label>Verify Password:
                <input type = "password" name = "verify_password"
                <h4 name = "verify_password_error">{verify_password_error}</h4></>
                <br>
                <br>
            <label>Email Address (optional):
                <input type = "text" name = "email_address" value = "{email_address}"
                <h4 name = "email_address_error">{email_address_error}</h4></>
                <br>
                <br>
            <input type = "submit" />
        </form>
    </body>
</html>
"""

@app.route('/validate-submission')
def display_signup_form():
    return signup.format(username_error = '', password_error = '', email_address_error = '', username = '', password = '', verify_password = '', verify_password_error = '', email_address = '') 

@app.route('/validate-submission', methods = ['POST'])
def validate_signup_form():
    username = request.form['username']
    password = request.form['password']
    verify_password = request.form['verify_password']
    email_address = request.form['email_address']

    username_error = "You cannot leave space blank."
    password_error = ''
    verify_password_error = ''
    email_address_error = ''
    blank = ""

    if password == blank or verify_password == blank or username == blank:
      password_error ="You cannot leave space blank."
      password = ""
      verify_password_error ="You cannot leave space blank."
      verify_password = ""
      #username_error = "You cannot leave space blank."
      username = ""
    elif len(password) and len(verify_password) and len(username) < 3 or len(password) and len(verify_password) and len(username) > 20: 
      password_error = "Passwords must be between 3-20 characters in length."
      password = ""
      verify_password_error = "Passwords must be between 3-20 characters in length."
      verify_password = ""
      username_error = "Username must be between 3-20 characters in length."
      username = ""
    elif " " in password and verify_password and username:
      password_error = "Passwords cannot have spaces."
      password = ""
      verify_password_error = "Passwords cannot have spaces."
      verify_password = ""
      username_error = "Username cannot have spaces."
      username = ""
    elif password != verify_password:
      password_error = "Passwords don't match."
      password = ""
      verify_password_error = "Passwords don't match."
      verify_password = ""
    elif password == verify_password:
      password = ""
      verify_password = ""
  
 
    elif len(email_address) == 1 or len(email_address) == 2 or len(email_address) > 20:
     email_address_error = "Email must be between 3-20 characters."
     email_address = ""
    elif email_address.count("@") > 1 or email_address.count(".") > 1 or email_address.count(" ") >= 1:
        email_address_error = "Please enter a valid Email."
        email_address = ""
    elif not ("@") in email_address and len(email_address) > 3 and len(email_address) < 20:
        email_address_error = "Please enter a valid Email."
        email_address = ""
    elif not (".") in email_address and len(email_address) > 3 and len(email_address) < 20:
        email_address_error = "Please enter a valid Email."
        email_address = ""
    #elif len(email_address) == 0:
      #email_address = ""
        #email_address_error = ""
    #else:
    elif not username_error:
        un = "Welcome, " + username + "!"
        return redirect('/validated?un={0}'.format(un))
    elif not password_error:
        un = "Welcome, " + username + "!"
        return redirect('validated?un={0}'.format(un))
    elif not verify_password_error:
        un = "Welcome, " + username + "!"
        return redirect('validated?un={0}'.format(un))      
    elif not email_address_error:
        un = "Welcome, " + username + "!"
        return redirect('validated?un={0}'.format(un))
    elif not verify_password_error and not email_address_error: 
      un = "Welcome, " + username + "!"
      return redirect('/validated?un={0}'.format(un))
 
    return signup.format(username_error = username_error, password_error = password_error,email_address_error = email_address_error, username = username, password = password, verify_password = verify_password, verify_password_error = verify_password_error, email_address = email_address) 

@app.route('/validated')
def display_validated_form():
  un = request.args.get("un")
  return '<h1>{0}</h1>'.format(un)
    

app.run()