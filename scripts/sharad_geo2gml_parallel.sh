#!/bin/bash
# $1 -> xsl_tranform_model
# $.. -> file list

parallel --gnu sharad_geo2gml.sh ::: $1 ::: ${@: 2}
