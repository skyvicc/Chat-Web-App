from flask import Flask, render_template, redirect, url_for, request, session
import sqlite3, hashlib, os
from datetime import timedelta

app = Flask(__name__, static_folder='static')
app.secret_key = os.urandom(16)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=120)

conn = sqlite3.connect('profiles.db')
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
""")
conn.commit()
conn.close()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('logIn.html')
@app.route('/signup')
def signup():
    return render_template('signUp.html')
#========================================================================
@app.route('/login_step', methods=['POST'])
def process_login():
    # get the login form data
    username = request.form['username']
    password = request.form['pass']
    stay_logged = request.form.get('stayLogged')
    conn = sqlite3.connect('profiles.db')
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()

    if result is None:
        conn.close()
        error = 'Invalid username or password'
        return render_template('logIn.html', error = error)
    else:
        hashed_password = result[0]
        hashed_input_password = hashlib.sha256(password.encode()).hexdigest()

        if hashed_input_password != hashed_password:
            conn.close()
            error = 'Invalid username or password'
            return render_template('logIn.html', error = error)
        else:
            session['username'] = username
            conn.close()

            session['logged_in'] = True
            session.modified =True
            return redirect(url_for('success'))
#------------------------------------------------------------------
@app.route('/register', methods=['POST'])
def process_signup():
    # code to process signup form data here
    username = request.form['username']
    password = request.form['password']
    password_confirm = request.form['password_confirm']
    stay_logged = request.form.get('stayLogged')
    conn = sqlite3.connect('profiles.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone() is not None:
        conn.close()
        error = 'Username already exists'
        return render_template('signUp.html', error = error)
    elif password != password_confirm:
        error = 'The passwords don\'t match'
        return render_template('signUp.html', error = error)
    else:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        session['username'] = username
        conn.close()
        return redirect(url_for('success'))
        
        
@app.route(f'/find')
def success():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    conn = sqlite3.connect('profiles.db')
    cursor = conn.cursor()
    cursor.execute('SELECT username FROM users')
    usernames = [row[0] for row in cursor.fetchall()]
    conn.close()
    user = session.get('username')
    del usernames[usernames.index(user)]
    return render_template('findSomeone.html', usernames=usernames, user=user)

if __name__ == '__main__':
    app.run()
