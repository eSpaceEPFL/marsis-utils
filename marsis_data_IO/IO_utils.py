# -*- coding: utf-8 -*-
# Copyright (C) 2015-2016 - EPFL - eSpace
#
# Author: Federico Cantini <federico.cantini@epfl.ch>
#
# Mantainer: Federico Cantini <federico.cantini@epfl.ch>

from numpy import fromstring as np_fromstring
from numpy import int32
from numpy import uint32
from numpy import uint16
from numpy import float32
from numpy import float64


def raw2data(raw_data, precision, machineformat, precisionbytes):
    """
    """

    if precision == 'char':
        return raw_data

    if machineformat == 'ieee-be':
        out_data = (np_fromstring(raw_data, dtype=eval(precision), count = -1)).astype(eval(precision)).byteswap().tolist()
    else:
        out_data = (np_fromstring(raw_data, dtype=eval(precision), count = -1)).astype(eval(precision)).tolist()

    if len(out_data) == 1:
        out_data = out_data[0]

    return out_data

class Raw2Data(object):
    """
    """

    def __init__(self, precision, precisionbytes):
        """
        """
        self.precision = precision
        self.precisionbytes = precisionbytes

    def read_data(self, raw_data_l):
        pass

class Raw2Str(Raw2Data):
    """
    """

    def read_data(self, raw_data_l):
        """
        """
        return raw_data_l


class Raw2Le(Raw2Data):
    """
    """

    pass

class Raw2Be(Raw2Data):
    """
    """

    pass
