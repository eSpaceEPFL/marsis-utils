# -*- coding: utf-8 -*-
# Copyright (C) 2015-2016 - EPFL - eSpace
#
# Author: Federico Cantini <federico.cantini@epfl.ch>
#
# Mantainer: Federico Cantini <federico.cantini@epfl.ch>

import lxml.etree as ET
import csv
from cStringIO import StringIO
from collections import OrderedDict

from xmltodict import unparse as xd_unparse

class DataWriter(object):
    """
    """
    def __init__(self, data_reader, point_id_f = True):
        """
        """
        self.data_reader = data_reader
        self.point_id_f = point_id_f
        self.data_dict = data_reader.data_dict
        self.samples = data_reader.samples
        self._set_data()

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

    def _set_dict(self):

        point_list = []
        self.out_dict = OrderedDict()
        for sample in range(self.samples):
            point_list.append(OrderedDict())
            if self.point_id_f:
                point_list[-1]['point_id'] = sample
            for attribute in self.data_dict.keys():
                point_list[-1][attribute] = self.data_dict[attribute][sample]

        self.out_dict['orbit_point'] = point_list

    def _set_data(self):
        pass

    def write(self, out_file):
        """
        """
        fout = open(out_file, 'w')
        fout.write(self.data)
        fout.close()

class XmlWriter(DataWriter):
    """
    """

    def _set_data(self):
        """
        """
        self._set_dict()
        xmldict = OrderedDict()
        xmldict['orbit'] = self.out_dict
        self.data = xd_unparse(xmldict, pretty = True)


class GmlWriter(DataWriter):
    """
    """

    def __init__(self, data_dict, xsl_template):
        """
        """
        self.xsl_template = xsl_template
        super(GmlWriter, self).__init__(data_dict)

    def _set_data(self):
        """
        """
        xmlw = XmlWriter(self.data_reader)
        fxsl = open(self.xsl_template)
        dom = ET.parse(StringIO(xmlw.data.encode('ascii', 'ignore')))
        xslt = ET.parse(fxsl)
        fxsl.close()
        transform = ET.XSLT(xslt)
        gml = transform(dom)
        self.data = ET.tostring(gml, pretty_print=True)


class CsvWriter(DataWriter):
    """
    """
    def _set_data(self):
        """
        """
        self._set_dict()
        f = StringIO()
        writer  = csv.writer(f)

        writer.writerow(self.out_dict['orbit_point'][0].keys()) # header

        for sample in range(self.samples):
            writer.writerow(self.out_dict['orbit_point'][sample].values())

        self.data = f.getvalue()

        f.close()


class TextWriter(DataWriter):
    """
    """
    def _set_data(self):
        """
        """
        self._set_dict()
        self.f = StringIO()

        for sample in range(self.samples):
            self.write_attribute(self.out_dict['orbit_point'][sample], 0)

#        self.data = self.f.getvalue()
        #########
        text_list = []
        for row in self.f.getvalue().split("\n"):
            text_list.append(row.ljust(78)+"\r\n")

        text_list.append("END".ljust(78)+"\r\n")

        self.data = ''.join(text_list)

        #########
        self.f.close()

    def write_attribute(self, attributes_dict, level):
        for attribute in attributes_dict:
            if type(attributes_dict[attribute]) == list:
                for element in attributes_dict[attribute]:
                    self._write_sub_attribute( element, attribute, level)
            elif type(attributes_dict[attribute]) == OrderedDict:
                self._write_sub_attribute( attributes_dict[attribute], attribute, level)
            else:
                self._write_attribute (attribute, attributes_dict[attribute], level)

    def _write_sub_attribute(self, attributes_dict, attribute, level):
        self.write_attribute({'OBJECT': attribute+"\n"}, level)
        self.write_attribute(attributes_dict, level+1)
        self.write_attribute({'END_OBJECT': attribute+"\n"}, level)

    def _write_attribute(self, attribute, value, level):
        attr_str = level*'   ' + attribute
        self.f.write(attr_str)
        self.f.write((28-len(attr_str.replace('\n','')))*' ' + ' = ')
        value_string_list = list(str(value))

        ii = 0
        line_start = 0
        last_blank = 0
        for char in value_string_list[:-1]:
            if char == '\n':
                line_start = ii+1
            if char == ' ' :
                if ii-line_start >= 48:
                    value_string_list[last_blank] = '\n'
                    line_start = last_blank+1
                else:
                    last_blank = ii

            ii = ii + 1

        if len(value_string_list) - line_start >= 48:
            value_string_list[last_blank] = '\n'


        value_string = "".join(value_string_list)
        value_list = value_string.split('\n')
        self.f.write(value_list[0]+'\n')
        for ii in range(1,len(value_list)):
            self.f.write(31*' ' + value_list[ii]+'\n')

