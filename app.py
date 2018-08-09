# pip/Homebrew imports
from flask import Flask, request, render_template, flash, redirect, url_for, session, logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt

# Personal imports
from comments import Comments


app = Flask(__name__)

Comments = Comments() #dummy comments for now

@app.route('/')
def index():
	return render_template('home.html')



# Actual Script...
if __name__ == '__main__':
	app.run(debug=True) #Debug mode turns on automatic server refresh on save