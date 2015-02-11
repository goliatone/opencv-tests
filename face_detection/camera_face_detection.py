# -*- coding: utf-8 -*-
import cv2
import cv2.cv as cv
import argparse



class HAARFilter(object):
    """docstring for HAARFilter"""
    def __init__(self, cascade_url):
        super(HAARFilter, self).__init__()
        #TODO: Check if cascade_path exists, else...gross, throw up.
        self.cascade = cv2.CascadeClassifier(cascade_path)

    def detect(self, image):
        rects = self.cascade.detectMultiScale(image, scaleFactor=1.1,
                                              minNeighbors=3,
                                              minSize=(10,10),
                                              flags = cv.CV_HAAR_SCALE_IMAGE)
        if len(rects) == 0:
            return []
        rects[:, 2:] += rects[:, :2]
        return rects


class UI(object):
    """docstring for UI"""
    def __init__(self, url=0):
        super(UI
        , self).__init__()
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
        return image


#TODO: We should check file exists...YOLO!
cascade = cv2.CascadeClassifier('/Users/eburgos/Development/OPENCV/data/haarcascades/haarcascade_frontalface_alt2.xml')
# cascade = cv2.CascadeClassifier('./haarcascade_frontalface_alt.xml')


def face_detect(img, cascade):
    rects = cascade.detectMultiScale(img, scaleFactor=1.1,
                                    minNeighbors=3,
                                    minSize=(10, 10), # w/h of min area to scan
                                    flags = cv.CV_HAAR_SCALE_IMAGE)
    if len(rects) == 0:
        return []
    rects[:, 2:] += rects[:, :2]
    return rects


def draw_rects(img, rects, color):

    for (x, y, w, h) in rects:
        cv2.rectangle(img, (x, y), (w, h), color, 2)


#Open camera and set dimensions
cam = cv2.VideoCapture(0)
cam.set(cv.CV_CAP_PROP_FRAME_WIDTH, 640)
cam.set(cv.CV_CAP_PROP_FRAME_HEIGHT, 480)


cv2.namedWindow(winName, cv2.CV_WINDOW_AUTOSIZE)

# time.sleep(0.500)
# first frames are empty, for now we hack it
ret, img = cam.read()
ret, img = cam.read()

while cam.isOpened():
    #image
    ret, img = cam.read()

    gray = cv2.cvtColor(img, cv.CV_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    cv2.imshow('Imgae', gray)
    faces = face_detect(gray, cascade)

    ## Extract face coordinates
    for(x, y, w, h) in faces:
        ## Extract face ROI
        faceROI = gray[y:y+h, x:x+w]

    ## Show face ROI
    try:
        cv2.imshow('Display face ROI', faceROI)
    except Exception, e:
        print "Ensure you have haarcascade_frontalface_alt XML file."

    vis = img.copy()
    draw_rects(vis, faces, (0, 255, 0))

    cv2.namedWindow('Display image')          ## create window for display
    cv2.imshow('Display image', vis)          ## Show image in the window

    key = cv2.waitKey(10)
    if key == 27:
        cv2.destroyAllWindows()
        break

print "Goodbye"

def main():
    parser = argparse.ArgumentParser(description='Camera face detection')
    parser.add_argument('-u', '--url', default=0, help='Video stream filename or device id')
    args = parser.parse_args()

    ui = UI(url=args.url)

    while ui.loop():
        image = ui.capture_frame()

        ##
        gray = cv2.cvtColor(image, cv.CV_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        # cv2.imshow('Image', gray)
        found = haar.detect(image)
        ##

        for(x, y, w, h) in found:
            faceROI = gray[y: y + h, x: x + w]
            try:
                cv2.imshow('Image ROI', faceROI)
            except Exception, e:
                raise e

        vis = ui.draw_detections(image.copy(), found)
        cv2.imshow('Display Image', vis)

        key = cv2.waitKey(10)
        if key == 27:
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    main()
