import cv2

camera = cv2.VideoCapture(0)
cascades = cv2.CascadeClassifier('face.xml')
count = 0

while True:
	count+=1
	rat,frame = camera._read()
	gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

	faces = cascades.detectMultiScale(gray,1.3,5)

	for (x,y,w,h) in faces:
		cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)

		cv2.putText(frame,str(count)+'%',(x+5,y-5),
	            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0),2)
	cv2.imshow("Test",frame)

	k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
	if k == 27:
		break

camera.release()
cv2.destroyAllWindows()