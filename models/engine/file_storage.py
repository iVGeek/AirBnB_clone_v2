#!/usr/bin/python3
"""
module containing FileStorage used for file storage
"""
import json
import models


class FileStorage:
    def __init__(self):
        # Initialize attributes
        self.__file_path = "file.json"
        self.__objects = {}

    def all(self, cls=None):
        # Returns a dictionary of all objects
        if cls is None:
            return self.__objects
        else:
            objects_dict = {}
            for key, value in self.__objects.items():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    objects_dict[key] = value
            return objects_dict

    def new(self, obj):
        # Sets in __objects the obj with key <obj class name>.id
        key = obj.__class__.__name__ + "." + obj.id
        self.__objects[key] = obj

    def save(self):
        # Serializes __objects to the JSON file (path: __file_path)
        objects_dict = {}
        for key, value in self.__objects.items():
            objects_dict[key] = value.to_dict()

        with open(self.__file_path, "w") as f:
            json.dump(objects_dict, f)

    def reload(self):
        # Deserializes the JSON file to __objects (only if the file exists)
        try:
            with open(self.__file_path, "r") as f:
                objects_dict = json.load(f)
                for key, value in objects_dict.items():
                    class_name, obj_id = key.split(".")
                    class_ = classes[class_name]
                    obj = class_(**value)
                    self.__objects[key] = obj
        except FileNotFoundError:
            pass

    def close(self):
        # Calls the reload method for deserializing the JSON file to objects
        self.reload()

