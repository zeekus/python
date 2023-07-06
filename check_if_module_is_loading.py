#!/usr/bin/env python3

import importlib

try:
    arcpy = importlib.import_module('arcpy')
    print("arcpy module is loaded")
except ImportError:
    print("arcpy module is not loaded")
