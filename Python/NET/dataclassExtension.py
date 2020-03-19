from dataclasses import dataclass

def toDict(obj: dataclass):
	return {attr:getattr(obj, attr) for attr in obj.__annotations__}