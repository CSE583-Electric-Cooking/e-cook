"""This script serves to process data for the A2EI sensor:
    1) convert dates to time series
    3) replace missing data with zeros
    4) Append new data sets/csvs to this master list
"""
import os
import pandas as pd
import numpy as np
import sparkboard.plotting
## Navigate to Kosko
plotting_path = os.path.abspath(sparkboard.plotting.__file__)
package_root_path = os.path.dirname(plotting_path)
parent_directory = os.path.dirname(package_root_path)
ecook = os.path.dirname(parent_directory)
data_directory = os.path.join(ecook, 'data/A2EI')


class A2EI:
    """
    class: A2EI
        -Class for the management of functions to modify the .csv corresponding to the A2EI data
    
    Inheritance: None

    Constructors: None
    """
    def __init__(self,write_csv = False):
        self.df = pd.read_csv(f"{data_directory}/A2EI.csv")
        self.process()
        data = {}
        data['TIME'] = self.df['measurementTime'].values
        data['VOLTAGE'] = self.df['meteredVoltageA'].values.astype(float)
        data['CURRENT'] = self.df['currentA'].values.astype(float)
        data['FREQUENCY'] = self.df['frequency'].values.astype(float)
        data['POWER'] = self.df['meteredPower'].values.astype(float)
        data['POWER FACTOR'] = self.df['powerFactorA'].values.astype(float)
        data['ID'] = self.df['account_id'].values.astype(int)
        self.df = pd.DataFrame(data)
        if write_csv:
            self.df.to_csv(f"{data_directory}/A2EI_processed.csv", index=False)

    def convert_date_time(self):
        """
        convert string values to datatime object
        """
        def reformat(data_string):
            """
            reformat - Local helper function to replace strings with format ready for conversion.
            Handles various formats of date-time strings using base Python string methods.
            """
            if isinstance(data_string, str):
                # Replace 'T' with a space
                data_string = data_string.replace("T", " ")

                if '.' in data_string: # Extract data after "."
                    data_string = data_string[:data_string.index('.')]

                return data_string
            else:
                # Return the original value if it's not a string
                return data_string
        self.df['measurementTime'] = self.df['measurementTime'].apply(reformat)
        self.df['sourceCreatedAt'] = self.df['sourceCreatedAt'].apply(reformat)
        self.df['createdOn'] = self.df['createdOn'].apply(reformat)

    def pad_zeros(self):
        """
        pad NaN with zeros

        input: self reference to dataframe
        """
        self.df = self.df.fillna(0)
    
    def process(self):
        """
        runs processing functions

        input: self reference to dataframe
        """
        self.convert_date_time()
        self.pad_zeros()

    def append_csv(self, path):
        """
        Append data from a new CSV file to the existing DataFrame.

        input: path - String path to the new CSV file
        """
        new_df = pd.read_csv(path)

        # Check if columns match
        if not new_df.columns.equals(self.df.columns):
            raise ValueError("Improper Columns: cannot concatenate")

        # Concatenate DataFrames vertically
        self.df = pd.concat([self.df, new_df], axis=0, ignore_index=True)
        # Rerun the processing procedure
        self.process()
