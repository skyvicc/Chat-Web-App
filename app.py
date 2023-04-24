from flask import Flask, render_template, redirect, url_for, request, session 
import sqlite3

app = Flask(__name__, static_folder='static')

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

    # create a new database connection
    conn = sqlite3.connect('profiles.db')
    cursor = conn.cursor()

    # check if the username and password match the records in the database
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()

    if user is None:
        conn.close()
        return 'Invalid username or password'
    else:
        # set a session variable to keep the user logged in

        # close the database connection
        conn.close()

        # redirect the user to the home page
        return redirect(url_for('success'))


#------------------------------------------------------------------

@app.route('/register', methods=['POST'])
def process_signup():
    # code to process signup form data here
    username = request.form['username']
    password = request.form['password']
    password_confirm = request.form['password_confirm']
    stay_logged = request.form.get('stayLogged')

    # create a new database connection
    conn = sqlite3.connect('profiles.db')
    cursor = conn.cursor()

    # check if the username already exists in the database
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone() is not None:
        conn.close()
        return 'Username already exists'
    elif password != password_confirm:
        return 'The passes don\'t match'
    else:
        # insert the user data into the database
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()

        # close the database connection
        conn.close()

        # redirect the user to a success page
        return redirect(url_for('success'))

@app.route('/find')
def success():
        # create a new database connection
    conn = sqlite3.connect('profiles.db')
    cursor = conn.cursor()

    # execute a SELECT query to retrieve usernames from the database
    cursor.execute('SELECT username FROM users')
    usernames = [row[0] for row in cursor.fetchall()]

    # close the database connection
    conn.close()

    # render the findSomeone.html template with the usernames variable
    return render_template('findSomeone.html', usernames=usernames)


if __name__ == '__main__':
    app.run(debug=True)
