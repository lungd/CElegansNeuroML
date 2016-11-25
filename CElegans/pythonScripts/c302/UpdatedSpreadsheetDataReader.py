# -*- coding: utf-8 -*-

############################################################

#    A simple script to read the values in herm_full_edgelist.csv.

#    Note: this file will be replaced with a call to PyOpenWorm
#    when that package is updated to read all of this data from the 
#    spreadseet

############################################################

import csv

from NeuroMLUtilities import ConnectionInfo
import os

spreadsheet_location = os.path.dirname(os.path.abspath(__file__))+"/../../../"

def readDataFromSpreadsheet(include_nonconnected_cells=False):

    conns = []
    cells = []
    filename = "%sherm_full_edgelist.csv" % spreadsheet_location
    
    with open(filename, 'rb') as f:
        reader = csv.DictReader(f)
        print "Opened file: " + filename

        known_nonconnected_cells = ['CANL', 'CANR', 'VC6']

        for row in reader:
            pre = str.strip(row["Source"])
            post = str.strip(row["Target"])
            num = int(row["Weight"])
            syntype = str.strip(row["Type"])
            synclass = 'Generic_GJ' if 'electrical' in syntype else 'Chemical_Synapse'

            conns.append(ConnectionInfo(pre, post, num, syntype, synclass))
            if pre not in cells:
                cells.append(pre)
            if post not in cells:
                cells.append(post)

        if include_nonconnected_cells:
            for c in known_nonconnected_cells: cells.append(c)

    return cells, conns
