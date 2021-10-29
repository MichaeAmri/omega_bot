import cv2 as cv
import numpy as np
import functions
import time

video = cv.VideoCapture(0)

if not video.isOpened():
    print('error while opening the video')

cv.waitKey(1)

while video.isOpened():
    _, frame = video.read()		# resolution 640 x 480

    frame = cv.resize(frame, (320, 240))
    copy_img = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    frame = functions.canny(frame)
    frame = functions.mask(frame)

    try:
        lines = cv.HoughLinesP(frame, 2, np.pi/180, 20, np.array([()]), minLineLength=20, maxLineGap=5)  # image, rho, theta, threshold, lines
        averaged_lines = functions.average_slope_intercept(frame, lines)
        line_image = functions.display_lines(frame, averaged_lines)
        #print('\nLeft: X1 = ', averaged_lines[0][0]-320, 'X2 = ', averaged_lines[0][2]-320,
	#'\nRight: X1 = ', averaged_lines[1][1]-320, 'X2 = ', averaged_lines[1][2]-320)
        #time.sleep(0.2)

        frame_plus_copy = cv.addWeighted(copy_img, 0.5, frame, 0.9, 1)
        combo = cv.addWeighted(frame_plus_copy, 0.8, line_image, 0.2, 1)
        #cv.line(combo, ((averaged_lines[0][0]+averaged_lines[1][1])//2 , 470), (380, 20), (255, 0, 0), 4)

        cv.imshow('video', combo)
        #cv.imshow('video', copy_img)
    except:
        pass

    if cv.waitKey(1) & 0xFF == ord('q'):
        video.release()
        cv.destroyAllWindows()

video.release()
cv.destroyAllWindows()
