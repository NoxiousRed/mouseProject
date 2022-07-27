import cv2
import datetime

#The video file is set to the variable 'cap', we can then manipulate it further
cap = cv2.VideoCapture('MouseMovies\playFile\MOV9BA.mp4')

#The output file's name, worth noting it will output to an avi file, this can
#be changed very simply by changing the format after the period.
filename = 'mouseMovement.avi'

#object detection from stable camera
object_detector = cv2.createBackgroundSubtractorMOG2()

#Framerate of videos is 30.00, any more or less and it will speed up or slow
#down the output video respectively. Change this value based on camera.
fourcc = cv2.VideoWriter_fourcc(*'XVID')  
out = cv2.VideoWriter(filename, fourcc, 30.00, (1920, 1080))

#initialize a contour counter for finding number of frames mouse is not on screen
contourCount = 0

#ret is a boolean value that returns true if the frame is available (feed is open)
#While the video is playing in the feed, do the following:
#If the program finds a difference between the frame and the mask, it will draw a
#contour around where the difference is detected, making a "Motion detection"
while cap.isOpened:
    ret, frame = cap.read()
    
    #if frames are still occuring
    if ret == True:
        # Object detection
        mask = object_detector.apply(frame)
        _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
        for cnt in contours:
            #clock display on screen
            font = cv2.FONT_HERSHEY_SCRIPT_COMPLEX
            dt = str(datetime.datetime.now())
            frame = cv2.putText(frame, dt, (10, 100), font, 1, (255, 0, 0), 2, cv2.LINE_8)
            #Calculate area of contours and remove small elements (noise, things we don't want)
            area = cv2.contourArea(cnt)
            if area > 120:
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 225, 0), 2 )
                out.write(frame)
                contourCount += 1

    #If the video has ended, close the feed        
    else:
        break
    
    #display the feed and the mask as a pop-out window
    cv2.imshow("feed", frame)
    cv2.imshow("Mask", mask)    
    
    #If the ` key is pressed while the video is playing, it will write out the file and kill the video feed.
    if cv2.waitKey(1) & 0xFF == ord('`'):
        break
      
#Logic that finds the number of seconds a mouse is on screen and displays it
frameCount = float(cap.get(cv2.CAP_PROP_FRAME_COUNT))
secondsCount = float(frameCount / 30)
contourCount = float(contourCount / 30)

print( "The number of seconds there is a moving mouse on screen is " + 
      str(secondsCount - (secondsCount - contourCount)) + " seconds")

#closes the feed and the output video file
cap.release()
out.release()
cv2.destroyAllWindows()