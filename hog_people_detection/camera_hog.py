#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
import cv2.cv as cv
import numpy as np


def inside(r, q):
    (rx, ry), (rw, rh) = r
    (qx, qy), (qw, qh) = q
    return rx > qx and ry > qy and (rx + rw) < (qx + qw) and (ry + rh) < (qy + qh)

def hog_detection(img):
    found = list(cv.HOGDetectMultiScale(cv.fromarray(img), storage, win_stride=(8,8),
        padding=(32,32), scale=1.05, group_threshold=2))
    found_filtered = []

    for r in found:
        insidef = False
        for q in found:
            if inside(r, q):
                insidef = True
                break
        if not insidef:
            found_filtered.append(r)
    for r in found_filtered:
        (rx, ry), (rw, rh) = r
        tl = (rx + int(rw * 0.1), ry + int(rh * 0.07))
        br = (rx + int(rw * 0.9), ry + int(rh * 0.87))
        cv2.rectangle(img, tl, br, (0, 255, 0), 3)


def draw_rects(img, rects, color):

    for (x, y, w, h) in rects:
        cv2.rectangle(img, (x, y), (w, h), color, 2)


#Open camera and set dimensions
cam = cv2.VideoCapture(0)
cam.set(cv.CV_CAP_PROP_FRAME_WIDTH, 640)
cam.set(cv.CV_CAP_PROP_FRAME_HEIGHT, 480)

winName = "Movement Indicator"
cv2.namedWindow(winName, cv2.CV_WINDOW_AUTOSIZE)

# time.sleep(0.500)
# first frames are empty, for now we hack it
ret, img = cam.read()
ret, img = cam.read()


storage = cv.CreateMemStorage(0)
while cam.isOpened():
    #image
    ret, img = cam.read()

    faces = hog_detection(img)

    vis = img.copy()


    cv2.namedWindow('Display image')          ## create window for display
    cv2.imshow('Display image', vis)          ## Show image in the window

    key = cv2.waitKey(10)
    if key == 27:
        cv2.destroyAllWindows()
        break

print "Goodbye"
