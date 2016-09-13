#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2015-2016 - EPFL - eSpace
#
# Author: Federico Cantini <federico.cantini@epfl.ch>
#
# Mantainer: Federico Cantini <federico.cantini@epfl.ch>

import sys
import os
from datetime import datetime

import marsis_utils.data_readers as mr
import marsis_utils.data_manager as mm
import marsis_utils.data_writers as mw
import marsis_utils.data_labels as dl


def write_with_data(orbit_file, orbit_dir):
    return orbit_file[0:-3]+'LBL'

def write_single_dir(orbit_file, orbit_dir):
    return lab_dir+orbit_file.split('/')[-1][0:-3]+'LBL'

def write_struct_dir(orbit_file, orbit_dir):
    filen = orbit_file.split('/')[-1][0:-3]+'LBL'
    orb_sdir = orbit_dir+'/RDR'+filen[2:6]+'X'
    if not os.path.exists(orb_sdir):
        os.makedirs(orb_sdir)

    return orb_sdir+'/'+filen


lab_dir = None

xml_file = sys.argv[1]

l2_lab = dl.L2BrowseLabels()

file_list = sys.argv[2:]

if len(file_list) == 1:
    file_list = file_list[0].split(";")

#print str(len(file_list))+"\n"
#print file_list
for orbit_file in file_list:
    print "Processing "+orbit_file+"..."
    labman = mm.DataManager()
    data = mr.RawReader(xml_file, orbit_file)

    browse_file = '/media/federico/Backup/MARSIS/L2_Data/BROWSE/'+orbit_file.split("/")[-2]+"/"+orbit_file.split("/")[-1]
    browse_file = browse_file[:-3]+'png'
#    print browse_file
#    print datetime.fromtimestamp(os.path.getctime(browse_file)).strftime('%Y-%m-%d %H:%M:%S')
    l2_lab.set_creation_time(datetime.fromtimestamp(os.path.getctime(browse_file)).strftime('%Y-%m-%dT%H:%M:%S'))
    l2_lab.set_data(data)

    for key in l2_lab.label_dict.keys():
        labman.add_attribute_data(key, [l2_lab.label_dict[key]])


    labwr = mw.TextWriter(labman, point_id_f = False)
#    if lab_dir:
#        labwr.write(lab_dir+orbit_file.split('/')[-1][0:-3]+'LBL')
#    else:
#        labwr.write(orbit_file[0:-3]+'LBL')

#    labwr.write(write_struct_dir(orbit_file, '/media/federico/Backup/MARSIS/L2_Data/BROWSE_LABELS'))
    labwr.write(write_struct_dir(orbit_file, '/home/federico/iMars/BROWSE_LABELS'))

