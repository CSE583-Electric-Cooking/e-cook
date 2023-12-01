"""
This module has a function to extract .csv files from another repository named data.
"""
# It's only extracting kosko data
# Need revise function to pull any data... Something like
# def extract_data("data name")
import os

def extract_data():
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
