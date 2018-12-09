import api
import cv2
import numpy as np
import sys

the_path = '/Users/hilman_dayo/Google_Drive/demo_files/'
vid = api.FramesBuffer(the_path + 'example.mp4')
dto = api.DualTrackedObjects(vid, the_path + 'refined_result.csv', the_path + 'original_result.csv')

# TODO: Solve time to sleep.
while True:
    select = input('Choose n or p: ')
    if select == 'n':
        d = dto.get_next_dual_object()
    elif select == 'p':
        d = dto.get_prev_dual_object()
    else:
        dto.close()
        break

    idx_object = 0
    while True:
        try:
            i = d[idx_object]
        except:
            if idx_object < 0:
                idx_object = 0
            else:
                idx_object -= 1
            i = d[idx_object]

        # Prepare the frame.
        # TODO: Solve the copy frame (rewinding the buffer gives us same frame?)
        ref_frame = i.frames[0].copy()
        corr_frame = ref_frame.copy()

        # Prepare reference to refined and correspond object (TrackedObject instance).
        # Correspond object will be a list.
        ref = i.refined
        corr = i.correspond

        cv2.rectangle(ref_frame, (ref.x1, ref.y1), (ref.x2, ref.y2), (0, 0, 255), 2)
        for c in corr:
            if c is not None:
                cv2.rectangle(corr_frame, (c.x1, c.y1), (c.x2, c.y2), (0, 0, 255), 2)

        frames = np.concatenate((ref_frame, corr_frame), axis=1)
        cv2.imshow('ref_frame, corr_frame', frames)

        key = cv2.waitKey() & 0xFF
        if key == ord('n'):
            idx_object += 1
        elif key == ord('p'):
            idx_object -= 1
        else:
            break
