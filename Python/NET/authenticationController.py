from sqlite3 import Connection

from .dataBaseController import DataBaseController

class AuthenticationController(DataBaseController):
	def __init__(self, db: Connection):
		super().__init__(db)

	def getUserByLogin(self, userLogin):
		params = f"login={userLogin!r}"
		res = self.get("users", params)
		result = list(self.toDictObj("users", res))
		return result[0] if len(result) > 0 else None
