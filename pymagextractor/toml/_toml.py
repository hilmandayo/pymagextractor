#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import toml
import os.path


# Get the annotations.
# Need to make some sort of return function that didnt produce error.
# Toml file format:
# ```
# [[annotations]]
# scene = "road_scene"
# object_id = [ "car", "bicycle",]
# car = [ [ "front", "a",], [ "back", "s",],]
# bicycle = [ [ "front", "z",], [ "back", "x",],]
#
# [[annotations]]
# scene = "konbini"
# object_id = [ "ice_cream", "drink",]
# ice_cream = [ [ "vanilla", "a",], [ "chocolate", "s",],]
# drink = [ [ "ocha", "z",], [ "coffee", "x",],]
# ```

# In[ ]:


class TomlHandler:
    def __init__(self):
        self._workspace = None
        self._filename = None
        self.anns = {'annotations':[]}
        self.clear_object = {'annotations' : []}
        self.anns_object = {'scene' : None, 'object_id' : []}
        self.clear_object = {'scene' : None, 'object_id' : []}
        self.temp_object_id = None

    def get_toml_filename(self):
        self._filename = f"{self._workspace}_ann.toml"

    def create_new_variable(self):
        '''
        write some default scene, objects and view
        '''
        # default = {
        #     "scene" : "itolab",
        #     "object_id": ["azu",
        #                   "hilman",
        #                   "abe",],
        #     "azu":
        #         [["front", "a"],
        #          ["back", "s"]],
        #     "hilman":
        #         [["front", "z"],
        #          ["back", "x"]],
        #     "abe":
        #         [["front", "z"],
        #          ["back", "x"]],
        # } #deprecriate

        default = {
            "scene" : "road_scene",
            "object_id": ["red_traffic_light",
                          "yellow_traffic_light",
                          "stop_sign",
                          "left_green_arrow",
                          "forward_green_arrow",
                          "right_green_arrow",
                          "tomare_paint",],
            "red_traffic_light":
                [["far", "a"],
                 ["middle", "a"],
                 ["close", "a"],
                 ["other", "s"]],
            "yellow_traffic_light":
                [["far", "a"],
                 ["middle", "a"],
                 ["close", "a"],
                 ["other", "s"]],
            "stop_sign":
                [["far", "a"],
                 ["middle", "a"],
                 ["close", "a"],
                 ["other", "s"]],
            "left_green_arrow":
                [["far", "a"],
                 ["middle", "a"],
                 ["close", "a"],
                 ["other", "s"]],
            "forward_green_arrow":
                [["far", "a"],
                 ["middle", "a"],
                 ["close", "a"],
                 ["other", "s"]],
            "right_green_arrow":
                [["far", "a"],
                 ["middle", "a"],
                 ["close", "a"],
                 ["other", "s"]],
            "tomare_paint":
                [["far", "a"],
                 ["middle", "a"],
                 ["close", "a"],
                 ["other", "s"]],
        }

        self.anns['annotations'].append(default)

    def check_if_exist(self):
        '''
        check the availability of the file.
        If file not avaiable, create a default variable
        '''
        try:
            # self.get_toml_filename()
            load_ = toml.load(self._filename)
            try:
                test_if_annotation_available = load_['annotations']
                self.anns = load_
            except KeyError:
                self.create_new_variable()

        except FileNotFoundError:
            print("File not found")
            self.create_new_variable()

    def get_scene(self, scene_name):
        self.anns_object['scene'] = scene_name

    def get_add_object_id(self, object_id):
        self.anns_object['object_id'].append(object_id)
        self.temp_object_id = object_id
        self.anns_object[object_id] = []

    def get_add_view_in_object_id(self, view_name, view_shortcutkey):
        self.anns_object[self.temp_object_id].append([str(view_name),str(view_shortcutkey)])

    def update_annotations(self):
        self.anns['annotations'].append(self.anns_object)

    def reset_annotation_object(self):
        self.anns_object = self.clear_object
        print("cleared")

    def save_annotation_to_file(self):
        toml.dump(self.anns, open(self._filename, 'w'))



# tomlhandle._workspace = "azu2"

# tomlhandle.check_if_exist()
# print(tomlhandle.anns['annotations'])

# print(tomlhandle.anns['annotations'])


# '''Assign keyboard shortcut'''
# _obj = []
# for i, _ann in enumerate(tomlhandle.anns['annotations']):
#     try:
#         _obj.append(_ann)
#         print(i, _obj[i])
#     except KeyError:
#         None
#     except ValueError:
#         None


# keyboard_shortcut = {}
# for i, _ in enumerate(_obj[1]['onigiri']):
#     _name = 0
#     _shortcut = 1
#     keyboard_shortcut[_obj[1]['onigiri'][i][_shortcut]] = _obj[1]['onigiri'][i][_name]

# print(keyboard_shortcut.get('p'))
# print(keyboard_shortcut.get('p'))
# print(keyboard_shortcut.get('r'))
# print(keyboard_shortcut.get('r'))




# ```
# def get_annotations_name(_annotations):
#     objects = []
#     scenes = []
#     views = []
#     for i, _ann in enumerate(_annotations):
#         try:
#             scenes.append(_ann['scene'])
#             objects.append(_ann['object_id'])
#             for j, _objects in enumerate(_ann['object_id']):
#                 try:
#                     views.append(_ann[_objects])
#                 except KeyError:
#                     None
#                 except ValueError:
#                     None
#         except KeyError:
#             None
#     print(objects, scenes, views)
# ```

# ```
# tomlhandle.get_scene('konbini')
#
# tomlhandle.get_add_object_id('onigiri')
# print(tomlhandle.temp_object_id)
# tomlhandle.get_add_view_in_object_id('plastic_wrap', 'p')
#
# print(tomlhandle.anns_object)
#
# tomlhandle.get_add_view_in_object_id('rice', 'r')
#
# print(tomlhandle.anns_object)
# -----------------------------------------------------------------------------
# tomlhandle.get_scene('road_scene')
#
# tomlhandle.get_add_object_id('car')
# print(tomlhandle.temp_object_id)
# tomlhandle.get_add_view_in_object_id('front', 'f')
#
# print(tomlhandle.anns_object)
#
# tomlhandle.get_add_view_in_object_id('back', 'b')
#
# print(tomlhandle.anns_object)
# -----------------------------------------------------------------------------
# tomlhandle.update_annotations()
#
# print(tomlhandle.anns['annotations'])
#
# print(tomlhandle._filename)
#
# tomlhandle.save_annotation_to_file()
# ```

# These part is for appending the values into annotations files

# ```
# anns = {'annotations':[]}
#
# anns1 = {
#     "scene" : "itolab",
#     "object_id": ["azu",
#                   "hilman",
#                   "abe",],
#     "azu":
#         [["front", "a"],
#          ["back", "s"]],
#     "hilman":
#         [["front", "z"],
#          ["back", "x"]],
#     "abe":
#         [["front", "z"],
#          ["back", "x"]],
# }
#
# anns2 = {
#     "scene" : "road_scene",
#     "object_id": ["car",
#                   "bicycle",],
#     "car":
#         [["front", "a"],
#          ["back", "s"]],
#     "bicycle":
#         [["front", "z"],
#          ["back", "x"]],
# }
#
# anns3 = {
#     "scene" : "konbini",
#     "object_id": ["ice_cream",
#                   "drink"],
#     "ice_cream":
#         [["vanilla", "a"],
#          ["chocolate","s"]],
#     "drink":
#         [["ocha", "z"],
#          ["coffee", "x"]],
# }
#
# anns['annotations'].append(anns1)
# toml.dump(anns, open(_filename, mode="w"))
#
# anns['annotations'].append(anns2)
# toml.dump(anns, open(_filename, mode="w"))
#
# anns['annotations'].append(anns3)
# toml.dump(anns, open(_filename, mode="w"))
# ```
