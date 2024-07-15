# this file contain backup of prvious code in app.py


from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'mydb'
app.secret_key = 'your_secret_key'

# Function to connect to MySQL database


def connect():
    try:
        conn = mysql.connector.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            database=app.config['MYSQL_DB']
        )
        if conn.is_connected():
            print('Connected to MySQL database')
        return conn
    except Error as e:
        print(e)
        return None


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        conn = connect()
        if conn is not None:
            error = None
            if request.method == 'POST':
                # Get form data
                email = request.form['email']
                password = request.form['pswd']

                cursor = conn.cursor(dictionary=True)

                # Execute the SQL query to find the user
                cursor.execute(
                    'SELECT * FROM users WHERE email = %s AND password = %s', (email, password))
                user = cursor.fetchone()

                # Close the cursor
                cursor.close()
                conn.close()
                if user:
                    # Store user information in session
                    session['loggedin'] = True
                    session['id'] = user['user_id']
                    session['name'] = user['name']

                    # Redirect to dashboard
                    return redirect(url_for('dashboard'))
                else:
                    error = 'Invalid username or password',

            return render_template('login.html', error=error)
        else:
            return 'Error: Could not connect to the database', 500
    except Error as e:
        print(e)
        return 'Error: Login Failed', 500


@app.route('/register', methods=['GET', 'POST'])
def register():
    try:
        conn = connect()
        if conn is not None:
            if request.method == 'POST':
                # Get form data
                name = request.form['name']
                email = request.form['email']
                password = request.form['pswd']
                phone = request.form['phone']
                address = request.form['address']
                gender = request.form['gender']

                cursor = conn.cursor()

                # Execute the SQL query to insert data into the database
                cursor.execute('INSERT INTO users (name, email, password, phone, address, gender) VALUES (%s, %s, %s, %s, %s, %s)', (
                    name, email, password, phone, address, gender))
                conn.commit()
                cursor.close()
                conn.close()

                # Redirect to login page after registration
                return redirect(url_for('login'))

            return render_template('register.html')
        else:
            return 'Error: Could not connect to database', 500
    except Error as e:
        print(e)
        return 'Error: Registration failed', 500


@app.route('/dashboard')
def dashboard():
    # Check if the user is logged in
    if 'loggedin' in session:
        return f"Welcome to your dashboard, {session['name']}!"
    else:
        return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)
