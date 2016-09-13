# -*- coding: utf-8 -*-
# Copyright (C) 2015 - EPFL - eSpace
#
# Author: Federico Cantini <federico.cantini@epfl.ch>
#
# Mantainer: Federico Cantini <federico.cantini@epfl.ch>

import matplotlib.pyplot as plt
from numpy import log10 as np_log10



def qirplot(qir, qiw, title, figfile=None):
    f, ax = plt.subplots(6,2, sharex=True)
    f.set_size_inches(18.5, 10.5)
    f.suptitle(title)
    for ii in range(3):


        ax[2*ii,0].imshow(20*np_log10(qiw.f1[ii,:,:].transpose()), cmap = 'gray')
        ax[2*ii,0].set_title('Freq1 - filter' + str(ii-1))
        ax[2*ii,1].imshow(20*np_log10(qiw.f2[ii,:,:].transpose()), cmap = 'gray')
        ax[2*ii,1].set_title('Freq2 - filter' + str(ii-1))

        ax[2*ii+1,0].plot(qir.snr[ii,:])
        ax[2*ii+1,1].plot(qir.snr[ii+3,:])

    if figfile:
        f.savefig(figfile, dpi=100)
    else:
        f.show()


