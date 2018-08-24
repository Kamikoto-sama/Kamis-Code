import cv2

def Detect_Faces(imagePath):
	image = cv2.imread(imagePath)
	cascades = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

	gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

	faces = cascades.detectMultiScale(
	gray,
	scaleFactor = 1.1,
	minNeighbors = 5,
	minSize = (30,30)
		)

	for (x,y,w,h) in faces:
		cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,255),2)

	cv2.imwrite("image.png",image)