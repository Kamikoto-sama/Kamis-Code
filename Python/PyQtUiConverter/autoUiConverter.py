import os
from time import sleep
from json import JSONEncoder, JSONDecoder

saveRegisteredFiles = True
dataStoreName = "registeredUiFiles.txt"
jsonEncoder = JSONEncoder(indent= 2)

sourceFilesPath = "ui"
outputFilePath = "ui/convertedUi"

def convertUi(fileName):
	print(f"{fileName} has changed")
	convertingConfig = f"{sourceFilesPath}//{fileName} -o {outputFilePath}//{fileName[:-3]}.py"
	code = os.system(f"python -m PyQt5.uic.pyuic -x " + convertingConfig)
	if code != 0:
		exit(code)

def monitorChanges():
	registeredFiles = getRegisteredFiles() if saveRegisteredFiles else {}
	while 1:
		for file in os.listdir(sourceFilesPath):
			if not file.endswith(".ui"):
				continue
			lastModifiedTime = os.path.getmtime(f"{sourceFilesPath}//{file}")
			if not file in registeredFiles or lastModifiedTime > registeredFiles[file]:
				registeredFiles[file] = lastModifiedTime
				convertUi(file)
				if saveRegisteredFiles:	
					saveChanges(registeredFiles)
		sleep(1)
		
def getRegisteredFiles():
	if not os.path.exists(dataStoreName):
		return {}
	with open(dataStoreName, 'r') as file:
		textData = file.read()
		return {} if len(textData) == 0 else JSONDecoder().decode(textData)
		
def saveChanges(files):
	filesData = jsonEncoder.encode(files)
	with open(dataStoreName, 'w') as dataStore:
		dataStore.write(filesData)
	
if __name__ == '__main__':
	monitorChanges()