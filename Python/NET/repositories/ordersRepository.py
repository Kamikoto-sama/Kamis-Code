from models import Order
from repositories.entityRepresentor import toEntity
from repositories.dataBaseController import DataBaseController

class OrdersRepository(DataBaseController):
	def __init__(self, db):
		super().__init__(db)
		self.__tableName = "orders"

	def addOrder(self, order: Order):
		values = (order.id, order.bookId, order.userId, order.date)
		self._create(self.__tableName, values)

	def getOrders(self, filterParams=None):
		rawAuthors = self._read(self.__tableName, filterParams)
		return toEntity(rawAuthors, Order)

	def deleteOrderById(self, orderId):
		params = f"id={orderId!r}"
		self._delete(self.__tableName, params)
		