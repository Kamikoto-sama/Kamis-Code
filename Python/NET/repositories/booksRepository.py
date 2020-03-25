from models import Book
from repositories.entityRepresentor import toEntity
from repositories.dataBaseController import DataBaseController

class BooksRepository(DataBaseController):
	def __init__(self, db):
		super().__init__(db)
		self.__tableName = "books"

	def getBooks(self, filterParams=None):
		rawBooks = self._read(self.__tableName, filterParams)
		return toEntity(rawBooks, Book)

	def addBook(self, book: Book):
		values = (book.id, book.name, book.genres, book.pageCount, 
				  book.authorId, book.publisherId, book.count, book.price)
		self._create(self.__tableName, values)

	def updateBookById(self, bookId, updatedValues: dict):
		params = f"id={bookId!r}"
		self._update(self.__tableName, updatedValues, params)

	def deleteBookById(self, bookId):
		params = f"id={bookId!r}"
		self._delete(self.__tableName, params)