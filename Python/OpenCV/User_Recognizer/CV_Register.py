import cv2
import os

cam = cv2.VideoCapture(0)

face_detector = cv2.CascadeClassifier('face.xml')

# For each person, enter one numeric face id
face_id = input('\n user id:  ')

print("\n [INFO] Initializing face capture...")
# Initialize individual sampling face count
count = 0

while(True):

    ret, img = cam._read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)
    
    for (x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)     
        count += 1

        # Save the captured image into the datasets folder
        cv2.imwrite("Users/User." + str(face_id) + '.' + str(count) 
            + ".jpg", gray[y:y+h,x:x+w])

        cv2.putText(img,str(count)+'%',(x+5,y-5),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0))
        
    cv2.imshow('image', img)
    k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break
    elif count >= 100: # Take 30 face sample and stop video
         break

# Do a bit of cleanup
print("\n [INFO] Scanning complete")
cam.release()
cv2.destroyAllWindows()