#!/bin/bash
# $1 -> xml data model
# $.. -> file list

parallel --gnu marsis_labels.py ::: $1 ::: ${@: 2}
