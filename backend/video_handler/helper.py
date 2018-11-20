import collections
import itertools

import cv2


# TODO: Make a test!
def _refresh_deque(self, old_start, old_end):
    ret = check_position(self, old_start, old_end)

    if ret == 'partial_forward_exceed':
        self.Q = slice_deque(self.Q, self.Q_frame_start, maxlen=self.Q.maxlen)
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, old_end)
    if ret == 'complete_forward_exceed':
        self.Q = collections.deque(maxlen=self.Q.maxlen)
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.Q_frame_start)
    if ret == 'partial_backward_exceed':
        # TODO: Can definitely make this better!
        self.Q = collections.deque(maxlen=self.Q.maxlen)
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.Q_frame_start)
    if ret == 'complete_backward_exceed':
        self.Q = collections.deque(maxlen=self.Q.maxlen)
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.Q_frame_start)


def check_position(self, old_start, old_end):
    # TODO: Give a better name.
    if within(self.Q_frame_start, self.Q_frame_end, old_start, old_end):
        print("I am within")
        return 'within'
    if partial_forward_exceed(self.Q_frame_start, self.Q_frame_end, old_start, old_end):
        print("I am pfe")
        return 'partial_forward_exceed'
    if complete_forward_exceed(self.Q_frame_start, self.Q_frame_end, old_start, old_end):
        print("I am cfe")
        return 'complete_forward_exceed'
    if partial_backward_exceed(self.Q_frame_start, self.Q_frame_end, old_start, old_end):
        print("I am pbe")
        return 'partial_backward_exceed'
    if complete_backward_exceed(self.Q_frame_start, self.Q_frame_end, old_start, old_end):
        print("I am cbe")
        return 'complete_backward_exceed'

    raise Exception


# TODO: Check better the logic under this.
def within(new_start, new_end, old_start, old_end):
    return new_start >= old_start and new_end < old_end


def partial_forward_exceed(new_start, new_end, old_start, old_end):
    return (new_start >= old_start and new_start < old_end
            and new_end >= old_end)


def complete_forward_exceed(new_start, new_end, old_start, old_end):
    # Assumption of buffer of frames only limited to 128
    return new_start >= old_end


def partial_backward_exceed(new_start, new_end, old_start, old_end):
    return (new_start < old_start and
            new_end <= old_end and new_end >= old_start)


def complete_backward_exceed(new_start, new_end, old_start, old_end):
    # Assumption of buffer of frames only limited to 128
    return new_end < old_end


def slice_deque(Q, start, end=None, maxlen=None):
    return collections.deque(itertools.islice(Q, start, end), maxlen=maxlen)
