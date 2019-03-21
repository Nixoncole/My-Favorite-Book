# Copyright (c) 2018 Cole Nixon

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, 
# including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, 
# subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


# pip/Homebrew imports
from flask import Flask, request, render_template, flash, redirect, url_for, session, logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, IntegerField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps

import requests, sys, json, re

# Personal imports

from myForms import PageForm, CommentForm, RegisterForm, BookForm, OrderForm
from keys import pwinty_id, pwinty_key, maps_key

if len(sys.argv) != 2:
    print("\tThis program expects a single argument, <databaseName> to be passed in.\n")
    print("\tPlease execute with format    :\t python app.py <databaseName>")
    sys.exit()


pwinty_headers = {'Content-type': 'application/json',
                  'accept': 'application/json',
                  'X-Pwinty-MerchantId': pwinty_id,
                  'X-Pwinty-REST-API-Key': pwinty_key
                  }

baseurl = "https://sandbox.pwinty.com/v3.0"
order_p = "/orders"
image_p = "/orders/{}/images"
order_status_p = "/orders/{}/SubmissionStatus"
order_submission_p = "/orders/{}/status"

app = Flask(__name__)

# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_DB'] = sys.argv[1]
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Init MySQL
mysql = MySQL(app)

start_up = 0


# Wraps for Access control
def user_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please Login', 'danger')
            return redirect(url_for('login'))

    return wrap


@app.route('/')
def index():
    global start_up
    if start_up == 0:
        cursorOnInit = mysql.connection.cursor()
        try:
            cursorOnInit.execute("SELECT * from USERS")
        except:
            cursorOnInit.execute(
                "CREATE TABLE users(id INT(11) auto_increment primary key, email VARCHAR(100), username VARCHAR(30), password VARCHAR(100), register_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
            cursorOnInit.execute(
                "CREATE TABLE books(id INT(11) auto_increment primary key, title VARCHAR(100), bio TEXT, author VARCHAR(50), owner VARCHAR(100), userId INT(11), FOREIGN KEY(userId) REFERENCES users(id) ON DELETE CASCADE, date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
            cursorOnInit.execute(
                "CREATE TABLE comments(id INT(11) auto_increment primary key, page INT(6) NOT NULL, body TEXT, owner VARCHAR(100), userId INT(11), FOREIGN KEY(userId) REFERENCES users(id) ON DELETE CASCADE, bookId INT(11), FOREIGN KEY(bookId) REFERENCES books(id) ON DELETE CASCADE, date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP, lat FLOAT(10,7), lng FLOAT(10,7)) ")
        start_up = 1

    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


# All books a user has control over
@app.route('/books')
@user_logged_in
def books():
    # Get the books
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM books WHERE userId = %s", [session['userId']])

    if result > 0:
        allbooks = cur.fetchall()
        return render_template('booksHome.html', allbooks=allbooks)

    else:
        msg = 'No Books for you!'
        return render_template('booksHome.html', msg=msg)
    # Close it
    cur.close()


# Page for a book
@app.route('/books/<int:id>', methods=['GET', 'POST'])
@user_logged_in
def book(id):
    # Set variable for page to filter comments
    currentPage = 0
    pageForm = PageForm(request.form)
    if request.method == 'POST' and pageForm.validate():
        currentPage = pageForm.currentPage.data

    # grab comments from MySQL
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM books WHERE id = %s", [id])

    if result > 0:
        book = cur.fetchone()
        result = cur.execute("SELECT * FROM comments WHERE bookId = %s ORDER BY page", [book['id']])

        if result > 0:
            comments = cur.fetchall()
            return render_template('book.html', book=book, comments=comments, pageForm=pageForm,
                                   currentPage=currentPage, maps_key=maps_key)
        else:
            msg = "No comments here yet! Be the first :)"
            comments = ''
            return render_template('book.html', book=book, msg=msg, comments=comments, pageForm=pageForm,
                                   currentPage=currentPage, maps_key=maps_key)
    else:
        error = "There is no Book with this ID"
        return render_template('book.html', error=error, maps_key=maps_key)
    # Cant forget!
    cur.close()


# Add a comment
@app.route('/book/<int:id>/add_comment', methods=['GET', 'POST'])
@user_logged_in
def add_comment(id):
    form = CommentForm(request.form)
    if request.method == 'POST' and form.validate():
        page = form.page.data
        body = form.body.data
        coords = re.sub('[()]', '', form.location.data)
        latLng = coords.split(', ')

        # Create cursor
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO comments(page, body, owner, userId, bookId, lat, lng) VALUES(%s, %s, %s, %s, %s, %s, %s)",
                    (int(page), body, session['username'], int(session['userId']), int(id), float(latLng[0]), float(latLng[1])))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        flash('Comment Added', 'success')
        return redirect(url_for('book', id=id))

    return render_template('add_comment.html', form=form, maps_key=maps_key)


# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get the form fields
        username = request.form['username']
        password_attempt = request.form['password']

        # Get user by username
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM users WHERE username = %s", [username])

        if result > 0:
            data = cur.fetchone()
            password = data['password']
            if sha256_crypt.verify(password_attempt, password):
                session['logged_in'] = True
                session['username'] = username
                session['userId'] = data['id']

                flash('You are logged in', 'success')
                return redirect(url_for('index'))

            else:
                error = "Invalid Login"
                return render_template('login.html', error=error)
            cur.close()
        else:
            app.logger.info('NO USER')
            error = "Invalid Login"
            return render_template('login.html', error=error)

    return render_template('login.html')


# User Registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        # register user
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # Create cursor
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(email, username, password) VALUES(%s, %s, %s)", (email, username, password))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        flash('You are now registered and can log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/add_book', methods=['GET', 'POST'])
@user_logged_in
def add_book():
    form = BookForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        author = form.author.data
        bio = form.bio.data
        # Create cursor
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO books(title, author, bio, owner, userId) VALUES(%s, %s, %s, %s, %s)",
                    (title, author, bio, session['username'], int(session['userId'])))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        flash('Book Added', 'success')
        return redirect(url_for('books'))

    return render_template('add_book.html', form=form)


@app.route('/qr/<int:id>', methods=['GET', 'POST'])
@user_logged_in
def qrdl(id):
    form = OrderForm(request.form)
    if request.method == 'POST' and form.validate():
        order_data = {'countryCode': 'US',
                      'recipientName': form.name.data,
                      'address1': form.address.data,
                      'addressTownOrCity': form.address.data,
                      'stateOrCounty': form.state.data,
                      'postalOrZipCode': form.zip.data,
                      'preferredShippingMethod': 'Budget'}
        order_resp = requests.post(baseurl + order_p, headers=pwinty_headers, json=order_data)
        if order_resp.status_code == 200:
            order_id = json.loads(order_resp.text)['data']['id']
            image_path = image_p.format(order_id)
            image_data = {'orderId': order_id,
                            'sku': "M-STI-3X4",
                            'copies': 1,
                            'size': 'ShrinkToFit',
                            'url': 'https://api.qrserver.com/v1/create-qr-code/?data=http://localhost:5000/book/'+str(id)+'size=600x600'
                            }
            image_resp = requests.post(baseurl+image_path, headers=pwinty_headers, json=image_data)
            if image_resp.status_code == 200:
                order_status_path = order_status_p.format(order_id)
                status_resp = requests.get(baseurl+order_status_path, headers=pwinty_headers)
                if json.loads(status_resp.text)['data']['isValid'] == True:
                    # finalize order
                    order_submission_path = order_submission_p.format(order_id)
                    wow = requests.post(baseurl+order_submission_path, headers=pwinty_headers, json={'status': 'Submitted'})
                    if wow.status_code == 200:
                        flash('Order Successfully Submitted. Order ID: '+str(order_id), 'success')

        return redirect(url_for('books'))
    return render_template('order_sticker.html', form=form)


# Redirect to the home...
@app.route('/logout')
@user_logged_in
def logout():
    session.clear()
    flash('Successfully logged out', 'success')
    return redirect(url_for('login'))


# Actual Script...
if __name__ == '__main__':
    app.secret_key = 'secret123'

    app.run(debug=True)  # Debug mode turns on automatic server refresh on save
