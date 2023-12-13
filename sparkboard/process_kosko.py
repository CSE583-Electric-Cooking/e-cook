"""
This script serves to process data for the Kosko sensor:
    1) convert dates to time series
    2) appends multiple CSV files into a master list
Class can later be used to import into main functinality as a tool to easiliy access processed data
"""
import os
import pandas as pd
import numpy as np
import plotting


## Navigate to Kosko
plotting_path = os.path.abspath(plotting.__file__)
package_root_path = os.path.dirname(plotting_path)
parent_directory = os.path.dirname(package_root_path)
data_directory = os.path.join(parent_directory, 'data/Kosko')


class Kosko:
    """
    This class processes data for the Kosko sensor:
    1) Converts dates to time series.
    2) Appends multiple CSV files into a master list.
    The class can later be used for importing into the main functionality
    as a tool to easily access processed data.
    Attributes:
    - df (pd.DataFrame): Processed data stored in a Pandas DataFrame.
    Note:
    - The processed data is stored in the 'df' attribute.
    Example:
    kosko_instance = Kosko()
    processed_data = kosko_instance.df
    """
    def __init__(self,write_csv = False):
        """
        Initializes the Kosko class. If 'Kosko_processed.csv' does not
        exist, it reads and processes CSV files from the '../data/Kosko' directory
        and creates a master DataFrame. If the file already exists, it reads the
        preprocessed data.
        """
        kosko_data = sorted(os.listdir(data_directory))

        ids = []
        data = []
        for kd in kosko_data:
            if ".csv" in kd and "EM" in kd: #exclude non compliant files
                id = kd.split("_")[1]
                ids.append(id)
                data.append(pd.read_csv(f"{data_directory}/{kd}"))
        for d,id in zip(data, ids):
            d["ID"] = str(id)

        self.df = pd.concat(data, axis=0, ignore_index=True)
        self.process()

        if write_csv:
            self.df.to_csv("Kosko_processed.csv", index=False)

    def process(self):
        """
        1. Convert date and time columns in the DataFrame.
        2. Sort the DataFrame.
        3. Filter the DataFrame based on the year.
        """
        self.convert_date_time()
        self.sort()
        self.filter_year()

    def convert_date_time(self):
        """
        1. Adds '20' to the beginning of each entry in the 'TIME' column.
        2. Converts the 'TIME' column to datetime using the specified format '%Y-%m-%d %H:%M:%S'.
        4. Converts the resulting datetime objects to a NumPy array.
        """
        self.df['TIME'] = self.df['TIME'].apply(lambda x: '20' + x)
        self.df['TIME'] = pd.to_datetime(self.df['TIME'],
                                         format='%Y-%m-%d %H:%M:%S',
                                         errors='coerce')
        self.df['TIME'] = np.array(self.df['TIME'])

    def sort(self):
        """
        Sort the DataFrame based on the 'ID' and 'TIME' columns.
        """
        self.df = self.df.sort_values(by=['ID', 'TIME'])

    def filter_year(self,year = 2022):
        """
        Filter the DataFrame to exclude entries from a specified year.
        """
        self.df = self.df[self.df['TIME'].dt.year != year]

    def save_to_csv(self):
        """
        Save the dataframe to a csv file
        """
