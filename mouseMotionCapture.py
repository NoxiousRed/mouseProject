import cv2

#The video file is set to the variable 'cap', we can then manipulate it further
cap = cv2.VideoCapture('MouseMovies\Mouse Movie 5.avi')

#The output file's name, worth noting it will output to an avi file, this can
#be changed by changing the format file after the dot in the below line of code
filename = 'mouseMovement.avi'

#ret is a boolean value that returns true if the frame is available
ret, frame1 = cap.read()
ret, frame2 = cap.read()


fourcc = cv2.VideoWriter_fourcc(*'XVID')  
out = cv2.VideoWriter(filename, fourcc, 60.00, (1920, 1080))

#While the video is playing in the feed, do the following:
#If the program finds a difference between frame1 and frame2, it will draw a
#contour around where the difference is detected, making a "Motion detection"
while cap.isOpened():
    print(frame1, frame2)
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        
        if cv2.contourArea(contour) < 130:
            continue
        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
    out.write(frame1)
    cv2.imshow("feed", frame1)
    frame1 = frame2
    ret, frame2 = cap.read()
    
    #If the video has ended
    if frame2 is None or frame1 is None:
        break
    
    #If the ` key is pressed while the video is playing, it will write out the file and kill the video feed.
    if cv2.waitKey(1) & 0xFF == ord('`'):
          break
        
cap.release()
out.release()
cv2.destroyAllWindows()
