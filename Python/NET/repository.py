from NET.models import User, Book

class Repository:
	def getUserByLogin(self, userLogin):
		pass
	
	def getOrders(self):
		pass
	
	def getAuthors(self, params):
		pass
	
	def getPublishers(self, params):
		pass
	
	def getBooks(self, params):
		pass
	
	def addUser(self, user: User):
		pass
	
	def addPublisher(self, obj):
		pass
	
	def addAuthor(self, obj):
		pass
	
	def addBook(self, book: Book):
		pass
	
	def deleteUserById(self, userId):
		pass
	
	def deleteBookById(self, bookId):
		pass
	
	def deleteAuthorById(self, id):
		pass
	
	def deletePublisherById(self, id):
		pass
	
	def deleteOrder(self, id):
		pass
	
	def updateBook(self, book: Book):
		pass