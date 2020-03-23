from models import User
from repositories.dataBaseController import DataBaseController
from repositories.entityRepresentor import toEntity

class UsersRepository(DataBaseController):
	def __init__(self, db):
		super().__init__(db)
		self.__tableName = "users"

	def getUserByLogin(self, userLogin):
		params = f"login={userLogin!r}"
		rawUsers = self._read(self.__tableName, params)
		if len(rawUsers) == 0:
			return None
		user = User(**(rawUsers[0]))
		return user
	
	def getAllUsers(self):
		rawUsers = self._read(self.__tableName)
		return toEntity(rawUsers, User)

	def registerUser(self, user: User):
		values = (user.id, user.login, user.password, user.role)
		self._create(self.__tableName, values)
		
	def deleteUserById(self, userId: int):
		params = f"id={userId!r}"
		self._delete(self.__tableName, params)