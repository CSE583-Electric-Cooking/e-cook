"""
This module is used to organize deaggragate and query data.
"""
import pandas as pd

import matplotlib.pyplot as plt

def deaggregate(kosko_data):
    """
    Deaggregates Kosko data into a dictionary of Pandas DataFrames.
    Parameters:
    - kosko_data (list): A list of file names containing Kosko data.
    Returns:
    - dict: A dictionary where keys are user IDs and values are corresponding Pandas DataFrames.
    """
    user_dict = {}
    for data in kosko_data:
        id = data.split("_")[1]
        user_dict[id] = pd.read_csv(data)
    return user_dict

# Example Test:
# data_files = ["user_1_data.csv", "user_2_data.csv"]
# user_data = deaggregate(data_files)
# print(user_data["1"])  # Assuming "1" is a valid user ID

def query(dictionary):
    """
    Displays basic visualization information for Kosko data.
    Parameters:
    - dictionary (dict): A dictionary where keys are user IDs and values are Pandas DataFrames.
    Returns:
    - None
    """
    print("BASIC VISUALIZATION KOSKO\n")
    print("AVAILABLE DATA:")
    print_user = lambda id: print(f"USER ID: {id}")
    ids = []
    for item in dictionary.items():
        ids.append(item[0])
        print_user(item[0])

# Example Test:
# query(user_data)  # Assuming user_data is a valid dictionary from deaggregate function
