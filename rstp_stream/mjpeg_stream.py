import cv2
import cv2.cv as cv
import numpy as np
import urllib

URL = 'http://10.8.253.209/snap.jpg'
stream = urllib.urlopen(URL)
bytes=''

def inside(r, q):
    rx, ry, rw, rh = r
    qx, qy, qw, qh = q
    return rx > qx and ry > qy and rx + rw < qx + qw and ry + rh < qy + qh

def draw_detections(img, rects, thickness = 1):
    for x, y, w, h in rects:
        # the HOG detector returns slightly larger rectangles than the real objects.
        # so we slightly shrink the rectangles to get a nicer output.
        pad_w, pad_h = int(0.15*w), int(0.05*h)
        cv2.rectangle(img, (x+pad_w, y+pad_h), (x+w-pad_w, y+h-pad_h), (0, 255, 0), thickness)


hog = cv2.HOGDescriptor()
hog.setSVMDetector( cv2.HOGDescriptor_getDefaultPeopleDetector() )

while True:
    bytes += stream.read(1024)
    a = bytes.find('\xff\xd8')
    b = bytes.find('\xff\xd9')
    if a!=-1 and b!=-1:
        # print "process"
        jpg = bytes[a: b+2]
        bytes= bytes[b+2:]
        img = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),
                             cv2.CV_LOAD_IMAGE_COLOR)



        # cv2.imshow('IP Camera Preview', img)

        found, w = hog.detectMultiScale(img, winStride=(8,8), padding=(32,32), scale=1.05)
        found_filtered = []
        for ri, r in enumerate(found):
            for qi, q in enumerate(found):
                if ri != qi and inside(r, q):
                    break
            else:
                found_filtered.append(r)
        draw_detections(img, found)
        draw_detections(img, found_filtered, 3)
        print '%d (%d) found' % (len(found_filtered), len(found))
        cv2.imshow('img', img)

        stream = urllib.urlopen(URL)
        bytes=''

        key = cv2.waitKey(10)
        if key == 27:
            cv2.destroyAllWindows()
            break

print "Goodbye"
