#!/bin/bash
# $1 -> xml_data_model
# $2 -> xsl_tranform_model
# $.. -> file list

parallel --gnu geo_raw2gml.sh ::: $1 ::: $2 ::: ${@: 3}

