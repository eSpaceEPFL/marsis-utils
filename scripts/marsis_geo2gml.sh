#!/bin/bash
# $1 -> xml_data_model
# $2 -> xsl_tranform_model
# $.. -> file list

for f in ${@: 3}
do
#   raw_snr2gml.py E${f:1:-7}G.DAT $f E${f:1:-7}G.gml $2 $1
   marsis_geo2gml.py $f /media/federico/fc_data/MARSIS_data/L2_Data/qi2/R${f:1:-5}snr.csv  /media/federico/Backup/MARSIS/track_gmls_qi/E${f:1:-4}.gml $2 $1
done

