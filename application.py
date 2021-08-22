from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from passlib.hash import sha256_crypt
from flask_mysqldb import MySQL
from password import sqlpassword
from templates.sqlworkers import *
from templates.forms import *

app = Flask(__name__)

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = sqlpassword
app.config['MYSQL_DB'] = 'crypto'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)


def login_user(username):
    users = Table("users", "name", "email", "username", "password")
    user = users.get_one("username",username)

    session['logged_in'] = True
    session['username'] = username
    session['name'] = user.get('name')
    session['email'] = user.get('email')


@app.route("/sign-up", methods=['GET', 'POST'])
def register():
    form = SignupForm(request.form)
    users = Table("users", "name", "email", "username", "password")


    if request.method == 'POST' and form.validate():
       
        username = form.username.data
        email = form.email.data
        name = form.name.data

       
        if isnewuser(username):
            
            password = sha256_crypt.encrypt(form.password.data)
            users.insert(name,email,username,password)
            login_user(username)
            return redirect(url_for('dashboard'))
        else:
            flash('User already exists', 'danger')
            return redirect(url_for('register'))
    return render_template('signup.html', form=form)


@app.route("/dashboard")
def dashboard():
    return render_template('dashboard.html',session=session)

@app.route("/")
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug=True)
