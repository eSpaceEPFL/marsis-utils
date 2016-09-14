#!/bin/bash
# $1 -> xml_data_model
# $2 -> track qi file
# $.. -> file list

for f in ${@: 3}
do
    snr_orbit.py $f $1 $2
done

