from flask import Flask, request, redirect, render_template

app = Flask(__name__)

app.config["DEBUG"] = True

def is_valid(field):
    if len(field) < 3 or len(field) > 21 or not field:
        return False
    if " " in field:
        return False
    return True

def is_valid_email(email):
    if not is_valid(email):
        return False
    if "." not in email or "@" not in email or " " in email:
        return False
    return True

def validate(inputs, errors):
    if not is_valid(inputs['username']):
            errors['username']="That's not a valid username"
    if not is_valid(inputs['password']):
        errors["password"] = "That's not a valid password"
    if inputs['password'] != inputs['verify_pass'] or not inputs['verify_pass']:
        errors["match_password"] = "Passwords don't match"
    if inputs['email']:
        if not is_valid_email(inputs['email']):
            errors["email"] = "That's not a valid email"



@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index_form.html")

    if request.method == "POST":
        username = request.form['user-name'].strip()
        password = request.form['password'].strip()
        verify_pass = request.form['verify-pass'].strip()
        email = request.form['email'].strip()
        field_inputs = {'username':username, 'password':password, 'verify_pass':verify_pass, 'email':email}
        errors = {}

        validate(field_inputs, errors)
        
        if errors:
            form_fields = {'username': username, "email": email}
            return render_template("index_form.html", errors=errors, form_fields=form_fields)
        return "Welcome, " + request.form["user-name"]

app.run()