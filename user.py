from book import Book
import itertools

class User:
	userId = itertools.count()
	def __init__(self, email, username, password):
		self.id = next(User.userId)
		self.email = email
		self.username = username
		self.password = password
		self.books = []
		self.comments = []

	def addBook(self, book):
		self.books.append(book)

	def addComment(self, comment):
		self.comments.append(comment)
