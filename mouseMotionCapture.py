import cv2

#The video file is set to the variable 'cap', we can then manipulate it further
cap = cv2.VideoCapture('MouseMovies\playFile\MOV9BA.mp4')

#The output file's name, worth noting it will output to an avi file, this can
#be changed very simply by changing the format after the period.
filename = 'mouseMovement.avi'

#ret is a boolean value that returns true if the frame is available (feed is open)
ret, frame1 = cap.read()
ret, frame2 = cap.read()

#Framerate of videos is 30.00, any more or less and it will speed up or slow
#down the output video respectively. Change this value based on camera.
fourcc = cv2.VideoWriter_fourcc(*'XVID')  
out = cv2.VideoWriter(filename, fourcc, 30.00, (1920, 1080))

#initialize a contour counter for finding number of frames mouse is not on screen
contourCount = 0

#initialize a counter for setting to a certain number of frames since last contour
timerCount = 0

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
    
    #clock display on screen
    #if ret:
        # describe the type of
        # font you want to display
        #font = cv2.FONT_HERSHEY_SCRIPT_COMPLEX
 
        # Get date and time and
        # save it inside a variable
        #dt = str(datetime.datetime.now())
 
        # put the dt variable over the
        # video frame
        #frame = cv2.putText(frame1, dt,
                            #(10, 100),
                            #font, 1,
                            #(255, 0, 0),
                            #4, cv2.LINE_8)

#this is a block attempting to find all of the moments of movement and all of
#the movement within 100 frames of the first detected contour.    
    for contour in contours:        
        if len(contours) > 0:
            timerCount = 100
            out.write(frame1)
        elif len(contours) > 0 or timerCount > 0:
            out.write(frame1)
            timerCount -= 1
        elif len(contours) == 0 and timerCount < 0:
            continue
    
    if len(contours) > 0:
        contourCount += 1
        
    
#Draws rectangles around the movement
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        
#This line controls the accuracy of the contours, a smaller number results in
#smaller changes being recognized as movement. Larger number results in
#more movement required to be recognized.
        if cv2.contourArea(contour) < 120:
            #putting out.write here only writes when contours are present!
            continue
        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
#put timer logic in here?
        
#For every frame of the video, if there is a contour, only write out that frame.
#Need to work on a 'Tolerance' that allows for a minute after motion has stopped.
#If contour, start timer and begin capturing all frames, if no contour after
#1 minute, stop timer, stop capturing frames.



#working iteration
    #out.write(frame1)
    cv2.imshow("feed", frame1)
    frame1 = frame2
    ret, frame2 = cap.read()
    
    #If the video has ended, close the feed
    if frame2 is None or frame1 is None:
        break
    
    #If the ` key is pressed while the video is playing, it will write out the file and kill the video feed.
    if cv2.waitKey(1) & 0xFF == ord('`'):
          break
      
#Logic that finds the number of seconds a mouse is on screen and displays it
contourCount = contourCount / 30
print( "The number of seconds there is a moving mouse on screen is " + str(contourCount) + " seconds")

cap.release()
out.release()
cv2.destroyAllWindows()