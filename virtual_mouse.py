import cv2
import time
import autopy
import numpy as np
import mediapipe as mp
import hand_tracking_module as htm
from screeninfo import get_monitors

# Variable Declaration
fReduction = 300
sReduction = 450
threshold_distance = 50
threshold_distance_1 = 60
threshold_distance_2 = 50
threshold_distance_3 = 30
smoothening = 20
wCam, hCam = 1280, 720
threshold_distance_3 = 45
wScreen, hScreen = autopy.screen.size()
prev_time=0
prev_locationX, prev_locationY = 0,0
curr_locationX, curr_locationY = 0,0
mbtgl = False
tgl = False
stgl = False
video_capture = cv2.VideoCapture(0)
video_capture.set(3, wCam)
video_capture.set(4, hCam)
detector = htm.handDetector(maxHands=1)

while True:
     _, img = video_capture.read()
     img = cv2.flip(img, 1)

     # Find hand landmarks
     img = detector.findHands(img)
     landmark_list, bbox = detector.findPosition(img, 0, False)

     # Get the tip of the Thumb
     if landmark_list:
        x1, y1 = landmark_list[4][1:]
        x2, y2 = landmark_list[4][1:]
        x3, y3 = landmark_list[20][1:]
         # Check which fingers are up
        fingers = detector.findFingersUp()
         # Create the cursor pad rectangle
        cv2.rectangle(img, (sReduction, fReduction), (wCam-sReduction, hCam-fReduction), (255,0,255), 2)

        distance_4amd_20, img, vertices = detector.findDistance(4, 20, img)     
       #  print(distance_4amd_20)
        #  print(wScreen, hScreen)
         # If all fingers up -> Moving Mode and if pinky of right hand down pause the moving
        if fingers[0] and fingers[1] and fingers[2] and fingers[3] and fingers[4] == False and stgl == False or stgl == True:
         stgl = True;
         if distance_4amd_20 >= 140 and x1 < x3:
            # Convert Coordinates
             x3 = np.interp(x1, (sReduction, wCam-sReduction), (0, wScreen))
             y3 = np.interp(y1, (fReduction, hCam-fReduction), (0, hScreen))

            # Smoothen the values -> so that it doesn't flicker much
             curr_locationX = prev_locationX + (x3-prev_locationX)/ smoothening
             curr_locationY = prev_locationY + (y3-prev_locationY)/ smoothening
            #  print(fingers[0], fingers[1], fingers[2], fingers[3], fingers[4])

            # Move mouse
             autopy.mouse.move(curr_locationX, curr_locationY)
            #  cv2.circle(img, (x1, y1), 3, (255,0,0), cv2.FILLED)
             prev_locationX, prev_locationY = curr_locationX, curr_locationY
            # Declaration of distance between finger landmark
             distance, img, vertices_0 = detector.findDistance(8, 6, img)
            #  print("Distance:",distance)
             distance_1, img, vertices_1 = detector.findDistance(12, 10, img)
            #  print("Distance 1:",distance_1)
             distance_2, img, vertices_2 = detector.findDistance(16, 14, img)
             distance_3, img, vertices_3 = detector.findDistance(8, 16, img)
             distance_4, img, vertices_4 = detector.findDistance(20, 15, img)
            #  print(distance_3, distance_3 <=threshold_distance_3)
         #  Index tip bend -> Clicking Mode  && index tip touch ring tip -> Double Click  
             if distance_3 <=threshold_distance_3:
                cv2.circle(img, (vertices_3[-2], vertices_3[-1]), 15, (0,255,0), cv2.FILLED)
                autopy.mouse.click(autopy.mouse.Button.LEFT);autopy.mouse.click(autopy.mouse.Button.LEFT)
               #  print("2")
             elif distance < threshold_distance:
                cv2.circle(img, (vertices_0[-2], vertices_0[-1]), 15, (0,255,0), cv2.FILLED)
                autopy.mouse.click(autopy.mouse.Button.LEFT);
               #  print("1")
         #  Finger tip over ring finger mid -> Drag
             if distance_4 <= threshold_distance_3 and tgl == False:
                cv2.circle(img, (vertices_4[-2], vertices_4[-1]), 15, (0,255,0), cv2.FILLED)
                autopy.mouse.toggle(autopy.mouse.Button.LEFT, True)
               #  print("2 drag")
                tgl = True
             elif distance_4 > threshold_distance_3 and tgl == True:
                cv2.circle(img, (vertices_4[-2], vertices_4[-1]), 15, (0,255,0), cv2.FILLED)
                autopy.mouse.toggle(autopy.mouse.Button.LEFT, False)
                tgl = False
         #  Middle finger tip bend -> Right Click
             if distance_1 < threshold_distance_1:
                cv2.circle(img, (vertices_1[-2], vertices_1[-1]), 15, (0,255,0), cv2.FILLED)
                autopy.mouse.click(autopy.mouse.Button.RIGHT)
         #  If ring finger tip down ->  Middle click for scroll
             if distance_2 < threshold_distance_2 and mbtgl == False:
                cv2.circle(img, (vertices_2[-2], vertices_2[-1]), 15, (0,255,0), cv2.FILLED)
                autopy.mouse.toggle(autopy.mouse.Button.MIDDLE, True);
                mbtgl = True
             elif distance_2 > threshold_distance_2 and mbtgl == True:
                cv2.circle(img, (vertices_2[-2], vertices_2[-1]), 15, (0,0,255), cv2.FILLED)
                autopy.mouse.toggle(autopy.mouse.Button.MIDDLE, False);
                mbtgl = False
         elif fingers[0] == False and fingers[1] == False and fingers[2] == False and fingers[3] == False and fingers[4] == False:
               #  print("O")
                stgl = False;
         else:
            autopy.mouse.toggle(autopy.mouse.Button.MIDDLE, False)
            

     # FPS
     curr_time = time.time()
     fps = 1/(curr_time-prev_time)
     prev_time = curr_time
     cv2.putText(img, f'FPS:{int(fps)}', (10, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 3)
     # Display
   #   cv2.imshow("Camera Cv", img)
     cv2.waitKey(1)