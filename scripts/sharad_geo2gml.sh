#!/bin/bash
# $1 -> xml_data_model
# $.. -> file list

for f in ${@: 2}
do
    mkdir -p gmls/${f:0:8}
    sharad_geo2gml.py $f gmls/${f:0:-3}gml $1
#    echo $f
done

