from flask import Flask, redirect, request, render_template
import os
import cgi
import jinja2

app = Flask(__name__)
app.config['DEBUG'] = True

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)


@app.route('/')
def display_user_signup():
    template = jinja_env.get_template('index.html') 
    return template.render()


@app.route('/', methods = ['GET', 'POST'])
def validate_username_submission():
    username = request.form['username']
    username_error = ''
    template = jinja_env.get_template('index.html') 

    if username == "":
      username_error = 'You cannot leave space empty. '
      username = ""
    if len(username) < 3 or len(username) > 20: 
      username_error = "Username must be between 3-20 characters in length."
      username = ""
    if " " in username:
      username_error = "Username cannot have spaces."
      username = ""
    else: 
        if not username_error:
            un = "Welcome, " + username + "!"
            return redirect('/validated?un={0}'.format(un))

    return template.render()

@app.route('/validated', methods = ['POST', 'GET'])
def display_validated_form():
  un = request.args.get("un")
  return '<h1>{0}</h1>'.format(un)

app.run()
