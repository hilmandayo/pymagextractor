import api
import time
import cv2


vid = api.FramesBuffer('/home/hilman/Documents/demo_files/example.mp4')
dto = api.DualTrackedObjects(vid, '/home/hilman/Documents/demo_files/refined_result.csv', '/home/hilman/Documents/demo_files/original_result.csv')

# TODO: Solve time to sleep.
time.sleep(3)
res = dto.get_next_dual_object()

r9 = res[9]

# TODO: Solve the best api for this
copy = r9.frames[18].copy()
cv2.rectangle(copy, (r9.refined.x1, r9.refined.y1), (r9.refined.x2, r9.refined.y2), (0, 0, 255), 2)
cv2.imshow('test', copyrighty)
cv2.waitKey()

dto.close()
