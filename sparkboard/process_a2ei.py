"""This script serves to process data for the A2EI sensor:
    1) convert dates to time series
    3) replace missing data with zeros
    4) Append new data sets/csvs to this master list
"""
import os
import pandas as pd
import numpy as np

class A2EI:
    """
    class: A2EI
        -Class for the management of functions to modify the .csv corresponding to the A2EI data
    
    Inheritance: None

    Constructors: None
    """
    def __init__(self,path,raw = True):
        if raw:
            self.df = pd.read_csv("../data/A2EI/A2EI.csv")
            self.process()
            data = {}
            data['TIME'] = np.array(self.df['measurementTime'].values)
            data['VOLTAGE'] = self.df['meteredVoltageA']
            data['CURRENT'] = self.df['currentA']
            data['FREQUENCY'] = self.df['frequency']
            data['POWER'] = self.df['meteredPower']
            data['POWER FACTOR'] = self.df['powerFactorA']
            data['ID'] = self.df['account_id']
            self.df = pd.DataFrame(data)
            self.save_to_csv()

        else:
            self.df = pd.read_csv("../data/A2EI/A2EI_processed.csv")

        
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

    def save_to_csv(self, path=None):
        """
        Save the current DataFrame to a CSV file. If no path is provided, it writes the name as processed.

        input: path - Optional string path to save the CSV file. If None, uses default name.
        """
        if path is None:
            path = "../data/A2EI/A2EI_processed.csv"  # Default path to the original file

        self.df.to_csv(path, index=False)

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
