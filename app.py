from flask import Flask, render_template, request, redirect, url_for, session
from sqlalchemy import create_engine, text
from models.models import *
import hashlib

app = Flask(__name__)
app.secret_key = 'Sylvie21'
app.config['SQLALCHEMY_DATABASE_URI']='mysql+mysqlconnector://root:Berklin21@localhost/lms_db'
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=True)

Base.metadata.create_all(engine)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/home')
def home():
    if 'loggedin' in session:
        return render_template('home.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username'].lower()
        password_entered = request.form['password']
        #decrypt the password
        hash = password_entered + app.secret_key
        hash = hashlib.sha256(hash.encode())
        password = hash.hexdigest()
        #check if the user exists in the database
        with engine.connect() as con:
            result = con.execute(text(f"Select * from users where username = '{username}' and password = '{password}'"))
            account = result.fetchone()
            con.commit()

    if account:
        session['loggedin'] = True
        session['id'] = account.id
        session['username'] = account.username
        msg = 'Logged in successfully !'
        return redirect(url_for('home', msg=msg))
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
        username = request.form['username'].lower()
        cusername = request.form['cusername'].lower()
        password = request.form['password']
        cpassword = request.form['cpassword']
        if username!=cusername:
            msg = "Usernames do not match"
            return render_template('registration.html', msg=msg)
        if password!=cpassword:
            msg = "Passwords do not match"
            return render_template('registration.html', msg=msg)
        with engine.connect() as con:
            result = con.execute(text(f"Select * from users where username = '{username}'"))
            account = result.fetchone()
            con.commit()
        if account:
            msg = "Account already exists"
            return render_template('registration.html', msg=msg)
        
        if not username or not password or not cusername or not cpassword:
                msg = "Please fill out the form"
                return render_template('registration.html', msg=msg)
        else:
            #encrypt the password
            hash = password + app.secret_key
            hash = hashlib.sha256(hash.encode())
            password = hash.hexdigest()
            #insert the user into the database
            with engine.connect() as con:
                con.execute(text(f"Insert into users (username, password) values ('{username}', '{password}')"))
                con.commit()
            msg = "Account created successfully"
            return redirect(url_for('login', msg=msg))
    return render_template('registration.html', msg=msg)
       

@app.route('/course', methods =['GET', 'POST'])
def course():
    msg = ''
    if request.method == 'POST' and 'course_name' in request.form and 'course_id' in request.form and 'teacher_id' in request.form:
        course_name = request.form['course_name']
        course_id = request.form['course_id']
        teacher_id = request.form['teacher_id']
        with engine.connect() as con:
            result = con.execute(text(f"Select * from courses where course_name = '{course_name}'"))
            account = result.fetchone()
            con.commit()
            if account:
                msg = 'Course already exists!'
            else:
                con.execute('Insert into courses VALUES (NULL, %s, %s)', (course_name, course_id, teacher_id))
                msg = 'You have successfully created a course!'
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('course.html', msg=msg)
    

@app.route('/enrollment', methods =['GET', 'POST'])
def enrollment():
    msg = ''
    if request.method == 'POST' and 'course_id' in request.form:
        course_id = request.form['course_id']
        enrollment_id = request.form['enrollment_id']
        student_id = request.form['student_id']
        with engine.connect() as con:
            result = con.execute(text(f"Select * from enrollments where course_id= '{course_id}'"))
            account = result.fetchone()
            con.commit()
            if account:
                msg = 'Course exists!'
            else:
                con.execute('Insert into courses VALUES (NULL, %s, %s)', (course_id, enrollment_id, student_id))
                msg = 'You have successfully enrolled in this course!'
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('enrollment.html', msg=msg)

#The page for the user registration
@app.route('/register_user', methods=['POST'])
def register_user():
    #get the data from the form
    if request.method=='POST' and 'unique_id' in request.form:
        unique_id = request.form['unique_id']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        middle_name = request.form['middle_name']
        date_of_birth = request.form['dob']
        phone_number = request.form['phone']
        address = request.form['line1']
        city = request.form['city']
        state = request.form['state']
        zip_code = request.form['zip-code']
        country = request.form['country']
        email = request.form['email']
        role = request.form['role']

        #check if the unique_id is already in the database
        with engine.connect() as con:
            result = con.execute(text(f"SELECT * FROM users WHERE unique_id = '{unique_id}'"))
            user = result.fetchone()
            if user:
                msg = 'The user already exists.'
                return redirect(url_for('home', msg = msg))
        #check if all the required fields are filled
        
        #insert the values in the database
        created_at = datetime.now()
        updated_at = datetime.now()
        created_by = session['id']
        updated_by = session['id']
        with engine.connect() as con:
            con.execute(text(f"INSERT INTO users(created_by, created_at, updated_at, updated_by, unique_id, first_name, last_name, middle_name, date_of_birth,\
                                        phone_number, address, city, state, zip_code, country, email, role)\
                                      VALUES('{created_by}','{created_at}', '{updated_at}', '{updated_by}','{unique_id}', '{first_name}', '{last_name}', '{middle_name}',\
                                      '{date_of_birth}', '{phone_number}', '{address}', '{city}', '{state}', '{zip_code}', '{country}', '{email}', '{role}')"))              
            con.commit()
        msg = 'You have successfully registered the user.';
        # redirect the user to the home page
        return redirect(url_for('home', msg = msg))
    return render_template('home.html')

#The retieve user page based on passed user_id
@app.route('/retrieve_user', methods=['POST'])
def retrieve_user():
    msg = ''
    #get the user_id from the urlß
    user_id = request.form['user_id']
    #validate the user_id
    #if the user_id is not valid, redirect to the home page
    #if the user_id is valid, continue
    if 'loggedin' in session:
        if user_id:
            #get the user data from the database
            with engine.connect() as con:
                result_users = con.execute(text(f"SELECT * FROM users WHERE unique_id = '{user_id}'"))
                result_courses = con.execute(text(f"SELECT * FROM courses WHERE unique_id = '{user_id}'"))
                result_course_materials = con.execute(text(f"SELECT * FROM course_materials WHERE unique_id = '{user_id}'"))
                result_enrollments = con.execute(text(f"SELECT * FROM enrollments WHERE unique_id = '{user_id}'"))
                result_student_progress = con.execute(text(f"SELECT * FROM student_progress WHERE unique_id = '{user_id}'"))
                result_performance_reports = con.execute(text(f"SELECT * FROM performance_reports WHERE unique_id = '{user_id}'"))

                users = result_users.fetchone()
                courses = result_courses.fetchone()
                course_materials = result_course_materials.fetchone()
                enrollments = result_enrollments.fetchone()
                student_progress = result_student_progress.fetchone()
                performance_reports = result_performance_reports.fetchone()
                
                con.commit()
            if users and courses and course_materials and enrollments and student_progress and performance_reports:
                #display the user data
                return render_template('userprofile.html', users = users, courses = courses, course_materials = course_materials, enrollments = enrollments, student_progress = student_progress, performance_reports = performance_reports)
                                     
            else:
                #redirect to the home page
                msg = 'The user does not exist.'
                return redirect(url_for('home', msg = msg))
    return redirect(url_for('login'))

@app.route('/update_users', methods=['POST'])
def update_users():
    msg=""
    user_id = request.form['unique_id']
    if 'loggedin' in session:
        if user_id:
            #get the user data from the database
            with engine.connect() as con:
                result_users = con.execute(text(f"SELECT * FROM users WHERE unique_id = '{user_id}'"))
                users = result_users.fetchone()
                con.commit()
            if users:
                update_at = datetime.now()
                updated_by = session['id']
                first_name = request.form['first_name']
                last_name = request.form['last_name']
                middle_name = request.form['middle_name']
                date_of_birth = request.form['dob']
                phone_number = request.form['phone']
                address = request.form['line1']
                city = request.form['city']
                state = request.form['state']
                zip_code = request.form['zip-code']
                country = request.form['country']
                email = request.form['email']
                role = request.form['role']
                with engine.connect() as con:
                    con.execute(text(f"UPDATE users SET updated_at = '{update_at}', updated_by = '{updated_by}',\
                                              first_name = '{first_name}', last_name = '{last_name}',\
                                                middle_name = '{middle_name}', date_of_birth = '{date_of_birth}',\
                                                phone_number = '{phone_number}', address = '{address}', city = '{city}',\
                                                state = '{state}', zip_code = '{zip_code}', country = '{country}',\
                                                email = '{email}', role ='{role}' WHERE unique_id = '{user_id}'"))
                    con.commit()
                msg = "User profile updated successfully"
                return render_template('home.html', msg=msg)
                
            else:
                #redirect to the home page
                msg = 'The user does not exist.'
                return redirect(url_for('home', msg = msg))

    
if __name__ == '__main__':
    app.run(debug=True)