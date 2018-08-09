import itertools

class Book:
	bookId = itertools.count()
	'''
	Params: 
		self - self, duh
		title - String for books title
		owner - User.id of book owner
		bio - What the owner wants to say about their book
	'''
	def __init__(self, title, owner, bio): 
		self.id = next(Book.bookId)
		self.title = title
		self.owner = owner
		self.bio = bio
		self.comments = []


