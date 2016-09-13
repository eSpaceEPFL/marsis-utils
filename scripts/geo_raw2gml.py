#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2015 - EPFL - eSpace
#
# Author: Federico Cantini <federico.cantini@epfl.ch>
#
# Mantainer: Federico Cantini <federico.cantini@epfl.ch>

import sys
import marsis_utils.data_readers as mr
import marsis_utils.data_writers as mw

DEF_XSL = 'geo_xml2gml.xsl'
DEF_XML = 'marsisgeo.xml'

raw_geo_file = sys.argv[1]
gml_file = sys.argv[2]

if len(sys.argv) < 3:
    xsl_transform = DEF_XSL
else:
    xsl_transform = sys.argv[3]

if len(sys.argv) < 4:
    xml_data_model= DEF_XML
else:
    xml_data_model= sys.argv[4]

raw_reader = mr.RawReader(xml_data_model, raw_geo_file)
gmlw = mw.GmlWriter(raw_reader, xsl_transform)
gmlw.write(gml_file)
