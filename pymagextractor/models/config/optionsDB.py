# TODO: implement an easier toml file
import xml.etree.ElementTree as etree
from pymagextractor.models.container.object import Object
from pymagextractor.models.container.object_view import ObjectView


class OptionsDB:

    def __init__(self):
        self.object_list = []

    def search_object(self, object_name):
        """Look for an object by the name"""
        for my_object in self.object_list:
            if my_object.name == object_name:
                return my_object

    def add_object(self, new_object):
        """Add new object"""
        if not self.search_object(new_object.name):
            self.object_list.append(new_object)
            self.object_list.sort(key=lambda x: x.name)
            return True
        else:
            return False

    def delete_object(self, object_selected):
        """Delete object"""
        self.object_list.remove(object_selected)

    def save_db(self, path):
        """Save all objects information on a xml file"""
        top = etree.Element('Options')

        comment = etree.Comment('Options database for pymagextractor')
        top.append(comment)

        for my_object in self.object_list:
            object_child = etree.SubElement(top, 'object', {'name': my_object.name})
            for my_view in my_object.view_list:
                view_child = etree.SubElement(object_child, 'view', {'name': my_view.name})
                view_path = etree.SubElement(view_child, 'path')
                view_path.text = my_view.path

        tree = etree.ElementTree(top)
        tree.write(path)

    def load_db(self, path):
        """Load xml file on the program"""
        tree = etree.parse(path)
        root = tree.getroot()

        for parsed_object in root.findall('object'):
            new_object = Object()
            new_object.name = parsed_object.get('name')
            for parsed_view in parsed_object.findall("view"):
                new_view = ObjectView(new_object)
                name = parsed_view.get('name')
                path = parsed_view.find('path').text
                new_view.name = name
                new_view.path = path
                new_object.add_view(new_view)
            self.add_object(new_object)
