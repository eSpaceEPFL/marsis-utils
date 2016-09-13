# -*- coding: utf-8 -*-
# Copyright (C) 2015 - EPFL - eSpace
#
# Author: Federico Cantini <federico.cantini@epfl.ch>
#
# Mantainer: Federico Cantini <federico.cantini@epfl.ch>

from collections import OrderedDict

class TempData(object):
    """
    """
    def __init__(self):
        """
        """
        self.data_dict = OrderedDict()

class DataManager(object):
    """
    """

    def __init__(self, data_manager = None):
        """
        """
        self.operation_mode = None
        self.data_dict = OrderedDict()
        self.samples = None

        if data_manager:
            self.add_data_dict(data_manager)
            try:
                self.upd_operation_mode(data_manager.operation_mode)
            except AttributeError:
                pass

    def _add_data_dict(self, data_manager_to_add, replace = False):
        """
        """
        #TODO: length check
        if self.samples == None:
            self.samples = len(data_manager_to_add.data_dict[data_manager_to_add.data_dict.keys()[0]])


        for attribute in data_manager_to_add.data_dict:
            if replace == False:
                if not self.data_dict.has_key(attribute):
                    self.data_dict[attribute] = data_manager_to_add.data_dict[attribute]
            else:
                self.data_dict[attribute] = data_manager_to_add.data_dict[attribute]

        self.__dict__.update(self.data_dict)

    def add_data_dict(self, data_manager_to_add):
        """
        """
        self._add_data_dict(data_manager_to_add, replace = False)

    def replace_data_dict(self, data_manager_to_add):
        """
        """
        self._add_data_dict(data_manager_to_add, replace = True)

    def upd_operation_mode(self, operation_mode):
        """
        """
        self.operation_mode = operation_mode

    def _add_attribute_data(self, attribute_name, attribute_list):
        """
        """
        temp_data = TempData()
        temp_data.data_dict[attribute_name] = attribute_list
        return temp_data

    def add_attribute_data(self, attribute_name, attribute_list):
        """
        """
        self.add_data_dict(self._add_attribute_data(attribute_name, attribute_list))

    def replace_attribute_data(self, attribute_name, attribute_list):
        """
        """
        self.replace_data_dict(self._add_attribute_data(attribute_name, attribute_list))

    def del_attribute_data(self, attribute_name):
        """
        """
        del self.data_dict[attribute_name]

    def add_data_as_attribute(self, attribute_name, data):
        """
        """
        self.data_dict[attribute_name] = data
        self.__dict__.update(self.data_dict)

    def slice_data(self, idx):
        """
        """
        for attribute in self.data_dict:
            self.data_dict[attribute] = [self.data_dict[attribute][i] for i in idx]

        self.__dict__.update(self.data_dict)

        self.samples = len(self.data_dict[self.data_dict.keys()[0]])

    def get_len(self):
        return len(self.data_dict[self.data_dict.keys()[0]])