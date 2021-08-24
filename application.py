from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from passlib.hash import sha256_crypt
from flask_mysqldb import MySQL
from password import sqlpassword
from templates.sqlworkers import *
from templates.forms import *
from functools import wraps

app = Flask(__name__)

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = sqlpassword
app.config['MYSQL_DB'] = 'crypto'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

def is_user_loggedin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("Please login","danger")
            return redirect(url_for("login"))
    return wrap


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

@app.route("/login",methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        candidate = request.form['password']

        users = Table("users", "name", "email", "username", "password")
        user = users.get_one("username",username)
        actual_pass = user.get('password')

        if actual_pass is None:
            flash('Username is not found','danger')
            return redirect(url_for('login'))
        else:
            if sha256_crypt.verify(candidate,actual_pass):
                login_user(username)
                flash('You are now logged in','success')
                return redirect(url_for('dashboard'))
            else:
                flash("Invalid password",'danger')
                return redirect(url_for('login'))


    return render_template('login.html')


@app.route("/logout")
@is_user_loggedin
def logout():
    session.clear()
    flash("Logout success","success")
    return redirect(url_for('login'))

@app.route("/dashboard")
@is_user_loggedin
def dashboard():
    return render_template('dashboard.html',session=session)


@app.route("/transaction", methods = ['GET','POST'])
@is_user_loggedin
def transaction():
    form = SendMoneyForm(request.form)
    balance =  get_balance(session.get('username'))

    if request.method == 'POST':
        pass

    return render_template('transaction.html',balance=balance,form=form)

@app.route("/")
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug=True)
