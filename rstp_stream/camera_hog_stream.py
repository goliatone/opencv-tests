#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
import cv2.cv as cv
import numpy as np


def filter_found_results(found):
    found_filtered = []

    for ri, r in enumerate(found):
        for qi, q in enumerate(found):
            if ri != qi and inside(r, q):
                break
            else:
                found_filtered.append(r)
    return found_filtered


def inside(r, q):
    rx, ry, rw, rh = r
    qx, qy, qw, qh = q
    return rx > qx and ry > qy and rx + rw < qx + qw and ry + rh < qy + qh

def draw_detections(img, rects, thickness = 1, color = (0, 255, 5)):
    for x, y, w, h in rects:
        # the HOG detector returns slightly larger rectangles than the real objects.
        # so we slightly shrink the rectangles to get a nicer output.
        pad_w, pad_h = int(0.15 * w), int(0.05 * h)
        cv2.rectangle(img, (x + pad_w, y + pad_h), (x + w - pad_w, y + h - pad_h),
                     color, thickness)


#Open camera and set dimensions
# cam = cv2.VideoCapture("rtsp://10.8.253.69:554/ch0_0.h264")
cam = cv2.VideoCapture("rtsp://10.8.253.69:554/MediaInput/mpeg4")
# cam = cv2.VideoCapture("http://10.8.253.211/snap.jpg")
# We can't set dimensions, stream overrides
# cam.set(cv.CV_CAP_PROP_FRAME_WIDTH, 640)
# cam.set(cv.CV_CAP_PROP_FRAME_HEIGHT, 480)

hog = cv2.HOGDescriptor()
hog.setSVMDetector( cv2.HOGDescriptor_getDefaultPeopleDetector() )

def main():
    while cam.isOpened():
        _, img = cam.read()

        found, w = hog.detectMultiScale(img, winStride=(8, 8), padding=(32, 32), scale=1.05)
        found_filtered = filter_found_results(found)

        draw_detections(img, found)
        draw_detections(img, found_filtered, 3)
        print '%d (%d) found' % (len(found_filtered), len(found))
        cv2.imshow('img', img)

        # cam = cv2.VideoCapture("http://10.8.253.211/snap.jpg")

        key = cv2.waitKey(10)
        if key == 27:
            cv2.destroyAllWindows()
            break

    print "Goodbye"

if __name__ == '__main__':
    main()
