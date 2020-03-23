from typing import List

def toEntity(rawEntities: List[dict], entityType: type):
	entities = [entityType(**rawEntity) for rawEntity in rawEntities]
	return entities
