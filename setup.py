# -*- coding: utf-8 -*-
# Copyright (C) 2015 - EPFL - eSpace
#
# Author: Federico Cantini <federico.cantini@epfl.ch>
#
# Mantainer: Federico Cantini <federico.cantini@epfl.ch>

from distutils.core import setup

setup(
      name = "pyMarsisUtils",
      version = "0.1",
      url = "", #TODO: add a url
      description = "Utilities to manage MARSIS data",
      author = "Federico Cantini",
      author_email = "federico.cantini@epfl.ch",
      maintainer = "Federico Cantini",
      maintainer_email = "federico.cantini@epfl.ch",
      license = "",
      packages = ["marsis_data_IO",
                  "marsis_utils"
                  ],
      package_dir = { "MarsisUtils" : "MarsisUtils"},
#      package_data={"py_marsis_utils": ['data/*']},
      scripts = ["scripts/raw_qi2gml.py",
                 "scripts/raw_qi2gml.sh",
                 "scripts/raw_qi2gml_parallel.sh",
                 "scripts/raw_snr2gml.py",
                 "scripts/raw_snr2gml.sh",
                 "scripts/raw_snr2gml_parallel.sh",
                 "scripts/data2gml.py",
                 "scripts/data2gml.sh",
                 "scripts/data2gml_parallel.sh",
                 "scripts/geo_raw2gml.py",
                 "scripts/geo_raw2gml.sh",
                 "scripts/geo_raw2gml_parallel.sh",
                 "scripts/qi_orbit.py",
                 "scripts/qi_orbit.sh",
                 "scripts/qi_orbit_parallel.sh",
                 "scripts/sharad_geo2gml.py",
                 "scripts/sharad_geo2gml.sh",
                 "scripts/sharad_geo2gml_parallel.sh",
                 "scripts/marsis_labels.py",
                 "scripts/marsis_browse_labels.py",
                 "scripts/marsis_labels_parallel.sh"
                 ],
#      requires = ["",
#                  ], #TODO: add dependencies here
#      data_files = [("", "")],
     )
