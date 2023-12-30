from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
import logging

app = Flask(__name__)
app.secret_key = 'root@123'

# Replace with your actual MySQL database configuration
db_config = {
    "host": "NITRO",
    "user": "root",
    "password": "root",
    "database": "login"
}

logging.basicConfig(level=logging.DEBUG)  # Use a proper logging configuration

def get_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            connection = get_connection()
            cursor = connection.cursor(dictionary=True)

            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))
            user = cursor.fetchone()

            cursor.close()
            connection.close()

            if user:
                # Successful login, store user in session and redirect to the home route
                session['user'] = {'id': user['id'], 'username': user['username']}
                return redirect(url_for('home'))
            else:
                error_message = "Login failed. The username and password do not match. Don't have an account? <a href='/signup'>Register now</a>."
                return render_template('index2.html', error=error_message)

        except mysql.connector.Error as err:
            logging.error("Error during login: %s", err)
            error_message = "An error occurred during login. Please try again."
            return render_template('index2.html', error=error_message)

    return render_template('index2.html')

@app.route('/home')
def home():
    return render_template('index2.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        logging.debug("Received signup POST request")
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        phone = request.form['phone']

        try:
            connection = get_connection()
            cursor = connection.cursor()

            # Replace 'users' with your actual table name
            query = "INSERT INTO users (username, password, email, phone) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (username, password, email, phone))
            connection.commit()
            logging.debug("Data committed to the database successfully")

            cursor.close()
            connection.close()

            # Redirect to login after successful signup
            return redirect(url_for('index'))
        except mysql.connector.Error as err:
            logging.error("Error during signup:", err)
            # Handle the case when the username is already taken
            return render_template('signup.html', error="An error occurred during signup. Please try again.")

    return render_template('signup.html')

@app.route('/index2')
def index2():
    # Check if the user is logged in
    if 'user' in session:
        user = session['user']
        return render_template('index2.html', username=user['username'])

    # If the user is not logged in, redirect to the login page
    return redirect(url_for('login'))

@app.route('/success')
def success():
    if 'user' in session:
        user = session['user']
        # You can render a success page or redirect to the main website
        return render_template('success.html', username=user['username'])
    else:
        # Redirect to login if the user is not in session
        return redirect(url_for('index'))
@app.route('/services')
def services():
    return render_template('services.html')
    # Your view logic here

@app.route('/location')
def location():
    # Your view logic goes here
    return render_template('location.html')



if __name__ == '__main__':
    app.run(debug=True)