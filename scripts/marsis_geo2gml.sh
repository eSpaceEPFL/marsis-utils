#!/bin/bash
# $1 -> xml_data_model
# $2 -> xsl_tranform_model
# $.. -> file list


GEODIR=. #Write here the dir containing the raw geo data
SNRDIR=. #Write here the dir containing the SNR csv files

GMLDIR=. #Write here the dir to write the gml files to

for f in ${@: 3}
do
#   raw_snr2gml.py E${f:1:-7}G.DAT $f E${f:1:-7}G.gml $2 $1
   marsis_geo2gml.py $GEODIR/$f $SNRDIR/R${f:1:-5}snr.csv  $GMLDIR/E${f:1:-4}.gml $2 $1
done

