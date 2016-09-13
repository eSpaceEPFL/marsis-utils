#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2015 - EPFL - eSpace
#
# Author: Federico Cantini <federico.cantini@epfl.ch>
#
# Mantainer: Federico Cantini <federico.cantini@epfl.ch>

import cgi
import cgitb
cgitb.enable()
import requests



form = cgi.FieldStorage()

#print "test"
#print form
#print
string = "?"
for field in form.keys():
	string=string+field+"="+form[field].value+"&"



r = requests.get("http://localhost/cgi-bin/marsissnr/qgis_mapserv.fcgi"+string)
#for header in r.headers:
#	print header+": "+r.headers[header]
print "Content-type: text/xml"
print

if r.content.find("<?xml",0,5) == -1:
	print "<?xml version='1.0' encoding=\"ISO-8859-1\" ?>"
print r.content
