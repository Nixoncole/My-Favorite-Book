# Some thoughts... Each book has a page associated with it. Page is created by owner of the book,
# when they put the sticker on it. Each subsequent person can post a comment that will appear when the current holder
# "reaches that page". Comments should include account information, commentary, page number, time, 
# (option to share location? This would paint a map of where the book has been?) 

#need to understand classes in python.
# 1 page per physical book, book has locations/map made my comments, comments, photo, information, and owner

def Comments():
	comments = [
		{
			'id': 1,
			'userID': 12345678, # Can we link this directly? Embed a link in the html layout?
			'pageNumber': 200,
			'body': 'I was amazed at how Kvothe survived in Tarbean despite the terrible circumstances.',
			'bookID': '1', # Should this be a hashed value? Definitely needs ot be unique
			'timestamp': 'TIMESTAMP'
		},
		{
			'id': 2,
			'userID': 87654321, # Can we link this directly? Embed a link in the html layout?
			'pageNumber': 50,
			'body': 'I loved the introduction.',
			'bookID': '1', # Should this be a hashed value? Definitely needs ot be unique
			'timestamp': 'TIMESTAMP'			
		},
		{
			'id': 3,
			'userID': 1234321, # Can we link this directly? Embed a link in the html layout?
			'pageNumber': 600,
			'body': 'Wow... Im speechless.',
			'bookID': '1', # Should this be a hashed value? Definitely needs ot be unique
			'timestamp': 'TIMESTAMP'			
		}
	]
	return comments
