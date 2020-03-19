from sqlite3 import Connection
from dataBaseController import DataBaseController
from models import User

class AuthenticationController(DataBaseController):
	def __init__(self, db: Connection):
		super().__init__(db)

	def getUserByLogin(self, userLogin):
		params = f"login={userLogin!r}"
		result = self.get("users", params)
		if len(result) == 0:
			return None
		user = User(**(result[0]))
		return user

	def registerUser(self, user: User):
		values = (user.login, user.password, user.access)
		self.add("users", values)