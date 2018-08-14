# Copyright (c) 2018 Cole Nixon

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, 
# including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, 
# subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

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

