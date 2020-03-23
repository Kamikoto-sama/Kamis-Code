from models import Publisher
from repositories.dataBaseController import DataBaseController
from repositories.entityRepresentor import toEntity


class PublishersRepository(DataBaseController):
	def __init__(self, db):
		super().__init__(db)
		self.__tableName = "publishers"

	def addPublisher(self, publisher: Publisher):
		values = (publisher.id, publisher.name, publisher.creationDate)
		self._create(self.__tableName, values)

	def getPublisher(self, filterParams=None):
		rawPublishers = self._read(self.__tableName, filterParams)
		return toEntity(rawPublishers, Publisher)

	def updatePublisherById(self, publisherId, updatedValues: dict):
		params = f"id={publisherId!r}"
		self._update(self.__tableName, updatedValues, params)

	def deletePublisherById(self, publisherId):
		params = f"id={publisherId!r}"
		self._delete(self.__tableName, params)