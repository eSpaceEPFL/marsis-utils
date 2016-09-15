#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2015-2016 - EPFL - eSpace
#
# Author: Federico Cantini <federico.cantini@epfl.ch>
#
# Mantainer: Federico Cantini <federico.cantini@epfl.ch>

import sys


import marsis_utils.data_readers as mr
import marsis_utils.data_manager as mm
import marsis_utils.data_writers as mw
import marsis_utils.quality_indexes as qi
import marsis_utils.plots as mp

JPEG = 0

orbit_file = sys.argv[1]
xml_file = sys.argv[2]
SNR_file = sys.argv[3]

data = mr.RawReader(xml_file, orbit_file)
qiw = qi.Track1(data)
qir = qi.Radargram1(data)

title = str(data.OrbitNumber[0]) + '   (QIf1: ' + str(qiw.qi_f1) + ')   (QIf2: ' + str(qiw.qi_f2)+')'

if JPEG:
    mp.qirplot(qir,qiw, title, figfile = str(data.OrbitNumber[0])+'.jpg')

qiman = mm.DataManager()
attr_name = ['SNR f1 -1',
             'SNR f1  0',
             'SNR f1 +1',
             'SNR f2 -1',
             'SNR f2  0',
             'SNR f2 +1']

qiman.add_attribute_data('f1', data.Freq1)
qiman.add_attribute_data('f2', data.Freq2)

ii = 0
for attr in attr_name:
    qiman.add_attribute_data(attr, qir.snr[ii,:].tolist())
    ii = ii+1

csvw = mw.CsvWriter(qiman)
csvw.write(orbit_file.split('/')[-1][:-4]+'_snr.csv')

fqi = open(SNR_file, 'a')
fqi.write(str(data.OrbitNumber[0])+' '+str(qiw.qi_f1)+' '+str(qiw.qi_f2)+'\r\n')
fqi.close()
