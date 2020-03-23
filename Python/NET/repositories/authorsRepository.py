from models import Author
from repositories.entityRepresentor import toEntity
from repositories.dataBaseController import DataBaseController

class AuthorsRepository(DataBaseController):
	def __init__(self, db):
		super().__init__(db)
		self.__tableName = "authors"
		
	def addAuthor(self, author: Author):
		values = (author.id, author.name, author.birthDate, author.bio)
		self._create(self.__tableName, values)

	def getAuthors(self, filterParams=None):
		rawAuthors = self._read(self.__tableName, filterParams)
		return toEntity(rawAuthors, Author)
		
	def updateAuthorById(self, authorId, updatedValues: dict):
		params = f"id={authorId!r}"
		self._update(self.__tableName, updatedValues, params)
		
	def deleteAuthorById(self, authorId):
		params = f"id={authorId!r}"
		self._delete(self.__tableName, params)