#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2015-2016 - EPFL - eSpace
#
# Author: Federico Cantini <federico.cantini@epfl.ch>
#
# Mantainer: Federico Cantini <federico.cantini@epfl.ch>

sharad_geo_lbl_head = ['point_id', 'epoch', 'lat', 'lon', 'mars_r', 'sc_r', 'rad_v', 'tan_v', 'sza', 'phase']

import sys
import marsis_utils.data_readers as mr
import marsis_utils.data_writers as mw
import marsis_utils.data_manager as dm

DEF_XSL = '../xsl/sharad_geo_xml2gml.xsl'

geo_file = sys.argv[1]
gml_file = sys.argv[2]

if len(sys.argv) < 3:
    xsl_transform = DEF_XSL
else:
    xsl_transform = sys.argv[3]

orb = geo_file.split('/')[-1][2:10]

csr = mr.CsvReader(geo_file, head = sharad_geo_lbl_head)
csrm = dm.DataManager(csr)
csrm.add_data_as_attribute('Orbit', [int(orb)]*csrm.get_len())
gmlw = mw.GmlWriter(csrm, xsl_transform)
gmlw.write(gml_file)
