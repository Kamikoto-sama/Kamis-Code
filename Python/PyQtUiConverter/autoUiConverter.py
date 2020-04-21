import os
from time import sleep
from json import JSONEncoder, JSONDecoder

# Config
saveRegisteredFiles = True
removeUnregisteredFiles = True
dataStoreName = "registeredUiFiles.txt"
jsonEncoder = JSONEncoder(indent= 2)
sourceFilesPath = "ui"
outputFilePath = "ui/convertedUi"
checkDelaySeconds = 1

def convertUi(fileName):
	print(f"Converting {fileName} ... ", end="\r")
	convertingConfig = f"{sourceFilesPath}//{fileName} -o {outputFilePath}//{fileName[:-3]}.py"
	code = os.system("python -m PyQt5.uic.pyuic -x " + convertingConfig)
	print(f"{fileName} has converted")
	if code != 0:
		exit(code)

def monitorChanges():
	print("Monitoring files...", end="\r")
	if saveRegisteredFiles:
		checkExistingOutputDir()
		registeredFiles = getRegisteredFiles()
	else:
		registeredFiles = {}
		
	while 1:
		checkedFiles, filesHaveChanged = checkUiFiles(registeredFiles)
		sleep(checkDelaySeconds)
		if removeUnregisteredFiles:
			filesHaveChanged = checkConvertedFiles(registeredFiles, checkedFiles, filesHaveChanged)
		if saveRegisteredFiles and filesHaveChanged:
			saveChanges(registeredFiles)
			
def checkExistingOutputDir():
	if not os.path.exists(outputFilePath):
		os.makedirs(outputFilePath)

def checkUiFiles(registeredFiles):
	sourceFiles = os.listdir(sourceFilesPath)
	filesHaveChanged = False
	checkedFiles = []
	for file in filter(lambda f: f.endswith(".ui"), sourceFiles):
		lastModifiedTime = os.path.getmtime(f"{sourceFilesPath}//{file}")
		if not file in registeredFiles or lastModifiedTime > registeredFiles[file]:
			registeredFiles[file] = lastModifiedTime
			convertUi(file)
			filesHaveChanged = True
		checkedFiles.append(file)
	return checkedFiles, filesHaveChanged
				
def checkConvertedFiles(registeredFiles, checkedFiles, filesHaveChanged):
	convertedFiles = os.listdir(outputFilePath)
	for file in filter(lambda f: f.endswith(".py"), convertedFiles):
		if (sourceFile := f"{file[:-3]}.ui") not in checkedFiles:
			os.remove(f"{outputFilePath}//{file}")
			registeredFiles.pop(sourceFile)
			print(f"Unregistered {file} has removed")
			filesHaveChanged = True
	return filesHaveChanged

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