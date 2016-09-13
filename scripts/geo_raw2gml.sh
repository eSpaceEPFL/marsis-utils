#!/bin/bash
# $1 -> xml_data_model
# $2 -> xsl_tranform_model
# $.. -> file list

for f in ${@: 3}
do
    geo_raw2gml.py $f ${f::-3}gml $2 $1
done

