import cv2

cap = cv2.VideoCapture('MouseMovies\Mouse Movie 5.avi')

filename = 'mouseMovement.avi'

ret, frame1 = cap.read()
ret, frame2 = cap.read()

fourcc = cv2.VideoWriter_fourcc(*'XVID')  
out = cv2.VideoWriter(filename, fourcc, 24.00, (1920, 1080))

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
        
        if cv2.contourArea(contour) < 5:
            continue
        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame1, "Status: {}".format('Movement'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 0, 255), 3)
    
    
    out.write(frame1)
    cv2.imshow("feed", frame1)
    frame1 = frame2
    ret, frame2 = cap.read()
    
    if frame2 is None or frame1 is None:
        break
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
          break
        
cap.release()
out.release()
cv2.destroyAllWindows()
