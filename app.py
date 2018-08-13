# pip/Homebrew imports
from flask import Flask, request, render_template, flash, redirect, url_for, session, logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps

# Personal imports
from comments import Comments


app = Flask(__name__)


# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_DB'] = 'my_favorite_book'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Init MySQL
mysql = MySQL(app)


Comments = Comments() #dummy comments for now


# Access Control
# Maybe change default to 'Home'
# Rip this out?
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
	return render_template('home.html')

#should be /<userid>/books, but we'll get there...
@app.route('/books')
@user_logged_in
def books():
	return render_template('booksHome.html')

@app.route('/books/<int:id>')
@user_logged_in
def book(id):
	# grab comments from MySQL
	return render_template('book.html', id=id, comments=Comments)

@app.route('/login', methods = ['GET', 'POST'])
def login():
	if request.method == 'POST':
		#Get the form fields
		username = request.form['username']
		password_attempt = request.form['password']

		# Get user by username
		cur = mysql.connection.cursor()
		result = cur.execute("SELECT * FROM users WHERE username = %s", [username])

		if result > 0:
			data = cur.fetchone()
			password = data['password']
			if sha256_crypt.verify(password_attempt, password):
				app.logger.info('PASSWORD MATCHED') #remove later...
				session['logged_in'] = True
				session['username'] = username


				flash('You are logged in', 'success')
				return redirect(url_for('dashboard'))

			else:
				error = "Invalid Login"
				return render_template('login.html', error=error)
			cur.close()
		else:
			app.logger.info('NO USER')
			error = "Invalid Login"
			return render_template('login.html', error=error)

	return render_template('login.html')


# Cut this out
class RegisterForm(Form):
	username = StringField('Username', [validators.Length(min=4, max=30)])
	email = StringField('Email', [validators.Length(min=6, max=50)])
	password = PasswordField('Password', [
		validators.DataRequired(),
		validators.EqualTo('confirm', message='Passwords do not match')
	])
	confirm = PasswordField('Confirm Password')

# User Registration
@app.route('/register', methods=['GET', 'POST'])
def register():
	form = RegisterForm(request.form)
	if request.method == 'POST' and form.validate():
		#register user
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

# First thing user sees upon login
@app.route('/dashboard')
@user_logged_in
def dashboard():
	return render_template('dashboard.html')

# Redirect to the home... 
@app.route('/logout')
def logout():
	session.clear()
	flash('Successfully logged out', 'success')
	return redirect(url_for('login'))
# Actual Script...
if __name__ == '__main__':
	app.secret_key='secret123'
	app.run(debug=True) #Debug mode turns on automatic server refresh on save







