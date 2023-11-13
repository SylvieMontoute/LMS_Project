from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

app.secret_key = 'Sylvie21'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Berklin21'
app.config['MYSQL_DB'] = 'users'

mysql = MySQL(app)

@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM registrations WHERE username = % s AND user_pass = % s', (username, password,))
        account = cursor.fetchone()
    if account:
        session['loggedin'] = True
        session['id'] = account['id']
        session['username'] = account['username']
        msg = 'Logged in successfully !'
        return render_template('index.html', msg=msg)
    else:
        msg = 'Incorrect username / password !'
    return render_template('login.html', msg=msg)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/registration', methods =['GET', 'POST'])
def registration():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'role' in request.form :
        username = request.form['username']
        password = request.form['password']
        email: str = request.form['email']
        role: str = request.form['role']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM registrations WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[A-Za-z0-9]+',username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO registrations VALUES (NULL, % s, % s)',(username, password, email, role))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
            msg = 'Please fill out the form !'
    return render_template('registration.html', msg=msg)

@app.route('/course', methods =['GET', 'POST'])
def course():
    msg = ''
    if request.method == 'POST' and 'coursename' in request.form and 'coursecontent' in request.form :
        coursename: str = request.form['coursename']
        coursecontent: str = request.form['coursecontent']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM courses WHERE coursename = % s', (coursename, ))
        account = cursor.fetchone()
        if account:
            msg = 'Course already exists !'
        else:
            cursor.execute('INSERT INTO courses VALUES (NULL, % s, % s)',(coursename,coursecontent ))
            mysql.connection.commit()
            msg = 'You have successfully created a course!'
    elif request.method == 'POST':
            msg = 'Please fill out the form !'
    return render_template('course.html', msg=msg)

@app.route('/enrollment', methods =['GET', 'POST'])
def enrollment():
    msg = ''
    if request.method == 'POST' and 'coursecode' in request.form :
        coursecode = request.form['coursecode']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM courses WHERE coursecode = % s', (coursecode, ))
        account = cursor.fetchone()
        if account:
            msg = 'Course exists!'
        else:
            cursor.execute('INSERT INTO courses VALUES (NULL, % s, % s)',(coursecode))
            mysql.connection.commit()
            msg = 'You have successfully enrolled in this course!'
    elif request.method == 'POST':
            msg = 'Please fill out the form !'
    return render_template('enrollment.html', msg=msg)