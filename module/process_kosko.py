"""This script serves to process data for the Kosko sensor:
    1) convert dates to time series
    2) appends multiple CSV files into a master list

    Class can later be used for importing into main functinality as a tool to easiliy access processed data
"""

import os
import pandas as pd
import numpy as np

class Kosko:

    def __init__(self):
        os.chdir("../Data/Kosko")
        kosko_data = sorted(os.listdir())
        if not "Kosko_processed.csv" in kosko_data:
            ids = []
            data = []
            for kd in kosko_data:
                if ".csv" in kd and "EM" in kd: #exclude non compliant files
                    id = kd.split("_")[1]
                    ids.append(id)
                    data.append(pd.read_csv(kd))

            for d,id in zip(data, ids):
                d["ID"] = id


            self.df = pd.concat(data, axis=0, ignore_index=True)
            self.df['TIME'] = self.df['TIME'].apply(lambda x: '20' + x)
            self.df['TIME'] = pd.to_datetime(self.df['TIME'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
            self.df['TIME'] = np.array(self.df['TIME'])
            self.df = self.df.sort_values(by=['ID', 'TIME'])

            self.df.to_csv("Kosko_processed.csv", index=False)
        else:
            self.df = pd.read_csv("Kosko_processed.csv")

        
        os.chdir("../../module")


