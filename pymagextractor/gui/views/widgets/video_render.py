from PySide2 import QtCore, QtGui, QtWidgets
import pymagextractor.gui.views.widgets.graphics_rect_item as CustomWidget
import pymagextractor.models.buffer.frame as Frame
import pandas as pd
import pymagextractor.models.data_handler as dh
from functools import partial
# import pymagextractor.models.sessions as sess  # TEMP: Use `DataHandler` only

class VideoRender(QtWidgets.QGraphicsView):

    def __init__(self, parent):
        super(VideoRender, self).__init__()
        self.main_window = parent
        self.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.size_adjusted = False
        self.ratio = 1
        self.setAcceptDrops(True)

        # Config QGraphics objects
        self.scene = QtWidgets.QGraphicsScene(self)
        self.setScene(self.scene)

        # Frame
        self.frame = None
        self.scene_frame = QtWidgets.QGraphicsPixmapItem()

        # Current Detection Selection
        self.init_point = QtCore.QPoint()
        self.end_point = QtCore.QPoint()
        self.drawing = False
        self.current_selection = QtWidgets.QGraphicsRectItem()
        self.brush_current = QtGui.QBrush(QtGui.QColor(10, 10, 100, 120))

        # Detections
        self.detection = []
        self.detection_objects = []  # List of GraphicsRectItem objects
        self.brush_detection = QtGui.QBrush(QtGui.QColor(100, 10, 10, 120))

        # Saved
        self.save_action = None
        self.current_frame_number = None
        # self.saved_object = {'frame_number':[], 'track_id':[], 'init_point':{'x':[], 'y':[]}, 'end_point':{'x':[], 'y':[]}, 'scene':[], 'object':[], 'view':[]}
        self.current_selected_track_id = None
        self.current_selected_scene = None
        self.current_selected_object = None
        self.current_selected_view = None
        self.write_to_csv = pd.DataFrame({'frame_id':[],
                                          'track_id':[],
                                          'x1':[],
                                          'y1':[],
                                          'x2':[],
                                          'y2':[],
                                          'scene':[],
                                          'object':[],
                                          'view':[]})
        self.ws_ = None
        self.ws_path_ = None
        self.csv_filename = None
        self.video_filename_ = None
        self.init()


    def init(self):
        self.size_adjusted = False
        self.ratio = 1


    def set_frame(self, original_frame):
        """Set frame to be shown and resize the frame and widget"""
        # Resize frame
        # self.frame = original_frame.scaled(self.size(), QtCore.Qt.KeepAspectRatio)
        # Change by HILMAN. This is temporary. It is the same with the size of video
        # defined in `home_controller.py`
        self.frame = original_frame.scaled(640, 500)

        # Resize render widget
        if not self.size_adjusted:
            self.ratio = self.frame.size().height()/original_frame.size().height()
            self.resize(self.frame.size())
            self.size_adjusted = True

        # for ii in NFOLLOW:
        #     ii.next(
        #             self.current_frame_number,
        #             self.init_point.x(),
        #             self.init_point.y(),
        #             self.end_point.x(),
        #             self.end_point.y(),
        #         )
        self.update_frame()

    def update_frame(self):
        """"Update the frame and all the detection squares"""
        self.scene.clear()
        # Display image/frame
        if self.frame:
            self.scene_frame = QtWidgets.QGraphicsPixmapItem(self.frame)
            self.scene.addItem(self.scene_frame)
            self.fitInView(self.scene_frame)
        # Draw new detection square
        if self.drawing:
            self.current_selection = QtWidgets.QGraphicsRectItem(QtCore.QRect(self.init_point, self.end_point))
            self.current_selection.setBrush(self.brush_current)
            self.scene.addItem(self.current_selection)
        # Detect all objects according to the Track List
        self.detection_objects = []
        for element in self.detection:
            d = CustomWidget.GraphicsRectItem(element.rect(self.ratio))
            d.setBrush(self.brush_detection)
            d.set_edit_mode(self.main_window.controller.edit_mode)
            self.scene.addItem(d)
            self.detection_objects.append(d)

    def set_detection_list(self, set_of_elements):
        """Set the position of all the recognition squares"""
        self.detection = set_of_elements

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if not self.main_window.controller.edit_mode:
            self.drawing = True
            self.init_point = event.pos()
            self.end_point = event.pos()
            self.update_frame()

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if not self.main_window.controller.edit_mode:
            x = event.pos().x()
            y = event.pos().y()
            if x < 0:
                self.end_point.setX(0)
            elif x > self.size().width():
                self.end_point.setX(self.size().width()-4)
            else:
                self.end_point.setX(x)
            if y < 0:
                self.end_point.setY(0)
            elif y > self.size().height():
                self.end_point.setY(self.size().height()-4)
            else:
                self.end_point.setY(y)
            self.update_frame()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        if not self.main_window.controller.edit_mode:
            menu = QtWidgets.QMenu(self)

            # === Menu that will come out on the screen after the release of button. ===
            # self.save_action = menu.addAction("Save")
            self.save_action = menu.addAction("Print CSV")
            self.actions = {}

            # for k, v in self.ACTIONS.items(): # the self.ACTIONS is the one added by user
            #     self.actions[k] = menu.addMenu(k)

            #     self.actions[k].addAction(f"{k} (New)").triggered.connect(self.upon_bb_selection(k))
            #     for vv in self.SAVED[k]:
            #         self.actions[k].addAction(f"Tokutei Object ({vv.track_id})").triggered.connect(self.upon_bb_selection(k, vv.track_id))
            menu.addAction(f"NEW object").triggered.connect(
                self.upon_bb_selection)
            # make based on datahandler

            self.save_action.triggered.connect(self.save_all)
            menu.exec_(QtGui.QCursor.pos())
            self.drawing = False
            self.update_frame()

    def enterEvent(self, event):
        if not self.main_window.controller.edit_mode:
            QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        return super(VideoRender, self).enterEvent(event)

    def leaveEvent(self, event):
        QtWidgets.QApplication.restoreOverrideCursor()
        return super(VideoRender, self).enterEvent(event)

    def upon_bb_selection(self, idx=None):
        # let say we got the tokuteiobject
        def ubbc():
            sessions = self.SAVED[session_name]
            nonlocal idx
            if idx is None:
                self.SAVED[session_name].append(sess.TokuteiObject(data_handler=self.DHS[session_name], normalize=[640, 500]))
                idx = self.SAVED[session_name][-1].track_id

            idxs = [i.track_id for i in self.SAVED[session_name]]
            idx = idxs.index(idx)
            track_id = idxs[idx]
            self.SAVED[session_name][idx].upon_bb_selection(
                track_id,
                self.current_frame_number,
                self.init_point.x(),
                self.init_point.y(),
                self.end_point.x(),
                self.end_point.y(),
                )
            if QtWidgets.QApplication.keyboardModifiers() == QtCore.Qt.ControlModifier:
                del self.SAVED["tokutei"][idx]

        return ubbc


    def save_callback(self):
        x1 = self.init_point.x()
        y1 = self.init_point.y()
        x2 = self.end_point.x()
        y2 = self.end_point.y()
        frame = self.current_frame_number
        track = self.current_selected_track_id
        scene = self.current_selected_scene
        obj = self.current_selected_object
        view = self.current_selected_view
        # print(self.ws_path_ + '/workspaces/' + self.ws_ + f'/orig_{self.ws_}.csv')
        # print('/home/zulfaqar/develop/pymagextractor/data/workspace_test/workspaces/aaaa/aaaa.csv')
        # self.saved_object['init_point']['x'].append(x1)
        # self.saved_object['init_point']['y'].append(y1)
        # self.saved_object['end_point']['x'].append(x2)
        # self.saved_object['end_point']['y'].append(y2)
        # self.saved_object['frame_number'].append(frame)
        # self.saved_object['track_id'].append(track)
        # self.get_csv()
        '''
        append file in Pandas DATAFRAME
        '''
        self.get_csv()
        print(self.csv_filename)
        new = pd.DataFrame({'frame_id':[frame],
                            'track_id':[track],
                            'x1':[int(x1)],
                            'y1':[int(y1)],
                            'x2':[x2],
                            'y2':[y2],
                            'scene':[scene],
                            'object':[obj],
                            'view':[view]})

        self.write_to_csv = self.write_to_csv.append(new, ignore_index=True)
        self.write_to_csv.to_csv(self.csv_filename, index = False)
        print(self.write_to_csv)

    def save_all(self):
        for k, v in self.DHS.items():
            v.save()


    def get_csv(self):
        self.csv_filename = str(self.ws_path_) + '/workspaces/' + str(self.ws_) + f'/{self.video_filename_}_{self.ws_}.csv'
        # print(self.csv_filename)
        try:
            self.write_to_csv = pd.DataFrame({'frame_id':[],
                                          'track_id':[],
                                          'x1':[],
                                          'y1':[],
                                          'x2':[],
                                          'y2':[],
                                          'scene':[],
                                          'object':[],
                                          'view':[]})

            df = pd.read_csv(self.csv_filename,
                             usecols=['frame_id',
                                      'track_id',
                                      'x1',
                                      'y1',
                                      'x2',
                                      'y2',
                                      'scene',
                                      'object',
                                      'view'])
            self.write_to_csv = df
            # print(self.write_to_csv)
        except FileNotFoundError:
            pass
