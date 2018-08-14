# pip/Homebrew imports
from flask import Flask, request, render_template, flash, redirect, url_for, session, logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, IntegerField, TextAreaField, PasswordField, validators
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


#Comments = Comments() #dummy comments for now


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

@app.route('/about')
def about():
	return render_template('about.html')


#should be /<userid>/books, but we'll get there...
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
	

class PageForm(Form):
	currentPage = IntegerField('Current Page', [validators.NumberRange(min=1, max=999999)])


@app.route('/books/<int:id>', methods = ['GET', 'POST'])
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
			return render_template('book.html', book=book, comments=comments, pageForm=pageForm, currentPage=currentPage)
		else:
			msg = "No comments here yet! Be the first :)"
			return render_template('book.html', book=book, msg=msg, pageForm=pageForm, currentPage=currentPage)
	else:
		error = "There is no Book with this ID"
		return render_template('book.html', error=error)
	# Cant forget!
	cur.close()



# Cut this out
class CommentForm(Form):
	page = StringField('Page Number', [validators.Length(min=1, max=6)])
	body = TextAreaField('Comment Body', [validators.Length(min=1)])


@app.route('/book/<int:id>/add_comment', methods = ['GET', 'POST'])
@user_logged_in
def add_comment(id):
	form = CommentForm(request.form)
	if request.method == 'POST' and form.validate():
		page = form.page.data
		body = form.body.data

		# Create cursor
		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO comments(page, body, owner, userId, bookId) VALUES(%s, %s, %s, %s, %s)", (int(page), body, session['username'], int(session['userId']), int(id)))

		# Commit to DB
		mysql.connection.commit()

		# Close connection
		cur.close()

		flash('Comment Added', 'success')
		return redirect(url_for('book', id=id))

	return render_template('add_comment.html', form=form)





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

# Cut this out
class BookForm(Form):
	title = StringField('Book Title', [validators.Length(min=1, max=100)])
	author = StringField('Book Author', [validators.Length(min=1, max=50)])
	bio = TextAreaField('What would you like people to know about your book?', [validators.Length(min=30)])
	

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
		cur.execute("INSERT INTO books(title, author, bio, owner, userId) VALUES(%s, %s, %s, %s, %s)", (title, author, bio, session['username'], int(session['userId'])))

		# Commit to DB
		mysql.connection.commit()

		# Close connection
		cur.close()

		flash('Book Added', 'success')
		return redirect(url_for('books'))

	return render_template('add_book.html', form=form)




# First thing user sees upon login
@app.route('/dashboard')
@user_logged_in
def dashboard():
	return render_template('dashboard.html')

# Redirect to the home... 
@app.route('/logout')
@user_logged_in
def logout():
	session.clear()
	flash('Successfully logged out', 'success')
	return redirect(url_for('login'))
# Actual Script...
if __name__ == '__main__':
	app.secret_key='secret123'
	app.run(debug=True) #Debug mode turns on automatic server refresh on save







