import numpy as np
import cv2
from cv2 import aruco
import sys

filename1 = 0
filename2 = 'video_input/gif_input.gif'

extension = filename2[len(filename2)-3:len(filename2)]

# videos that will be displayed
cap = cv2.VideoCapture(filename1) # 0 for the webcam input
cap2 = cv2.VideoCapture(filename2)

# Uncomment the two lines below to save the result as a mp4 file
#fourcc = cv2.VideoWriter_fourcc(*'XVID')
#out = cv2.VideoWriter('output.mp4',fourcc, 20.0, (1920,1080))

ret1, frame = cap.read()
ret2, frame2 = cap2.read()

# Output image with and height
w_img_dest = frame.shape[1]
h_img_dest = frame.shape[0]

w_img_src = frame2.shape[1]
h_img_src = frame2.shape[0]

# Define the homography matching parameters
pts_gauche = np.array([[0, 0, 1], [w_img_src, 0, 1], [w_img_src, h_img_src, 1], [0, h_img_src, 1]], dtype='float')
pts_droite = np.zeros((4,3), dtype='float')

# Defines two white frames to make a negative mask and display two images on the same output
one_frame_src = 255*np.ones((h_img_src, w_img_src, 3), dtype=np.uint8)
one_frame_dest = 255*np.ones((h_img_dest, w_img_dest, 3), dtype=np.uint8)

# AruCO definition
aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
parameters =  aruco.DetectorParameters_create()

while(1):
    # Capture frame-by-frame
    ret1, frame = cap.read()
    ret2, frame2 = cap2.read()

    if not(ret1) or not(ret2):
        if extension != 'gif':
            break
        else:
            cap2.release()
            cap2 = cv2.VideoCapture(filename2)
            ret2, frame2 = cap2.read()


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
            if ids[i][0] == 8:
                ids[i][0] = 0
            if ids[i][0] == 7:
                ids[i][0] = 1
            if ids[i][0] == 11:
                ids[i][0] = 2
            if ids[i][0] == 12:
                ids[i][0] = 3
            # put text to display the id number of the markers
            # This can be used to fine the order of rearangement of ids.
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
            result = cv2.warpPerspective(frame2, M, (w_img_dest, h_img_dest))
            #mask the patched video on the displayed frame
            result2 = cv2.warpPerspective(one_frame_src, M, (w_img_dest, h_img_dest))
            result2 = one_frame_dest - result2
            cv2.bitwise_and(result2, frame, frame)
            frame += result

    #flips the webcam along the Y axis
    # Comment if not wanted
    #frame = cv2.flip(frame, 1)
    # Display the resulting frame
    
    # uncomment the line below to write the ouput video result
    # out.write(frame)
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cap2.release()
# uncomment the line below to release the video writer used to record the output
# out.release()
cv2.destroyAllWindows()