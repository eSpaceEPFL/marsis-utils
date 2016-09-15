# -*- coding: utf-8 -*-
# Copyright (C) 2015-2016 - EPFL - eSpace
#
# Author: Federico Cantini <federico.cantini@epfl.ch>
#
# Mantainer: Federico Cantini <federico.cantini@epfl.ch>

from numpy import array as np_array
from numpy import sum as np_sum
from numpy import mean as np_mean
from numpy import log10 as np_log10

class QualityIndex(object):
    """
    """
    def __init__(self, data_reader, run_set_data = True):
        """
        """
        self.data_reader = data_reader
        self.data_dict = data_reader.data_dict
        self.samples = data_reader.samples
        if run_set_data:
            self._set_data()
            self.compute()


    def _set_data(self):
        """
        """
        pass

    def compute(self):
        """
        """
        pass

class Track1(QualityIndex):
    """
    """

    def _set_data(self, f1_list = ['EchoModMin1F1Dip',
                                   'EchoMod0F1Dip',
                                   'EchoModPlus1F1Dip'],
                        f2_list = ['EchoModMin1F2Dip',
                                   'EchoMod0F2Dip',
                                   'EchoModPlus1F2Dip']):

        """
        """
        self.f1 = np_array([self.data_dict[key] for key in f1_list])
        self.f2 = np_array([self.data_dict[key] for key in f2_list])

    def compute(self):
        """
        """
        self.qi_f1 = np_sum(self.f1)/float(self.samples)
        self.qi_f2 = np_sum(self.f2)/float(self.samples)

class Radargram1(QualityIndex):

    """
    """
    def _set_data(self, s_list = ['EchoModMin1F1Dip',
                                   'EchoMod0F1Dip',
                                   'EchoModPlus1F1Dip',
                                   'EchoModMin1F2Dip',
                                   'EchoMod0F2Dip',
                                   'EchoModPlus1F2Dip']):

        """
        """
        self.s = np_array([self.data_dict[key] for key in s_list])

    def compute(self):
        """
        """
        self.s.sort(axis=2)

        a_sig = np_mean(self.s[:,:,-25:], axis=2)
        a_noise = np_mean(self.s[:,:,1:52], axis=2)

        self.snr = 20*np_log10(a_sig/a_noise)
