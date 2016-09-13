#!/bin/bash
# $1 -> xml_data_model
# $2 -> xsl_tranform_model
# $.. -> file list

parallel --gnu raw_snr2gml.sh ::: $1 ::: $2 ::: ${@: 3}
