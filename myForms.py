from wtforms import Form, StringField, IntegerField, TextAreaField, PasswordField, validators

class PageForm(Form):
	currentPage = IntegerField('Current Page', [validators.NumberRange(min=1, max=999999)])


# Cut this out
class CommentForm(Form):
	page = StringField('Page Number', [validators.Length(min=1, max=6)])
	body = TextAreaField('Comment Body', [validators.Length(min=1)])


# Cut this out
class RegisterForm(Form):
	username = StringField('Username', [validators.Length(min=4, max=30)])
	email = StringField('Email', [validators.Length(min=6, max=50)])
	password = PasswordField('Password', [
		validators.DataRequired(),
		validators.EqualTo('confirm', message='Passwords do not match')
	])
	confirm = PasswordField('Confirm Password')

# Cut this out
class BookForm(Form):
	title = StringField('Book Title', [validators.Length(min=1, max=100)])
	author = StringField('Book Author', [validators.Length(min=1, max=50)])
	bio = TextAreaField('What would you like people to know about your book?', [validators.Length(min=30)])

