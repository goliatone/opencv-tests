#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
import numpy as np
import argparse

"""
# video_url = "rtsp://10.8.253.69:554/ch0_0.h264"
# video_url = "rtsp://10.8.253.69:554/MediaInput/mpeg4"

rtsp://admin:12345@10.8.253.68:554/ch0_0.h264
rtsp://admin:12345@10.8.253.68:554/MediaInput/mpeg4

python camera_hog_stream -u rtsp://10.8.253.69:554/MediaInput/mpeg4
"""

class HOGFilter(object):
    """docstring for HOGFilter"""
    def __init__(self):
        super(HOGFilter, self).__init__()
        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector( cv2.HOGDescriptor_getDefaultPeopleDetector() )

    def detect(self, image, winStride, padding, scale):
        found, _ = self.hog.detectMultiScale(image, winStride=winStride,
            padding=padding, scale=scale)
        return found

    def filter(self, found):
        filtered = []
        for ri, r in enumerate(found):
            for qi, q in enumerate(found):
                if ri != qi and self.inside(r, q):
                    break
                else:
                    filtered.append(r)
        return filtered

    def inside(self, r, q):
        rx, ry, rw, rh = r
        qx, qy, qw, qh = q
        return rx > qx and ry > qy and rx + rw < qx + qw and ry + rh < qy + qh


class UI(object):
    """docstring for UI"""
    def __init__(self, url):
        super(UI, self).__init__()
        self.url = url
        self.camera = cv2.VideoCapture(url)

    def loop(self):
        return self.camera.isOpened()

    def capture_frame(self):
        _, image = self.camera.read()
        return image


    def draw_detections(self, image, rects, thickness = 1, color = (0, 255, 5)):
        for x, y, w, h in rects:
            # the HOG detector returns slightly larger rectangles than the real objects.
            # so we slightly shrink the rectangles to get a nicer output.
            pad_w, pad_h = int(0.15 * w), int(0.05 * h)
            cv2.rectangle(image, (x + pad_w, y + pad_h), (x + w - pad_w, y + h - pad_h),
                         color, thickness)

def main():

    parser = argparse.ArgumentParser(description='HOG Camera stream')
    parser.add_argument('-u', '--url', required=True, help='Video stream filename or device id')
    args = parser.parse_args()

    window_title = parser.description

    ui = UI(args.url)
    hog = HOGFilter()

    while ui.loop():
        image = ui.capture_frame()

        found = hog.detect(image, winStride=(8, 8), padding=(32, 32), scale=1.05)
        filtered = hog.filter(found)

        ui.draw_detections(image, found)
        ui.draw_detections(image, filtered, 3, (0, 0, 255))

        print '%d filtered, (%d) found' % (len(filtered), len(found))
        cv2.imshow(window_title, image)

        key = cv2.waitKey(10)
        if key == 27:
            cv2.destroyAllWindows()
            break

    print "Exit script..."

if __name__ == '__main__':
    main()
