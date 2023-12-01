"""
This module has a function to extract .csv files from another repository named data.
"""
# It's only extracting kosko data
# Not sure if it extracts A2EI
import os

def kosko():
    """
    This function extracts kosko data from the /data/kosko repository.
    It interacts with other functions in different modules to be sorted
    for analysis.
    """
    os.chdir(('../data/kosko'))
    files = os.listdir()
    kosko_data = []
    for file in files:
        if ".csv" in file:
            kosko_data.append(file)
    # Sorts list of .csv data
    kosko_data = sorted(kosko_data)
    # add test pulls only .csv data
    return kosko_data

def a2ei():
    """
    This function extracts kosko data from the /data/A2EI repository.
    It interacts with other functions in different modules to be sorted
    for analysis.
    """
    os.chdir(('../data/A2EI'))
    files = os.listdir()
    a2ei_data = []
    for file in files:
        if ".csv" in file:
            a2ei_data.append(file)
    # Sorts list of .csv data
    a2ei_data = sorted(a2ei_data)
    # add test pulls only .csv data
    return a2ei_data
