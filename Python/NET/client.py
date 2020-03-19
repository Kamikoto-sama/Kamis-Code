from dbProvider import DataBaseProvider

from NET.authenticationController import AuthenticationController

db = DataBaseProvider().getDbConnection()
controller = AuthenticationController(db)
res = controller.getUserByLogin("hello")
print(res)

if __name__ == '__main__':
	pass
