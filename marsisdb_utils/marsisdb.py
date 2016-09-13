# -*- coding: utf-8 -*-
# Copyright (C) 2015 - EPFL - eSpace
#
# Author: Federico Cantini <federico.cantini@epfl.ch>
#
# Mantainer: Federico Cantini <federico.cantini@epfl.ch>

from string import Template

class MarsisView(object):
    """
    """
    def __init__(self, template_file, data_manager):
        """
        """
        self.temp_dict = {}
        th = open(template_file)
        self.temp = th.read()
        th.close()
        self._add_data(data_manager)
        self._set_view_text()

    def _add_data(self, data_manager):
        """
        """
        attr_str = ""
        for s in data_manager.data_dict.iterkeys():
            attr_str = attr_str +", " + s.lower()

        self.temp_dict['attributes_list'] = attr_str
        self.temp_dict['geometry_name'] = 'geometry'

    def set_geo_name(self, geo_name):
        """
        """
        self.temp_dict['geometry_name'] = geo_name
        self._set_view_text()

    def _set_view_text(self):
        """
        """
        src = Template(self.temp)
        self.view_str = src.safe_substitute(self.temp_dict)

    def add_roi(self, roi_d):
        """
        """
        for roi in roi_d.keys():
                self.view_str = self.view_str + "\r\n\r\n#" + roi + "\r\n" + ". create_roi_views.sh $1 " + roi + " " + roi_d[roi]

    def write(self, file_out):
        """
        """
        fh = open(file_out, 'w')
        fh.write(self.view_str)
        fh.close()
