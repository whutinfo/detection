import cv2
import read_config,read_frame,frame_background,frame_detection,frame_tracker

if __name__ == '__main__':
    # 计数器初始化
    count = 0
    #读取配置
    #data = read_config.read()
    # 视频初始化
    # filename = "E:/FFOutput/龙洲垸船闸_上游靠船墩_20190108135824_20190108150952_-1665902912_0001 00_21_42-01_11_28.mp4"
    # cutname = 'E:/FFOutput/龙洲垸船闸_上游靠船墩_20190108135824_20190108150952_-1665902912_0001 00_23_56-01_10_48.mp4'
    # filename1 = "E:/FFOutput/4.mp4"
    file = 'C:/Users/lwhoo/Documents/Tencent Files/471317526/FileRecv/detection/1.mp4'
    # twoname = "E:/FFOutput/162.mp4"C:\Users\lwhoo\Documents\Tencent Files\471317526\FileRecv\detection>
    shiping = cv2.VideoCapture(file)
    camera, ok, frame, length = read_frame.cam_init(file) # 71664

    # 背景减除器初始化
    fgbg = frame_background.background_init()
    diff = 0

    tracker_list = []
    detect_list = []
    result_list = []
    while(1):
        #计数
        count += 1
        #读取帧
        success, frame_lwpCV = camera.read()
        if success != True:
            break
        # 当前帧的背景减除

        # 每 n 帧做一次背景减除 并进行对象监测，而在其间的n-1帧中采用跟踪算法
        n = 15
        if count % n == 0:
            # 清零，只是为了防止count计数太大
            count = 0
            diff = frame_background.process(fgbg,frame_lwpCV,count)

        #if diff is not 0:
            cv2.imshow('dis', diff)
            # 当前帧的目标检测
            print("*"*20)
            # detect (x,y,w,h)
            detect_list,detected_img,contour = frame_detection.detectobj(diff,frame_lwpCV)

            # 1、遍历所有跟踪器列表，更新位置，放进当前位置的列表0
            for detect in detect_list:
                # 初始化跟踪器，并添加进跟踪器列表
                tracker_list=frame_tracker.init_tracker(detected_img,detect,tracker_list)

        if diff is not 0:
            # 更新跟踪器画出跟踪框
            result_list = frame_tracker.update_tracker(detected_img,tracker_list)

            cv2.imshow('contours', detected_img)

        key = cv2.waitKey(1) & 0xFF

    camera.release()
    # 清除缓存退出
    cv2.destroyAllWindows()






