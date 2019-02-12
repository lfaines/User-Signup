from flask import Flask, request, redirect
import cgi
import os
import jinja2

app = Flask(__name__)
app.config['DEBUG'] = True

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)


@app.route('/validate-submission')
def display_signup_form():
    template = jinja_env.get_template('index.html')
    return template.render()

@app.route('/validate-submission', methods = ['POST', 'GET'])
def validate_signup_form():
    username = request.form['username']
    password = request.form['password']
    verify_password = request.form['verify_password']
    email_address = request.form['email_address']

    username_error = ''
    password_error = ''
    verify_password_error = ''
    email_address_error = ''
    empty = ""

    if password == empty or verify_password == empty:
      password_error ="You cannot leave space empty."
      password = ""
      verify_password_error ="You cannot leave space empty."
      verify_password = ""
    elif len(password) and len(verify_password) < 3 or len(password) and len(verify_password) > 20: 
      password_error = "Passwords must be between 3-20 characters in length."
      password = ""
      verify_password_error = "Passwords must be between 3-20 characters in length."
      verify_password = ""
    elif " " in password and verify_password:
      password_error = "Passwords cannot have spaces."
      password = ""
      verify_password_error = "Passwords cannot have spaces."
      verify_password = ""
    elif password != verify_password:
      password_error = "Passwords don't match."
      password = ""
      verify_password_error = "Passwords don't match."
      verify_password = ""
    if password == verify_password:
      password = ""
      verify_password = ""
    
    if username == "":
      username_error = "You cannot leave space empty."
      username = ""
    elif len(username) < 3 or len(username) > 20: 
      username_error = "Username must be between 3-20 characters in length."
      username = ""
    elif " " in username:
      username_error = "Username cannot have spaces."
      username = ""

    if len(email_address) == 1 or len(email_address) == 2 or len(email_address) ==3 or len(email_address) > 20:
      email_address_error = "Email must be between 3-20 characters."
      email_address = ""
    if len(email_address) == 0:
      email_address = ""
    elif not ("@") in email_address:
      email_address_error = "Please enter a valid Email."
      email_address = ""
    elif not (".") in email_address:
      email_address_error = "Please enter a valid Email."
      email_address = ""
    elif email_address.count("@") > 1 or email_address.count(".") > 1 or email_address.count(" ") >= 1:
      email_address_error = "Please enter a valid Email."
      email_address = ""
    if username_error == "" and password_error== "" and verify_password_error== "" and email_address_error == "":
      un = "Welcome, " + username + "!"
      return redirect('/validated?un={0}'.format(un))
    
    template = jinja_env.get_template('index.html')
    return template.render(username_error = username_error, password_error = password_error, email_address_error = email_address_error, username = username, password = password, verify_password = verify_password, verify_password_error = verify_password_error, email_address = email_address) 


@app.route('/validated')
def display_validated_form():
  un = request.args.get("un")
  return '<h1>{0}</h1>'.format(un)
    

app.run()