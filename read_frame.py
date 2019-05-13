import cv2
import sys

def cam_init(filename):

    cam = cv2.VideoCapture(filename)
    if not cam.isOpened():
        print('can not open')
        sys.exit()
    ok, frame = cam.read()
    if not ok:
        print('Cannot read video file')
        sys.exit()
    length = int(cam.get(cv2.CAP_PROP_FRAME_COUNT))
    return cam,ok,frame,length
