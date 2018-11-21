import collections
import itertools

import cv2


# TODO: Make a test!
def _refresh_deque(self, new_start, new_end, old_head, old_tail):
    if new_start is None:
        ret = complete_forward_exceed
    else:
        ret = check_position(new_start, new_end, old_head, old_tail)

    if ret == 'partial_forward_exceed':
        i = new_start - old_head
        self.Q = slice_deque(self.Q, i, maxlen=self.Q.maxlen)
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, old_tail)
        self.Q_frame_head = new_start

    if ret == 'complete_forward_exceed':
        self.Q = collections.deque(maxlen=self.Q.maxlen)
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, new_start)
        self.Q_frame_head = new_start
        self.Q_frame_tail = new_start

    if ret == 'partial_backward_exceed':
        # TODO: Can definitely make this better!
        self.Q = collections.deque(maxlen=self.Q.maxlen)
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, new_start)
        self.Q_frame_head = new_start
        self.Q_frame_tail = new_start

    if ret == 'complete_backward_exceed':
        self.Q = collections.deque(maxlen=self.Q.maxlen)
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, new_start)
        self.Q_frame_head = new_start
        self.Q_frame_tail = new_start


def check_position(new_start, new_end, old_head, old_tail):
    # TODO: Give a better name.
    if within(new_start, new_end, old_head, old_tail):
        print("I am within")
        return 'within'
    if partial_forward_exceed(new_start, new_end, old_head, old_tail):
        print("I am pfe")
        return 'partial_forward_exceed'
    if complete_forward_exceed(new_start, new_end, old_head, old_tail):
        print("I am cfe")
        return 'complete_forward_exceed'
    if partial_backward_exceed(new_start, new_end, old_head, old_tail):
        print("I am pbe")
        return 'partial_backward_exceed'
    if complete_backward_exceed(new_start, new_end, old_head, old_tail):
        print("I am cbe")
        return 'complete_backward_exceed'

    raise Exception


# TODO: Check better the logic under this.
def within(new_start, new_end, old_head, old_tail):
    print(new_start)
    print(new_end)
    print(old_head)
    print(old_tail)
    return new_start >= old_head and new_end < old_tail


def partial_forward_exceed(new_start, new_end, old_head, old_tail):
    return (new_start >= old_head and new_start < old_tail
            and new_end >= old_tail)


def complete_forward_exceed(new_start, new_end, old_head, old_tail):
    # Assumption of buffer of frames only limited to 128
    return new_start >= old_tail


def partial_backward_exceed(new_start, new_end, old_head, old_tail):
    return (new_start < old_head and
            new_end <= old_tail and new_end >= old_head)


def complete_backward_exceed(new_start, new_end, old_head, old_tail):
    # Assumption of buffer of frames only limited to 128
    return new_end < old_tail


def slice_deque(Q, start, end=None, maxlen=None):
    return collections.deque(itertools.islice(Q, start, end), maxlen=maxlen)
