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

spreadsheet_location = os.path.dirname(os.path.abspath(__file__)) + "/../../../"
filename = "%sherm_full_edgelist.csv" % spreadsheet_location


def is_muscle_cell(cell):
    known_muscle_prefixes = ["pm", "vm", "um", "dBWM", "vBWM"]
    return cell.startswith(tuple(known_muscle_prefixes))

def is_body_wall_muscle(cell):
    known_muscle_prefixes = ["dBWM", "vBWM"]
    return cell.startswith(tuple(known_muscle_prefixes))

def is_neuron(cell):
    return cell[0].isupper()

# TODO: Check if this is necessary.
def remove_leading_zero(cell):
    """
    Returns neuron name with an index without leading zero. E.g. VB01 -> VB1.
    """
    if is_neuron(cell) and cell[-2:].startswith("0"):
        return "%s%s" % (cell[:-2], cell[-1:])
    return cell


def readDataFromSpreadsheet(include_nonconnected_cells=False):
    """
    Args:
        include_nonconnected_cells (bool): Also append neurons without known connections to other neurons to the 'cells' list. True if they should get appended, False otherwise.
    Returns:
        cells (:obj:`list` of :obj:`str`): List of neurons
        conns (:obj:`list` of :obj:`ConnectionInfo`): List of connections from neuron to neuron
    """

    conns = []
    cells = []

    with open(filename, 'rb') as f:
        reader = csv.DictReader(f)
        print "Opened file: " + filename

        known_nonconnected_cells = ['CANL', 'CANR']

        for row in reader:
            pre = str.strip(row["Source"])
            post = str.strip(row["Target"])
            num = int(row["Weight"])
            syntype = str.strip(row["Type"])
            synclass = 'Generic_GJ' if 'electrical' in syntype else 'Chemical_Synapse'

            if not is_neuron(pre) or not is_neuron(post):
                continue # pre or post is not a neuron

            pre = remove_leading_zero(pre)
            post = remove_leading_zero(post)

            conns.append(ConnectionInfo(pre, post, num, syntype, synclass))
            if pre not in cells:
                cells.append(pre)
            if post not in cells:
                cells.append(post)

        if include_nonconnected_cells:
            for c in known_nonconnected_cells:
                if c not in cells:
                    cells.append(c)

    return cells, conns


def readMuscleDataFromSpreadsheet(include_muscle_to_muscle_conns=False):
    """
    Args:
        include_muscle_to_muscle_conns (bool): Also append muscle to muscle connections to the 'conns' list. True if they should get appended, False otherwise.
    Returns:
        neurons (:obj:`list` of :obj:`str`): List of motor neurons. Each neuron has at least one connection with a post-synaptic muscle cell
        muscles (:obj:`list` of :obj:`str`): List of muscle cells.
        conns (:obj:`list` of :obj:`ConnectionInfo`): List of connections with/without
    """

    neurons = []
    muscles = []
    conns = []

    with open(filename, 'rb') as f:
        reader = csv.DictReader(f)
        print "Opened file: " + filename

        for row in reader:
            pre = str.strip(row["Source"])
            post = str.strip(row["Target"])
            num = int(row["Weight"])
            syntype = str.strip(row["Type"])
            synclass = 'Generic_GJ' if 'electrical' in syntype else 'Chemical_Synapse'

            if not is_muscle_cell(post):
                # Don't add connections unless post=muscle
                continue
            if is_muscle_cell(pre) and not include_muscle_to_muscle_conns:
                # Don't add muscle-muscle connections unless include_muscle_to_muscle_conns=True
                continue
            if not is_muscle_cell(pre) and not is_neuron(pre):
                # Don't add otherCell-muscle connections, e.g. mc2dr-muscle
                continue

            pre = remove_leading_zero(pre)

            conns.append(ConnectionInfo(pre, post, num, syntype, synclass))
            #print "NEWSpreadsheedDataReader >> %s-%s %s" % (pre, post, synclass)
            if pre not in neurons and is_neuron(pre):
                neurons.append(pre)
            if post not in muscles:
                muscles.append(post)

    return neurons, muscles, conns


def main():
    cells, conns = readDataFromSpreadsheet()

    print("%i cells in spreadsheet: %s\n" % (len(cells), sorted(cells)))

    from os import listdir
    cell_names = [f[:-9] for f in listdir('%s/CElegans/morphologies/' % spreadsheet_location) if
                  f.endswith('.java.xml')]

    cell_names.remove('MDL08')  # muscle

    print("%i cell morphologies found: %s\n" % (len(cell_names), sorted(cell_names)))

    for c in cells:
        cell_names.remove(c)

    print("Difference: %s" % cell_names)

    cells2, conns2 = readDataFromSpreadsheet(include_nonconnected_cells=True)

    assert (len(cells2) == 302)

    print("Lengths are equal if include_nonconnected_cells=True\n")

    neurons, muscles, conns = readMuscleDataFromSpreadsheet()

    print("Found %i neurons connected to muscles: %s\n" % (len(neurons), sorted(neurons)))
    print("Found %i muscles connected to neurons: %s\n" % (len(muscles), sorted(muscles)))
    print("Found %i connections between neurons and muscles, e.g. %s" % (len(conns), conns[0]))


    neurons, muscles, conns = readMuscleDataFromSpreadsheet(include_muscle_to_muscle_conns=True)
    print("Found %i connections between neurons and muscles or between muscles and muscles" % len(conns))


if __name__ == '__main__':
    main()
