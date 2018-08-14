# My Favorite Book

An application meant to connect people over your personal copy of your favorite book. 

## Author

Cole Nixon

cnixon@pdx.edu

## License

Copyright (C) 2018 Cole Nixon

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated docuementation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software. 

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANT OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, WRISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


## Description

My Favorite Book is an application inspired by the Little Free Libraries around Portland. The idea was to inspire a new way of sharing a book, by sharing the experience of reading the same copy of a book. I, as a book lover could enroll any number of my books into the application, where my book would now have a designated page for people to discuss various parts of the book. This page includes a place for you as the owner to share a bit about yourself or the book. To access this page for the first time, the holder of the book scans a QR code (downloaded within application) and can then register an account. To avoid spoilers, the viewer must enter their current page number to view comments. Comments will only be shown for pages leading up to what the user entered. Since everyone shares the same book, this eliminates the issue of different editions. 

Future implementation goals for this application are to include the location of a book when it is scanned/commented on, to provide a map of everywhere the book has traveled. Another ambition I have for this is to include the ability to upload images to the book's page, allowing commentors to share the journey of the book in more ways than one.

## Issue Tracker
```
https://github.com/Nixoncole/My-Favorite-Book/issues
```

## Usage

### Clone via HTTPS
```
git clone https://github.com/Nixoncole/My-Favorite-Book.git
cd My-Favorite-Book
```
### Setup Environment
NOTES: This is the work flow for Linux, similar instructions apply for MacOS.
If using Python 3, version 3.3 or higher is required for Flask
```
sudo apt-get python3-pip
sudo apt-get install mysql-server libmysqlclient-dev
pip install flask
pip install flask-mysqldb
pip install Flask-WTF
pip install passlib
pip install requests
```

Finally, run MySQL as the root user and create a database for the application to acccess, I named mine "my_favorite_book".
```
mysql -u root
mysql> create database {DB_Name_Here};
```

### Running Application
After you have your MySQL database, run the application by navigating to the directory where you cloned the repo and type
```
python app.py {DB_Name_Here}
```

You should be off and running!