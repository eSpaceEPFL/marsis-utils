# -*- coding: utf-8 -*-
# Copyright (C) 2015 - EPFL - eSpace
#
# Author: Federico Cantini <federico.cantini@epfl.ch>
#
# Mantainer: Federico Cantini <federico.cantini@epfl.ch>
import os.path, time

from collections import OrderedDict
from datetime import datetime

from numpy import diff
from matplotlib.mlab import find
from csv import reader as csv_reader

class L2Labels(object):

    def __init__(self):
#        self.data_dict = data_dict
        self.first_orbit = []
        self.phase_name = []
        self.qi = {}

        self._read_mission_phases()
        self._read_quality_ids()

        self.creation_time = None

#        self.__set_label_dict()

    def _reset(self):
        self.foot_start_idx = None
        self.foot_stop_idx = None
        self.orbit_number = -1
#        self.creation_time = None

    def set_data(self, data_dict):
        self._reset()
        self.data_dict = data_dict
        self._get_footprint_idx()
        self.__set_label_dict()

    def __set_label_dict(self):
        self.label_dict = OrderedDict()

        self.label_dict['PDS_VERSION_ID'] = 'PDS3'
        self.label_dict['LABEL_REVISION_NOTE'] = '"R. Orosei, 2013-10-02"'+'\n'

        self.label_dict['DATA_SET_ID'] = self.get_data_set_id()
        self.label_dict['DATA_SET_NAME'] = self.get_data_set_name()
        self.label_dict['PRODUCT_ID'] = self.get_product_id()
        self.label_dict['PRODUCT_TYPE'] = 'RDR'
        self.label_dict['PRODUCT_CREATION_TIME'] = self.get_creation_time()
        self.label_dict['RELEASE_ID'] = self.get_release_id()
        self.label_dict['REVISION_ID'] = self.get_revision_id()+'\n'

        self.label_dict['MISSION_ID'] = 'MEX'
        self.label_dict['MISSION_NAME'] = '"MARS EXPRESS"'
        self.label_dict['INSTRUMENT_HOST_ID'] = 'MEX'
        self.label_dict['INSTRUMENT_HOST_NAME'] = '"MARS EXPRESS"'
        self.label_dict['INSTRUMENT_ID'] = 'MARSIS'
        self.label_dict['INSTRUMENT_NAME'] = '"MARS ADVANCED RADAR FOR SUBSURFACE AND IONOSPHERE SOUNDING"'
        self.label_dict['INSTRUMENT_TYPE'] = 'RADAR'
        self.label_dict['INSTRUMENT_MODE_ID'] = self.get_mode_id()
        self.label_dict['INSTRUMENT_MODE_DESC'] = self.get_mode_desc()+'\n'

        self.label_dict['MISSION_PHASE_NAME'] = self.get_phase_name()
        self.label_dict['ORBIT_NUMBER'] = self.get_orbit_number()
        self.label_dict['START_TIME'] = self.get_start_time()
        self.label_dict['STOP_TIME'] = self.get_stop_time()
        self.label_dict['SPACECRAFT_CLOCK_START_COUNT'] = self.get_clock_start()
        self.label_dict['SPACECRAFT_CLOCK_STOP_COUNT']  = self.get_clock_stop()
        self.label_dict['TARGET_NAME'] = self.get_target_name()
        self.label_dict['TARGET_TYPE'] = self.get_target_type()+'\n'

        self.label_dict['PROCESSING_LEVEL_ID'] = '3'
        self.label_dict['PROCESSING_LEVEL_DESC'] = '"Irreversibly tranformed (e.g., resampled, remapped, calibrated) values of the instrument measurements (e.g., radiances, magnetic field strenght)"'
        self.label_dict['DATA_QUALITY_ID'] = self.get_quality_id()
        self.label_dict['DATA_QUALITY_DESC'] = '"0: data quality unknown; 1: median data quality index in the bottom 25% of computed values; 2: median data quality index in the bottom 50% of computed values; 3: median data quality index in the top 50% of computed values; 4: median data quality index in the top 25% of computed values. For instrument mode transmitting at two different frequencies, DATA_QUALITY_ID reports a value for every frequency."'
        self.label_dict['FOOTPRINT_POINT_LONGITUDE'] = self.get_footprint_long()
        self.label_dict['FOOTPRINT_POINT_LATITUDE'] = self.get_footprint_lat()+'\n'

        self.label_dict['PRODUCER_ID'] = 'MARSIS_TEAM'
        self.label_dict['PRODUCER_FULL_NAME'] = '"GIOVANNI PICARDI"'
        self.label_dict['PRODUCER_INSTITUTION_NAME'] = '"UNIVERSITY OF ROME LA SAPIENZA"'+'\n'+'\n'

        self.label_dict['FILE'] = OrderedDict([('RECORD_TYPE', 'FIXED_LENGTH'),
                                               ('RECORD_BYTES', self.get_record_bytes()),
                                               ('FILE_RECORDS', str(self.get_file_record())+'\n'),
                                               ('^SCIENCE_DATA_TABLE', '"'+self.get_product_id()+'.DAT"\n'),
                                               ('SCIENCE_DATA_TABLE', OrderedDict([('INTERCHANGE_FORMAT', 'BINARY'),
                                                                                        ('ROWS', self.get_file_record()),
                                                                                        ('ROW_BYTES', self.get_record_bytes()),
                                                                                        ('COLUMNS', 48),
                                                                                        ('DESCRIPTION', '"Each row of the table contains a frame, that is a processed batch of a variable number of echoes. The beginning of each record contains ancillary data, i.e. parameters describing pulse transmission, echo reception and on-board processing. The main part of the record contains one complex spectrum of the processed signal (one vector for the real part and one for the imaginary part) for each antenna, for each band and for each filter of the instrument mode. The final part of the record contains geometric quantities generated on-ground from spacecraft navigation data."'),
                                                                                        ('^STRUCTURE', '"R_SS3_TRK_CMP.FMT"\n')]
                                                                                      )
                                               )])

        #OBJECT                       = FILE
        #
        #  RECORD_TYPE                = FIXED_LENGTH
        #  RECORD_BYTES               = record_bytes_frm
        #  FILE_RECORDS               = file_records_frm
        #
        #  ^SCIENCE_TELEMETRY_TABLE   = science_telemetry_table
        #
        #  OBJECT                     = SCIENCE_TELEMETRY_TABLE
        #
        #    INTERCHANGE_FORMAT       = BINARY
        #    ROWS                     = rows_frm
        #    ROW_BYTES                = row_bytes_frm
        #    COLUMNS                  = columns_frm
        #    DESCRIPTION              = description_frm
        #    ^STRUCTURE               = structure_frm
        #
        #  END_OBJECT                 = SCIENCE_TELEMETRY_TABLE
        #
        #END_OBJECT                   = FILE
        #
        #
        #OBJECT                       = FILE
        #
        #  RECORD_TYPE                = FIXED_LENGTH
        #  RECORD_BYTES               = 215
        #  FILE_RECORDS               = file_records_geo
        #
        #  ^AUXILIARY_DATA_TABLE      = auxiliary_data_table
        #
        #  OBJECT                     = AUXILIARY_DATA_TABLE
        #
        #    INTERCHANGE_FORMAT       = BINARY
        #    ROWS                     = rows_geo
        #    ROW_BYTES                = 215
        #    COLUMNS                  = 19
        #    DESCRIPTION              = "Table listing geometric quantities generated on-ground from spacecraft navigation data. This table is associated to a binary file containing instrument science telemetry, and contains one line for each line in the science telemetry table."
        #    ^STRUCTURE               = "E_GEO.FMT"
        #
        #  END_OBJECT                 = AUXILIARY_DATA_TABLE
        #
        #END_OBJECT                   = FILE
        #
        #
        #END

    def set_creation_time(self, ct):
        self.creation_time = ct

    def get_data_set_id(self):
        orbnum = self.get_orbit_number()
        if orbnum <= 2418:
            return 'MEX-M-MARSIS-3-RDR-SS-V2.0'
        elif orbnum <= 4918:
            return 'MEX-M-MARSIS-3-RDR-SS-EXT1-V2.0'
        elif orbnum <= 6836:
            return 'MEX-M-MARSIS-3-RDR-SS-EXT2-V1.0'
        elif orbnum <= 11453:
            return 'MEX-M-MARSIS-3-RDR-SS-EXT3-V1.0'
        elif orbnum <= 13960:
            return 'MEX-M-MARSIS-3-RDR-SS-EXT4-V1.0'
        else:
            return 'MEX-M-MARSIS-3-RDR-SS-EXT5-V1.0'

    def get_data_set_name(self):
        orbnum = self.get_orbit_number()
        if orbnum <= 2418:
            return '"MARS EXPRESS MARS MARSIS REDUCED DATA RECORD SUBSURFACE V2.0"'
        elif orbnum <= 4918:
            return '"MARS EXPRESS MARS MARSIS REDUCED DATA RECORD SUBSURFACE EXTENSION 1 V2.0"'
        elif orbnum <= 6836:
            return '"MARS EXPRESS MARS MARSIS REDUCED DATA RECORD SUBSURFACE EXTENSION 2 V1.0"'
        elif orbnum <= 11453:
            return '"MARS EXPRESS MARS MARSIS REDUCED DATA RECORD SUBSURFACE EXTENSION 3 V1.0"'
        elif orbnum <= 13960:
            return '"MARS EXPRESS MARS MARSIS REDUCED DATA RECORD SUBSURFACE EXTENSION 4 V1.0"'
        else:
            return '"MARS EXPRESS MARS MARSIS REDUCED DATA RECORD SUBSURFACE EXTENSION 5 V1.0"'

    def get_product_id(self):
        return self.data_dict.product_name

    def get_creation_time(self):
        if self.creation_time:
            return self.creation_time
        else:
            return datetime.fromtimestamp(os.path.getctime(self.data_dict.data_in_file)).strftime('%Y-%m-%dT%H:%M:%S')
#        return datetime.strftime(datetime.now(), '%Y-%m-%dT%H:%M:%S')


    def get_release_id(self):
        return "0001"

    def get_revision_id(self):
        return "0000"

    def get_mode_id(self):
        return 'SS3_TRK_CMP'
#        return self.data_dict.operation_mode

    def get_mode_desc(self):
        self._set_mode_dict()

        for mode in self.mode_dict.keys():
            if self.label_dict['INSTRUMENT_MODE_ID'].find(mode) >= 0:
                return self.mode_dict[mode]

    def get_phase_name(self):
        orb = self.get_orbit_number()
        for ii in range(len(self.first_orbit)):
            if int(orb)<int(self.first_orbit[ii]):
                return '"'+self.phase_name[ii-1]+'"'


    def get_orbit_number(self):
        return self.data_dict.Orbit[0]

    def get_start_time(self):
        return self.data_dict.GeoEp[0]

    def get_stop_time(self):
        return self.data_dict.GeoEp[-1]

    def _get_clock(self, idx):
        return '"1/'+ str(self.data_dict.ScetW[idx]).zfill(10) + '.' + str(self.data_dict.ScetF[idx]).zfill(5) + '"'

    def get_clock_start(self):
        return self._get_clock(0)

    def get_clock_stop(self):
        return self._get_clock(-1)

    def get_target_name(self):
        target_name = self.data_dict.Target[0]
        if target_name.find('TEST') >= 0:
            target_name = 'NON SCIENCE'

        target_name = '"'+target_name.strip()+'"'

        return target_name

    def get_target_type(self):
        target_name = self.get_target_name()
        if target_name.find('NON SCIENCE') >= 0:
            return '"CALIBRATION"'

        if target_name.find('MARS') >= 0:
            return '"PLANET"'

        if target_name.find('PHOBOS') >= 0:
            return '"SATELLITE"'

    def _read_quality_ids(self, qi_file = '/home/federico/Documents/iMars/labelPDS/qi/qi.txt'):
        qi_fh = open(qi_file)
        csr=csv_reader(qi_fh, delimiter = ' ')
        for row in csr:
            self.qi[int(row[0])] = row[1]+row[2]

    def get_quality_id(self):
        try:
            qid = self.qi[self.get_orbit_number()]
        except KeyError:
            qid = '00'

        return qid

    def _get_footprint_idx(self):
        if not (self.foot_start_idx):
            start_idx_a = find(diff(self.data_dict.EphemT)>10)
            stop_idx_a = start_idx_a - 1

            self.foot_start_idx = [0]+start_idx_a.tolist()
            self.foot_stop_idx = stop_idx_a.tolist()+[len(self.data_dict.EphemT)-1]


    def _get_footprint_lon_lat(self, lon_lat_data):
        out_str = "("
        for ii in range(len(self.foot_start_idx)):
            out_str = out_str+"("
            out_str = out_str+str(round(lon_lat_data[self.foot_start_idx[ii]],3))+","
            out_str = out_str+str(round(lon_lat_data[self.foot_stop_idx[ii]],3))
            out_str = out_str+"), "

        out_str = out_str[0:-2]+")"

        return out_str

    def get_footprint_long(self):
        return self._get_footprint_lon_lat(self.data_dict.ScELon)

    def get_footprint_lat(self):
        return self._get_footprint_lon_lat(self.data_dict.ScLat)

    def _set_mode_dict(self):
        self.mode_dict={'AIS': '"In this mode, the instrument transmits 160 short, narrow-band pulses at different frequencies. The signal is acquired through the dipole antenna. Receiving windows are divided into 80 segments, each of which is as long as the transmitted pulse: power received within each segment is computed, and the result is stored for down-link."',
                        'CAL': '"In this mode, the instrument transmits a frequency-modulated waveform having a 1 MHz bandwidth. The signal is acquired through both the dipole and the monopole antennas. The instrument collects data during 80 receiving windows, then transmits them to the ground without any on-board processing."',
                        'RXO': '"In this mode, the instrument is not transmitting. The signal is acquired through both the dipole and the monopole antennas. The instrument collects data during 80 receiving windows, then transmits them to the ground without any on-board processing."',
                        'SS1_ACQ_CMP': '"In this mode, the instrument transmits a frequency-modulated waveform having a 200 kHz bandwidth. The signal is acquired through the dipole antenna. An altitude-dependent number of echoes (of the order of hundred) is collected in a single batch. Doppler processing adds a delay to the samples of each echo, and then sums the samples so as to allow the constructive sum of the signal component coming from a desired direction. Each coherent sum of the echoes is called a synthesized filter: this mode produces 1 filter."',
                        'SS1_TRK_CMP': '"In this mode, the instrument transmits two frequency-modulated waveforms in close succession, each having a 1 MHz bandwidth but centered at a different frequency. The signal is acquired through both the dipole and the monopole antennas. An altitude-dependent number of echoes (of the order of hundred) is collected in a single batch. Doppler processing adds a delay to the samples of each echo, and then sums the samples so as to allow the constructive sum of the signal component coming from a desired direction. Each coherent sum of the echoes is called a synthesized filter: this mode produces 1 filter for every frequency and for every antenna."',
                        'SS2_ACQ_CMP': '"In this mode, the instrument transmits a frequency-modulated waveform having a 200 kHz bandwidth. The signal is acquired through the dipole antenna. An altitude-dependent number of echoes (of the order of hundred) is collected in a single batch. Doppler processing adds a delay to the samples of each echo, and then sums the samples so as to allow the constructive sum of the signal component coming from a desired direction. Each coherent sum of the echoes is called a synthesized filter: this mode produces 1 filter."',
                        'SS2_TRK_CMP': '"In this mode, the instrument transmits two frequency-modulated waveforms in close succession, each having a 1 MHz bandwidth but centered at a different frequency. The signal is acquired through the dipole antenna. An altitude-dependent number of echoes (of the order of hundred) is collected in a single batch. Doppler processing adds a delay to the samples of each echo, and then sums the samples so as to allow the constructive sum of the signal component coming from a desired direction. Each coherent sum of the echoes is called a synthesized filter: this mode produces 1 filter for every frequency. Range processing consists in computing the correlation between the transmitted pulse and received echoes. Multi-look processing sums echoes non-coherently, after both Doppler and range processing, to increase the signal-to-noise ratio and reduce speckle."',
                        'SS3_ACQ_CMP': '"In this mode, the instrument transmits a frequency-modulated waveform having a 200 kHz bandwidth. The signal is acquired through the dipole antenna. An altitude-dependent number of echoes (of the order of hundred) is collected in a single batch. Doppler processing adds a delay to the samples of each echo, and then sums the samples so as to allow the constructive sum of the signal component coming from a desired direction. Each coherent sum of the echoes is called a synthesized filter: this mode produces 1 filter."',
                        'SS3_TRK_CMP': '"In this mode, the instrument transmits two frequency-modulated waveforms in close succession, each having a 1 MHz bandwidth but centered at a different frequency. The signal is acquired through the dipole antenna. An altitude-dependent number of echoes (of the order of hundred) is collected in a single batch. Doppler processing adds a delay to the samples of each echo, and then sums the samples so as to allow the constructive sum of the signal component coming from a desired direction. Each coherent sum of the echoes is called a synthesized filter: this mode produces 3 filters for every frequency."',
                        'SS4_ACQ_CMP': '"In this mode, the instrument transmits a frequency-modulated waveform having a 200 kHz bandwidth. The signal is acquired through the dipole antenna. An altitude-dependent number of echoes (of the order of hundred) is collected in a single batch. Doppler processing adds a delay to the samples of each echo, and then sums the samples so as to allow the constructive sum of the signal component coming from a desired direction. Each coherent sum of the echoes is called a synthesized filter: this mode produces 1 filter."',
                        'SS4_TRK_CMP': '"In this mode, the instrument transmits a frequency-modulated waveform having a 1 MHz bandwidth. The signal is acquired through both the dipole and the monopole antennas. An altitude-dependent number of echoes (of the order of hundred) is collected in a single batch. Doppler processing adds a delay to the samples of each echo, and then sums the samples so as to allow the constructive sum of the signal component coming from a desired direction. Each coherent sum of the echoes is called a synthesized filter: this mode produces 5 filters for every antenna."',
                        'SS5_ACQ_CMP': '"In this mode, the instrument transmits trains of four short identical unmodulated pulses. The signal is acquired through the dipole antenna. An altitude-dependent number of echoes (of the order of hundred) is collected in a single batch. Doppler processing adds a delay to the samples of each echo, and then sums the samples so as to allow the constructive sum of the signal component coming from a desired direction. Each coherent sum of the echoes is called a synthesized filter: this mode produces 1 filter."',
                        'SS5_TRK_CMP': '"In this mode, the instrument transmits trains of four short identical unmodulated pulses. The signal is acquired through both the dipole and the monopole antennas. An altitude-dependent number of echoes (of the order of hundred) is collected in a single batch. Doppler processing adds a delay to the samples of each echo, and then sums the samples so as to allow the constructive sum of the signal component coming from a desired direction. Each coherent sum of the echoes is called a synthesized filter: this mode produces 3 filters for every antenna."'}

    def _read_mission_phases(self, phases_file = '/home/federico/Documents/iMars/labelPDS/label PDS/MEX_Science_SubPhase_Definitions.TAB'):
        with open(phases_file) as f:
            lines = f.readlines()

            first_orbit = []
            phase_name = []
            lines=lines[2:-1]
            for line in lines:
                first_orbit.append(int(line[14:19]))
                phase_name.append(line[25:36])

        self.first_orbit = first_orbit
        self.phase_name = phase_name
        return (first_orbit, phase_name)

    def get_file_record(self):
        return self.data_dict.samples

    def get_record_bytes(self):
        return self.data_dict.chunk_size

class L2BrowseLabels(L2Labels):

    def set_data(self, data_dict):
        self._reset()
        self.data_dict = data_dict
        self.__set_label_dict()

    def __set_label_dict(self):
        self.label_dict = OrderedDict()

        self.label_dict['PDS_VERSION_ID'] = 'PDS3'
        self.label_dict['RECORD_TYPE'] = 'UNDEFINED'+'\n'

        self.label_dict['DATA_SET_ID'] = self.get_data_set_id()
        self.label_dict['DATA_SET_NAME'] = self.get_data_set_name()
        self.label_dict['SOURCE_PRODUCT_ID'] = self.get_source_id()
        self.label_dict['PRODUCT_ID'] = self.get_product_id()
        self.label_dict['PRODUCT_CREATION_TIME'] = self.get_creation_time()
        self.label_dict['RELEASE_ID'] = self.get_release_id()
        self.label_dict['REVISION_ID'] = self.get_revision_id()+'\n'

        self.label_dict['MISSION_ID'] = 'MEX'
        self.label_dict['MISSION_NAME'] = '"MARS EXPRESS"'
        self.label_dict['INSTRUMENT_HOST_ID'] = 'MEX'
        self.label_dict['INSTRUMENT_HOST_NAME'] = '"MARS EXPRESS"'
        self.label_dict['INSTRUMENT_ID'] = 'MARSIS'
        self.label_dict['INSTRUMENT_NAME'] = '"MARS ADVANCED RADAR FOR SUBSURFACE AND IONOSPHERE SOUNDING"'
        self.label_dict['INSTRUMENT_TYPE'] = 'RADAR'
        self.label_dict['INSTRUMENT_MODE_ID'] = self.get_mode_id()
        self.label_dict['INSTRUMENT_MODE_DESC'] = self.get_mode_desc()+'\n'

        self.label_dict['MISSION_PHASE_NAME'] = self.get_phase_name()
        self.label_dict['ORBIT_NUMBER'] = self.get_orbit_number()
        self.label_dict['START_TIME'] = self.get_start_time()
        self.label_dict['STOP_TIME'] = self.get_stop_time()
        self.label_dict['SPACECRAFT_CLOCK_START_COUNT'] = self.get_clock_start()
        self.label_dict['SPACECRAFT_CLOCK_STOP_COUNT']  = self.get_clock_stop()
        self.label_dict['TARGET_NAME'] = self.get_target_name()
        self.label_dict['TARGET_TYPE'] = self.get_target_type()+'\n'

        self.label_dict['DATA_QUALITY_ID'] = self.get_quality_id()
        self.label_dict['DATA_QUALITY_DESC'] = '"0: data quality unknown; 1: median data quality index in the bottom 25% of computed values; 2: median data quality index in the bottom 50% of computed values; 3: median data quality index in the top 50% of computed values; 4: median data quality index in the top 25% of computed values. For instrument mode transmitting at two different frequencies, DATA_QUALITY_ID reports a value for every frequency."'

        self.label_dict['PRODUCER_ID'] = 'MARSIS_TEAM'
        self.label_dict['PRODUCER_FULL_NAME'] = '"GIOVANNI PICARDI"'
        self.label_dict['PRODUCER_INSTITUTION_NAME'] = '"UNIVERSITY OF ROME LA SAPIENZA"'+'\n'+'\n'

        self.label_dict['^BROWSE_IMAGE'] = self.get_product_id()+'\n\n'

        self.label_dict['BROWSE_IMAGE'] = OrderedDict([('ENCODING_TYPE', 'PNG'),
                                               ('INTERCHANGE_FORMAT', 'BINARY'),
                                               ('LINES', str(512*6)),
                                               ('LINE_SAMPLES', str(self.get_file_record())),
                                               ('SAMPLE_BITS', '"N/A"'),
                                               ('SAMPLE_TYPE', '"N/A"'),
                                               ('DESCRIPTION', '"This image consists of multiple radargrams, their number depending on instrument mode, arranged in a vertical sequence. Each radargram is a representation of radar echoes acquired continuously during the movement of the spacecraft as a grey-scale image, in which the horizontal dimension is distance along the ground track, the vertical dimension is the round trip time of the echo, and the brightness of the pixel is proportional to the logarithm of the modulus of the complex echo sample."\n')
                                               ])

    def get_product_id(self):
        return '"'+self.data_dict.product_name+'.PNG"'

    def get_source_id(self):
        return '"'+self.data_dict.product_name+'"'#+'.DAT"'
