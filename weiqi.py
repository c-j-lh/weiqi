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
        cursor.execute('SELECT P.*, C.flag FROM player P, country C WHERE P.name<>%s and P.countryName=C.name', ('Le Heng2',))
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
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html',
        account=account,
        data=cursor.fetchall())
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/pythonlogin/player/<player>')
def player(player):
    # Check if user is loggedin
    print(f'player is {player}')
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT G.*, P1.countryName as blackFlag, P2.countryName as whiteFlag FROM game G, player P1, player P2 WHERE (G.playerNameBlack=%s or G.playerNameWhite=%s) and  G.playerNameBlack=P1.name and G.playerNameWhite=P2.name', (player, player))
        #games.execute("SELECT G.*, P1.countryName as blackFlag, P2.countryName as whiteFlag FROM game G, player P1, player P2 WHERE compname=%s and compiter=%s and G.playerNameBlack=P1.name and G.playerNameWhite=P2.name", (compname, compiter));
        
        age = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        age.execute("SELECT TIMESTAMPDIFF(YEAR,dob,CURDATE()) AS age, player.* from player where name=%s", (player,));
        dd = age.fetchone()
        #print(dd)
        
        data = cursor.fetchall()
        print('games:', data)
        #account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('player.html',
        age=dd,
        games=data,
        player=player)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))
    #return f'Hello, {s}!' 




@app.route('/pythonlogin/country/<country>')
def country(country):
    # Check if user is loggedin
    print(f'player is {player}')
    if 'loggedin' in session:
        info = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        info.execute('SELECT * FROM country WHERE name=%s', (country,))
        info = info.fetchone()
        
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM player WHERE countryname=%s', (country,))
        players = cursor.fetchall()
        print('players,', players)
        
        games = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        games.execute("""SELECT G.playerNameBlack, G.playerNameWhite, P1.countryName as blackFlag, P2.countryName as whiteFlag
FROM game G , player P1, player P2
where ( playerNameBlack in (SELECT name FROM player WHERE countryname=%s) 
	or playerNameWhite in (SELECT name FROM player WHERE countryname=%s) )
	and G.playerNameBlack=P1.name and G.playerNameWhite=P2.name
;""", (country, country));
        #FROM game G, player P1, player P2 WHERE compname=%s and compiter=%s and G.playerNameBlack=P1.name and G.playerNameWhite=P2.name
        games = games.fetchall()
        #print(dd)
        
        #print('games:', data)
        #account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('country.html',
        games=games,
        players=players,
        info=info)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))
    #return f'Hello, {s}!' 



@app.route('/pythonlogin/event/<compname>/<compiter>')
def event(compname, compiter):
    # Check if user is loggedin
    print(f'{compname} {compiter}')
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        info = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        info.execute('SELECT * FROM event WHERE compname=%s and compiter=%s', (compname, compiter))
        info = info.fetchone()
        print('info,', info)
        
        games = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        games.execute("SELECT G.*, P1.countryName as blackFlag, P2.countryName as whiteFlag FROM game G, player P1, player P2 WHERE compname=%s and compiter=%s and G.playerNameBlack=P1.name and G.playerNameWhite=P2.name", (compname, compiter));
        games = games.fetchall()
        print('GAMES', games)
        print('images/'+{'China':'cn', 'Japan':'jp', 'Korea':'kr', None:''}['China']+'.png')
        return render_template('event.html',
        games=games,
        info=info)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))
    #return f'Hello, {s}!' 


@app.route('/pythonlogin/game/<gameid>')
def game(gameid):
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        info = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        info.execute('SELECT G.*, P1.countryName as blackFlag, P2.countryName as whiteFlag FROM game G, player P1, player P2 WHERE id=%s and G.playerNameBlack=P1.name and G.playerNameWhite=P2.name', (gameid,))
        
        info = info.fetchone()
        print('info,', info)
        
        moves = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        moves.execute("SELECT * FROM move WHERE gameid=%s", (gameid,));
        moves = moves.fetchall()
        
        comments = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        comments.execute("SELECT * FROM comment WHERE gameidabout=%s", (gameid,));
        comments = comments.fetchall()
        print('comments', comments)
        
        return render_template('game.html',
        moves=moves,
        comments=comments,
        info=info)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))
    #return f'Hello, {s}!'
   
fstr = '''select m1.gameid
from move m1, move m2 -- , move m3
where m1.gameid=m2.gameid and m1.moveno < m2.moveno -- and m2.gameid=m3.gameid
	and (
		(m1.positionx=3 and m1.positiony=4 and m2.positionx=5 and m2.positiony=3)
        or (m1.moveno+1=m2.moveno and m1.positionx=17 and m1.positiony=4 and m2.positionx=15 and m2.positiony=3)
        or (m1.moveno+1=m2.moveno and m1.positionx=3 and m1.positiony=16 and m2.positionx=5 and m2.positiony=17)
        or (m1.moveno+1=m2.moveno and m1.positionx=17 and m1.positiony=16 and m2.positionx=15 and m2.positiony=17)
		
        or (m1.moveno+1=m2.moveno and m1.positionx=4 and m1.positiony=3 and m2.positionx=3 and m2.positiony=5)
        or (m1.moveno+1=m2.moveno and m1.positionx=4 and m1.positiony=17 and m2.positionx=3 and m2.positiony=15)
        or (m1.moveno+1=m2.moveno and m1.positionx=16 and m1.positiony=3 and m2.positionx=17 and m2.positiony=5)
        or (m1.moveno+1=m2.moveno and m1.positionx=16 and m1.positiony=17 and m2.positionx=17 and m2.positiony=15)
	);'''

def imageFor(country):
    print(f'country is {country}')
    games = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    games.execute('SELECT * FROM country WHERE name = %s', (country,))
    games = games.fetchone()
    print(games.flag)
    return url_for('static', filename='cn.png')
    
@app.route('/pythonlogin/joseki/')   
def joseki():
    # Output message if something goes wrong...
    msg = ''
    # Check if "name", "password" and "ranking" POST requests exist (user submitted form)
    games = []
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'ranking' in request.form:
        # Create variables for easy access
        coords = request.form['coords']
        
        # If account exists show error and validation checks
        try:
            coords = list(map(int, coords.split(' ')))
            print(coords)
            assert len(coords)==4  # %2 == 0
            
            games = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            games.execute('SELECT * FROM games WHERE id = %s', (1,))
            games = games.fetchall()
            msg = 'result'
        except:
            msg = 'Please enter pairs of coordinates'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('joseki.html', msg=msg, games=games)


if __name__=='__main__':
    print('starting :)')
    app.debug = True
    app.run()