from sys import modules
from dataclasses import dataclass

@dataclass
class User:
	login:str
	password:str
	role:str
	id:int=None
	
@dataclass
class Author:
	name:str
	birthDate:str
	bio:str
	id:int=None

@dataclass
class Order:
	bookId:int
	userId:int
	date:str
	id:int=None
	
@dataclass
class Book:
	name:str
	genres:str
	pageCount:int
	authorId:int
	publisherId:int
	count:int
	price:int
	id:int=None
	
@dataclass
class Publisher:
	name:str
	creationDate:str
	id:int=None
	
class ClientInfo:
	def __init__(self, rawClientInfo):
		self.connection = rawClientInfo[0]
		rawAddress = rawClientInfo[1]
		self.ipAddress = rawAddress[0]
		self.port = rawAddress[1]
		self.fullAddress = f"{self.ipAddress}:{self.port}"

class Request:
	def __init__(self, action, entityTypeName, rawEntity):
		self.action = action
		thisModule = modules[__name__]
		self.entity = getattr(thisModule, entityTypeName)(**rawEntity)