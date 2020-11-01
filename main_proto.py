# from https://webnautes.tistory.com
import cv2 as cv # opencv __version__ 4.2.0

# draw coordinate using cv2.line()
def draw_ball_location(img_color, locations):
    for i in range(len(locations) - 1):
        # if locations is empty
        if locations[0] is None or locations[1] is None:
            continue

        # draw each coordinates in locations on window
        # BGR of yellow = (0, 255, 255)
        cv.line(img_color, tuple(locations[i]), tuple(locations[i+1]), (0, 255, 0), 3)

# parameter 0 means main web camera
cap = cv.VideoCapture(-1)

list_ball_location = []
history_ball_locations = []
isDraw = False # Do not draw as soon as the program starts

# __main()__
while True:
    if not cap.isOpened():
        cap.open()

       # print('cam initializing fail')
       # break
    
    # loading video
    ret,img_color = cap.read()
    if not ret:
        print('read() error')
        break

    # it doesn't work on version 4.2.0
    # img_color = cv.filp(img_color,1)

    # make video colorful. Using parameter cv2.COLOT_BGR@HSV
    img_hsv = cv.cvtColor(img_color, cv.COLOR_BGR2HSV)

    ## for color detection
    hue_blue = 170 # HSV red value
    lower_blue = (hue_blue-10, 0, 240)
    upper_blue = (hue_blue+10, 255, 255)

    ## detect between lower_blue and upper_blue color
    img_mask = cv.inRange(img_hsv, lower_blue, upper_blue)

    # make circle structuring element for segmentation
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (5, 5))
    # combination of erosion and dilation
    # use cv2.morphologyEx(). erosion and dilation for iterations=3 times
    img_mask = cv.morphologyEx(img_mask, cv.MORPH_DILATE, kernel, iterations = 3)
    # labeling
    nlabels, labels, stats, centroids = cv.connectedComponentsWithStats(img_mask)

    max = -1
    max_index = -1

    for i in range(nlabels):

        if i < 1:
            continue

        area = stats[i, cv.CC_STAT_AREA]

        if area > max:
            max = area
            max_index = i

    if max_index != -1:
        # make a circle and square
        center_x = int(centroids[max_index, 0]) 
        center_y = int(centroids[max_index, 1])
        left = stats[max_index, cv.CC_STAT_LEFT]
        top = stats[max_index, cv.CC_STAT_TOP]
        width = stats[max_index, cv.CC_STAT_WIDTH]
        height = stats[max_index, cv.CC_STAT_HEIGHT]

        cv.rectangle(img_color, (left, top), (left + width, top + height), (0, 0, 255), 5)
        cv.circle(img_color, (center_x, center_y), 10, (0, 255, 0), -1)

        # if isDraw is True, append the center coordinate of detected stuff
        if isDraw:
            list_ball_location.append((center_x, center_y))
        # if isDraw is False, saving last coordinate and all clear
        else:
            history_ball_locations.append(list_ball_location.copy())
            list_ball_location.clear()

        # draw a line based on coordinate
        draw_ball_location(img_color, list_ball_location)

        for ball_locations in history_ball_locations:
            draw_ball_location(img_color, ball_locations)

        # create window and show the result
        cv.imshow('Binarization', img_mask)
        cv.imshow('Result', img_color)

        # Using keyboard function for drawing or not or clear all
        key = cv.waitKey(1)
        if key == 27: # esc
            break
        elif key == 32: # space bar
            list_ball_location.clear()
            history_ball_locations.clear()
        elif key == ord('v'):
            isDraw = not isDraw
