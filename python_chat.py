from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    return render_template('logIn.html')

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/log', methods=['POST'])
def log():
    username = request.form['username']
    password = request.form['password']
    stay_logged = request.form.get('stayLogged')

    # create a new database connection
    conn = sqlite3.connect('profiles.db')
    cursor = conn.cursor()

    # check if the username already exists in the database
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone() is not None:

        return redirect(url_for('success'))
    if password != password_confirm:
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
    return render_template('findSomeone.html')
if __name__ == '__main__':
    app.run(debug=True)
