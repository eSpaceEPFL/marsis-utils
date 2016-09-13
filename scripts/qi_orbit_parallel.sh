#!/bin/bash
# $1 -> xml_data_model
# $2 -> track qi file
# $.. -> file list

parallel --gnu qi_orbit.sh ::: $1 ::: $2 ::: ${@: 3}

