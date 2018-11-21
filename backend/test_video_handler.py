from video_handler.video_handler import VideoCaptureAsync
import cv2
import time


vid = VideoCaptureAsync('/home/hilman/Documents/final_hatsu_presentation/videos/exp.avi', 32, 64)

vid.start()

vid.refresh_deque(150, 200)
time.sleep(5)
vid.refresh_deque(250, 300)
time.sleep(5)
vid.refresh_deque(0, 100)
time.sleep(5)
vid.stop()
vid.exit()
