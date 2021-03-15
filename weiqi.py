from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'weiqi'

# Intialize MySQL
mysql = MySQL(app)

# http://localhost:5000/pythonlogin/ - this will be the login page, we need to use both GET and POST requests
@app.route('/pythonlogin/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    
    # Check if "name" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form:
        # Create variables for easy access
        name = request.form['name']
        password = request.form['password']
        if not re.match(r'[0-9]{4}-[0-9]{2}-[0-9]{2}', password):
            msg = 'Invalid DOB!'
        else:
        
    # Check if account exists using MySQL
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM player WHERE name = %s AND dob = %s', (name, password,))
            print(f'SELECT * FROM player WHERE name = {name} AND dob = {password}')
            # Fetch one record and return result
            account = cursor.fetchone()
            print('account:',account)
            
            # If account exists in accounts table in out database
            if account:
                # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['name'] = account['name']
                # Redirect to home page
                return redirect(url_for('home'))
            else:
                # Account doesnt exist or name/password incorrect
                msg = 'Incorrect name/password!'
    return render_template('index.html', msg=msg)
    
# http://localhost:5000/python/logout - this will be the logout page
@app.route('/pythonlogin/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   #session.pop('id', None)
   session.pop('name', None)
   # Redirect to login page
   return redirect(url_for('login'))

# http://localhost:5000/pythinlogin/register - this will be the registration page, we need to use both GET and POST requests
@app.route('/pythonlogin/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "name", "password" and "ranking" POST requests exist (user submitted form)
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'ranking' in request.form:
        # Create variables for easy access
        name = request.form['name']
        password = request.form['password']
        ranking = request.form['ranking']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM player WHERE name = %s', (name,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[0-9]{4}-[0-9]{2}-[0-9]{2}', password):
            print('\n\npassword:',password, '\n\n')
            msg = 'Invalid DOB!'
        elif not re.match(r'[0-9]{2}[kdps]', ranking):
            msg = 'Invalid ranking!'
        #elif not re.match(r'[^@]+@[^@]+\.[^@]+', ranking):
        #    msg = 'Invalid ranking!'
        elif not re.match(r'[A-Za-z0-9]+', name):
            msg = 'name must contain only characters and numbers!'
        elif not name or not password or not ranking:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO player VALUES (%s, %s, %s, false, NULL, NULL, NULL)', (name, ranking, password, ))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)
    
# http://localhost:5000/pythinlogin/home - this will be the home page, only accessible for loggedin users
@app.route('/pythonlogin/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM player WHERE name <> %s', ('Le Heng2',))
        #account = cursor.fetchone()
        print(*(i[0] for i in cursor.description))
        data = cursor.fetchall()
        print('cursor:', data)
        # User is loggedin show them the home page
        return render_template('home.html', name=session['name'], data=data)
       
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))
    
# http://localhost:5000/pythinlogin/profile - this will be the profile page, only accessible for loggedin users
@app.route('/pythonlogin/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM player WHERE name = %s', (session['name'],))
        #account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account,
        data=cur.fetchall())
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))
    
if __name__=='__main__':
    print('starting :)')
    app.debug = True
    app.run()