# -*- coding:utf-8 -*-

import cv2

'''
if len(sys.argv) != 2:
	print('Input video name is missing')
	exit()
'''

print('Select 3 tracking targets')

filename = './car.mp4'
cv2.namedWindow("tracking")
camera = cv2.VideoCapture(filename)
tracker = cv2.MultiTracker_create()
init_once = False

ok, image = camera.read()
if not ok:
	print('Failed to read video')
	exit()

bbox1 = cv2.selectROI('tracking', image)
bbox2 = cv2.selectROI('tracking', image)
bbox3 = cv2.selectROI('tracking', image)

frame_width = int(camera.get(3))
frame_height = int(camera.get(4))
# Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
out = cv2.VideoWriter('./outpy.avi',
	                      cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (frame_width, frame_height))

while camera.isOpened():
	ok, image = camera.read()
	if not ok:
		print('no image to read')
		break

	if not init_once:
		ok1 = tracker.add(cv2.TrackerTLD_create(), image, bbox1)
		ok2 = tracker.add(cv2.TrackerTLD_create(), image, bbox2)
		ok3 = tracker.add(cv2.TrackerTLD_create(), image, bbox3)
		init_once = True

	ok, boxes = tracker.update(image)
	print(ok, boxes)

	for newbox in boxes:
		p1 = (int(newbox[0]), int(newbox[1]))
		p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
		cv2.rectangle(image, p1, p2, (200, 0, 0))

	cv2.imshow('tracking', image)


	out.write(image)

	k = cv2.waitKey(1)
	if k == 27:
		break  # esc pressed

out.release()
