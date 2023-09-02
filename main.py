import cv2
import numpy as np

cap = cv2.VideoCapture(0)
upper_color = np.array([35, 255, 255])
lower_color = np.array([10, 192, 192])
kernel = np.ones((5,5),np.uint8)
points = []

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_color, upper_color)
    mask=cv2.erode(mask,kernel,iterations=2)
    mask=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernel)
    mask=cv2.dilate(mask,kernel,iterations=1)
    cnts,foo = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(cnts) > 0:
        cnt = sorted(cnts, key=cv2.contourArea, reverse=True)[0]
        ((x,y), r)=cv2.minEnclosingCircle(cnt)
        points.append({'x':int(x),'y':int(y)})
    
    for point in points:
        cv2.circle(frame,(point['x'],point['y']), 5, (255,0,0), -1)
    
    #res = cv2.bitwise_and(frame, frame, mask=mask)
    cv2.imshow('frame',frame)

    #cv2.imshow('mask', mask)
    #cv2.imshow('res', res)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()