# -*- coding:utf-8 -*-

import cv2
import read_config,read_frame,frame_background,frame_detection,frame_tracker

if __name__ == '__main__':
    # 计数器初始化
    count = 0
    #读取配置
    #data = read_config.read()
    # 视频初始化
    filename = "E:/FFOutput/龙洲垸船闸_上游靠船墩_20190108135824_20190108150952_-1665902912_0001 00_21_42-01_11_28.mp4"
    cutname = 'C:/Users/lwhoo/PycharmProjects/detection/龙洲垸船闸_上游靠船墩_20190108091510_20190108102553_-1666244087_0001.mp4'
    filename1 = "4.mp4"
    file = './car.mp4'


    camera, ok, frame, length = read_frame.cam_init(file) # 71664

    # 背景减除器初始化
    fgbg = frame_background.background_init()
    diff = 0

    cap = cv2.VideoCapture(file)
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    # Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
    out = cv2.VideoWriter('./outpy.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (frame_width, frame_height))

    tracker_list = []
    detect_list = []
    result_list = []

    while count < 10000:
        #计数
        count += 1
        print('the frame count is',count)
        #读取帧
        success, frame_lwpCV = camera.read()
        if success != True:
            break
        # 针对高架桥视频做裁剪
        # frame_lwpCV = frame_background.cut(frame_lwpCV)
        # 当前帧的背景减除
        # 每 n 帧做一次背景减除 并进行对象监测，而在其间的n-1帧中采用跟踪算法
        step = 1
        diff = frame_background.process(fgbg,frame_lwpCV,count,step)
#        if count > 50 :  #等背景生成稳定后进行处理
        if diff is not 0:
            cv2.imshow('dis', diff)
            # 当前帧的目标检测
            print("*"*20)
            # detect (x,y,w,h)
            detect_list,detected_img,contour = frame_detection.detectobj(diff,frame_lwpCV)
            print('detectlist')
            print(detect_list)
            # 确定未能跟踪的目标
            print(result_list)
            new_detect_list=frame_tracker.list_compare(detect_list,result_list)
            print('newdetectlist')
            print(new_detect_list)
            # 初始化跟踪器，并添加未跟踪进跟踪器列表

            Added_tracker_list=frame_tracker.init_tracker(frame_lwpCV,new_detect_list)
            #
            tracker_list += Added_tracker_list
            cv2.imshow('contours', detected_img)
            tracked_img,result_list = frame_tracker.update_tracker(frame_lwpCV,tracker_list)
            cv2.imshow('tracked',tracked_img)

            out.write(tracked_img)
        key = cv2.waitKey(1) & 0xFF
    out.release()
    camera.release()
    # 清除缓存退出
    cv2.destroyAllWindows()






