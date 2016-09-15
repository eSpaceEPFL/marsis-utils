#!/bin/bash
# $1 -> xsl_tranform_model
# $.. -> file list

GEODIR=. #Write here the dir containing the txt geo data

GMLDIR=. #Write here the dir to write the gml files to

for f in ${@: 2}
do
    mkdir -p $GMLDIR/${f:0:8}
    sharad_geo2gml.py $GEODIR/$f $GMLDIR/${f:0:-3}gml $1
#    echo $f
done

