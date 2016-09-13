#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2016 - EPFL - eSpace
#
# Author: Federico Cantini <federico.cantini@epfl.ch>
#
# Mantainer: Federico Cantini <federico.cantini@epfl.ch>

import sys
from csv import reader as csv_reader
import marsis_utils.data_readers as mr
import marsis_utils.data_writers as mw
import marsis_utils.data_manager as dm

def _read_quality_ids(self, qi_file = '/home/federico/Documents/iMars/labelPDS/qi/qi.txt'):
    qi_fh = open(qi_file)
    csr=csv_reader(qi_fh, delimiter = ' ')
    for row in csr:
        self.qi[int(row[0])] = row[1]+row[2]

def get_quality_id(orbit_number, qi_file = '/home/federico/Documents/iMars/labelPDS/qi/qi.txt'):

    qi_fh = open(qi_file)
    csr=csv_reader(qi_fh, delimiter = ' ')
    qi = {}
    for row in csr:
        qi[int(row[0])] = row[1]+row[2]

    try:
        qid = qi[orbit_number]
    except KeyError:
        qid = '00'

    return qid

DEF_XSL = 'geo_xml2gml.xsl'
DEF_XML = 'marsisgeo.xml'

raw_geo_file = sys.argv[1]
csv_file = sys.argv[2]
gml_file = sys.argv[3]


if len(sys.argv) < 4:
    xsl_transform = DEF_XSL
else:
    xsl_transform = sys.argv[4]

if len(sys.argv) < 5:
    xml_data_model= DEF_XML
else:
    xml_data_model= sys.argv[5]

raw_reader = mr.RawReader(xml_data_model, raw_geo_file)
qid = get_quality_id(raw_reader.Orbit[0])

csr = mr.CsvReader(csv_file)
datam = dm.DataManager(raw_reader)
datam.add_data_dict(csr)
datam.add_attribute_data('qi1', [qid[0]]*len(raw_reader.Orbit))
datam.add_attribute_data('qi2', [qid[1]]*len(raw_reader.Orbit))
gmlw = mw.GmlWriter(datam, xsl_transform)
gmlw.write(gml_file)


