# -*- coding: utf-8 -*-

############################################################

#    A simple script to read the values in CElegansNeuronTables.xls.

#    Note: this file will be replaced with a call to PyOpenWorm
#    when that package is updated to read all of this data from the 
#    spreadseet

############################################################


from NeuroMLUtilities import ConnectionInfo

from xlrd import open_workbook
import os

spreadsheet_location = os.path.dirname(os.path.abspath(__file__))+"/../../../"

def readDataFromSpreadsheet(include_nonconnected_cells=False):

    conns = []
    cells = []
    filename = "%sherm_full_edgelist.xls"%spreadsheet_location
    rb = open_workbook(filename)

    print "Opened Excel file: " + filename

    known_nonconnected_cells = ['CANL', 'CANR', 'VC6']


    for row in range(1,rb.sheet_by_index(0).nrows):
        pre = str.strip(str(rb.sheet_by_index(0).cell(row,0).value))
        post = str.strip(str(rb.sheet_by_index(0).cell(row,1).value))
        num = int(rb.sheet_by_index(0).cell(row, 2).value)
        syntype = rb.sheet_by_index(0).cell(row,3).value
        synclass = 'Generic_GJ' if 'electrical' in syntype else 'Chemical_Synapse'
        #print "%s-%s %s %s %s"%(pre,post,num,syntype,synclass)

        conns.append(ConnectionInfo(pre, post, num, syntype, synclass))
        if pre not in cells:
            cells.append(pre)
        if post not in cells:
            cells.append(post)

    if include_nonconnected_cells:
        for c in known_nonconnected_cells: cells.append(c)

    return cells, conns