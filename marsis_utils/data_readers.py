# -*- coding: utf-8 -*-
# Copyright (C) 2015 - EPFL - eSpace
#
# Author: Federico Cantini <federico.cantini@epfl.ch>
#
# Mantainer: Federico Cantini <federico.cantini@epfl.ch>
"""
dw.flag.rfi_dect_func
=====================

Implement data reading for different formats

Classes
-------
* DataReader - Base class for data reading
* RawReader - Read binary data file
* CsvReader - Read CSV data file
"""

import os
import csv
from xmltodict import parse as xd_parse
from collections import OrderedDict
from marsis_data_IO.IO_utils import raw2data

class DataReader(object):
    """
    Base class for data reading

    *Methods*
    * get_implementations - Return the subclasses
    * get_data_size - Return the size of the data file
    * get_operation_mode - Read the operation mode from the file name
    """

    @classmethod
    def get_implementations(cls):
        """Return the subclasses
        """
        implementations = cls.__subclasses__() + [g for s in cls.__subclasses__() for g in s.get_implementations()]
        impl = []
        for implementation in implementations:
            if implementation.is_exec:
                impl.append(implementation)

        return impl

    def _get_data_size(self):
        """
        Return the size of the data file
        """
        fh = self.data_file_h
        old_file_position = fh.tell()
        fh.seek(0, os.SEEK_END)
        file_size = fh.tell()
        fh.seek(old_file_position, os.SEEK_SET)
        return file_size


    def _get_operation_mode(self, filename_string):
        """
        Read the operation mode from the file name

        *filename_string - Filename
        """
        return filename_string.split('/')[-1][8:-4]

    def _get_product_name(self, filename_string):
        """
        Read the product from the file name

        *filename_string - Filename
        """
        return filename_string.split('/')[-1].split('.')[0]

class RawReader(DataReader):
    """
    Read binary data file

    *Methods*

    * __init__ - Initialize the class
    * _get_chunk_size - Return the size of a data frame
    * _check_data_size - Check whether the file contains an integer number of frames
    * load_data - Load the data from the input file
    """

    def __init__(self, data_xml_file, data_in_file):
        """
        Parse the format descriptor and initialize variables values

        * data_xml_file - Binary format descriptor (XML file)
        * data_in_file - Input data file
        """
        fh = open(data_xml_file)
        raw_dict = xd_parse(fh.read())
        fh.close()
        self.data_in_file = data_in_file
        self.orbit_id = ""
        self.raw_dict = raw_dict[raw_dict.keys()[0]]
#        for attribute in self.raw_dict.keys():
#            self.raw_dict[attribute]['data'] = []

#        self.__dict__.update(self.raw_dict)
        self._get_chunk_size()
        self.load_data()


    def _get_chunk_size(self):
        """
        Return the size of a data frame
        """
        chunk_size = 0
        for attribute in self.raw_dict.keys():
            chunk_size = chunk_size + int(self.raw_dict[attribute]['items'])*int(self.raw_dict[attribute]['precisionbytes'])

        self.chunk_size = chunk_size

    def _check_data_size(self):
        """
        Check whether the file contains an integer number of frames
        """
        if self._get_data_size()%self.chunk_size:
            return False
        else:
            return self._get_data_size()/self.chunk_size

    def load_data(self):
        """
        Load the data from the input file
        """
        self.data_file_h = open(self.data_in_file, 'rb')
        self.samples = self._check_data_size()
        if not self.samples:
            print ("ERROR: data contains a non integer number of samples")
            return -1


        self.operation_mode = self._get_operation_mode(self.data_in_file)
        self.product_name = self._get_product_name(self.data_in_file)
        raw = self.data_file_h.read()
        self.data_dict = OrderedDict()

        self.data_dict['OperationMode'] = [None for x in range(self.samples)]
        for attribute in self.raw_dict.keys():
            self.data_dict[attribute] = [None for x in range(self.samples)]

        raw_dict_keys = self.raw_dict.keys()

#        chunk_starts = range(0, self.chunk_size*self.samples, self.chunk_size)
#        for attribute in raw_dict_keys:
#            off = self.raw_dict[attribute]['offset']
#            precision = self.raw_dict[attribute]['precision']
#            items = int(self.raw_dict[attribute]['items'])
#            attr_raw_data_list = [raw[x+off:x+off+(precision*items)]for x in chunk_starts]



        for attribute in raw_dict_keys:
            s_list = [None for x in range(self.samples)]
            offset = int(self.raw_dict[attribute]['offset'])
            precision = self.raw_dict[attribute]['precision']
            machineformat = self.raw_dict[attribute]['machineformat']
            items = int(self.raw_dict[attribute]['items'])
            precisionbytes = int(self.raw_dict[attribute]['precisionbytes'])

            for sample in range(self.samples):
                chunk = raw[sample*self.chunk_size:(sample+1)*self.chunk_size]
                attr_raw_data = chunk[offset:offset+(precisionbytes*items)]


                s_list[sample] = raw2data(attr_raw_data,
                                          precision,
                                          machineformat,
                                          precisionbytes)

            self.data_dict[attribute] = s_list

        self.data_file_h.close()
        self.__dict__.update(self.data_dict)
        return self.data_dict


class CsvReader(DataReader):
    """
    Read CSV data file

    *Methods*

    * __init__ - Initialize the class and read the data from the input file

    """
    def __init__(self, data_in_file, head = None):
        """
        """
        self.data_in_file = data_in_file
        self.data_file_h = open(data_in_file)
        csr = csv.reader(self.data_file_h)
        if not head:
            head = csr.next()
        lr = len(head)
        for ii in range(lr):
            head[ii] = head[ii].replace(' ','_').replace('+','p').replace('-','m')
        self.data_dict = OrderedDict()
        for attribute in head:
            self.data_dict[attribute] = []

        for row in csr:
            for ii in range(lr):
                row[ii] = row[ii].replace(' ','')
                self.data_dict[head[ii]].append(row[ii])

        self.data_file_h.close()
        self.__dict__.update(self.data_dict)
        self.samples = len(self.data_dict[self.data_dict.keys()[0]])








