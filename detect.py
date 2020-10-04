import cv2
import numpy as np

treshold_max_area = 5
treshold_min_area = 0

def detect_blob(img):
    result = []

    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    thresh = cv2.threshold(gray, 125, 255, cv2.THRESH_BINARY)[1]

    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        area = cv2.contourArea(c)
        if area >= treshold_min_area and area < treshold_max_area:
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])) if area > 0 else (c[0][0][0], c[0][0][1])
            result.append(center)
            cv2.drawContours(img, [c], -1, (36,255,12), -1)

    # cv2.imshow("aaa", img)
    # cv2.waitKey()

    return result