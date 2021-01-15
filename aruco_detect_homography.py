import numpy as np
import cv2
from cv2 import aruco

# videos that will be displayed
cap = cv2.VideoCapture('MVI_6739.mp4') # 0 for the webcam input
cap2 = cv2.VideoCapture('C:/Users/tpean/Downloads/besancon_drone.mp4')

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.mp4',fourcc, 20.0, (1920,1080))

# Output image with and height
w_img_dest = 1920
h_img_dest = 1080

w_img_src = 1920
h_img_src = 1080

# Define the homography matching parameters
pts_gauche = np.array([[0, 0, 1], [w_img_src, 0, 1], [w_img_src, h_img_src, 1], [0, h_img_src, 1]], dtype='float')
pts_droite = np.zeros((4,3), dtype='float')

# Defines two white frames to make a negative mask and display two images on the same output
one_frame_src = 255*np.ones((h_img_src, w_img_src, 3), dtype=np.uint8)
one_frame_dest = 255*np.ones((h_img_dest, w_img_dest, 3), dtype=np.uint8)

# AruCO definition
aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
parameters =  aruco.DetectorParameters_create()

while(cap.isOpened() and cap2.isOpened()):
    # Capture frame-by-frame
    ret1, frame = cap.read()
    ret2, frame2 = cap2.read()

    if not(ret1) or not(ret2):
        break 

    # Our operations on the frame come here. Aruco detects only on gray frames
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    # if the detection success
    if ids is not None:
        for i in range(len(ids)):
            c = corners[i][0]
            cv2.circle(frame,(c[:, 0].mean(), c[:, 1].mean()), 5, (255, 0, 0), -1) #quick check draws circles at the center of the markers
            # markers id must be arranged in an anti trigonometric way (top left, top right, bottom right, bottom left)
            #(too lazy to implement a faster way of rearanging the marker numbers)
            if ids[i][0] == 4:
                ids[i][0] = 0
            if ids[i][0] == 6:
                ids[i][0] = 1
            if ids[i][0] == 3:
                ids[i][0] = 2
            if ids[i][0] == 10:
                ids[i][0] = 3
            # put text to display the id number of the markers
            #cv2.putText(frame, str(ids[i][0]), (int(c[:, 0].mean()) + 10, int(c[:, 1].mean()) + 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)

        # if 4 markers are detected, carry on the homography
        if len(ids) == 4:
            #only takes the exterior corners of the markers
            for i in range(len(ids)):
                c = corners[i][0]
                # points must be stacked as homogeneous coordinates
                #cv2.circle(frame,(c[ids[i][0], 0], c[ids[i][0], 1]), 5, (255, 0, 0), -1)
                pts_droite[ids[i][0], 0] = c[ids[i][0], 0]
                pts_droite[ids[i][0], 1] = c[ids[i][0], 1]
                pts_droite[ids[i][0], 2] = 1

            # Find the homography between the detected corners and the video to patch
            M, mask = cv2.findHomography(pts_gauche, pts_droite, cv2.RANSAC,5.0)
            result = cv2.warpPerspective(frame2, M, (w_img_src, h_img_src))
            #mask the patched video on the displayed frame
            result2 = cv2.warpPerspective(one_frame_src, M, (w_img_dest, h_img_dest))
            result2 = one_frame_dest - result2
            cv2.bitwise_and(result2, frame, frame)
            frame += result

    #flips the webcam along the Y axis
    # Comment if not wanted
    #frame = cv2.flip(frame, 1)
    # Display the resulting frame
    
    out.write(frame)
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cap2.release()
out.release()
cv2.destroyAllWindows()