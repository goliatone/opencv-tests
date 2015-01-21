import cv2
import cv2.cv as cv
import sys
import time

cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

def face_detect(img, cascade):
    rects = cascade.detectMultiScale(img, scaleFactor=1.1,
                                    minNeighbors=3,
                                    minSize=(10, 10), # w/h of min area to scan
                                    flags = cv.CV_HAAR_SCALE_IMAGE)
    if len(rects) == 0:
        return []
    rects[:,2:] += rects[:,:2]
    return rects

def draw_rects(img, rects, color):
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

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
    cv2.imshow('Display face ROI', faceROI)


    vis = img.copy()
    draw_rects(vis, faces, (0, 255, 0))

    cv2.namedWindow('Display image')          ## create window for display
    cv2.imshow('Display image', vis)          ## Show image in the window

    key = cv2.waitKey(10)
    if key == 27:
        cv2.destroyAllWindows()
        break

print "Goodbye"