"""
This script is utilized for the truncation of the large survey results
into a more compact form for analysis in the dashboard application
"""
import pandas as pd
import numpy as np

def process_name(string_in, mode):
    """
    Reformats community names in a CSV file to match a specific dashboard format.

    Parameters:
    string_in (str): The input string representing a community name.
    mode (str): The mode specifying the type of formatting to apply. 
                Accepted values are 'community', 'electricity_payment_to/', and 'appliances/'.

    Returns:
    str: The reformatted community name.

    Raises:
    ValueError: If the input is not a string or the mode is not in the accepted list.
    """
    if not isinstance(string_in,str):
        raise ValueError("Incorrect data input type, recast as string")

    white_list = ["community"]
    column_list = ["electricity_payment_to/","appliances/"]
    white_list.extend(column_list)
    if mode not in white_list:
        raise ValueError("Incorrect mode type")

    if mode == "community":
        if not string_in.isalpha():
            string_in = string_in.replace("_"," ")
            clean = [char for char in string_in if char.isalpha() or char.isspace() ]
            string_in = "".join(clean)

        words = string_in.split(" ")
        for word in words:
            string_in = string_in.replace(word.lower(),word.capitalize())

        if string_in[-1] == " ":
            string_in = string_in[:len(string_in)-1]
        return string_in

    if mode in ["electricity_payment_to/","appliances/"]:
        string_in = string_in.split("/")[-1]
        return string_in

def column_reduction(df, column):
    """
    Counts unique entries in a specified column of a DataFrame and returns 
    their occurrence in each community.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the data.
    column (str): The column name to analyze.

    Returns:
    tuple: A tuple containing:
           - A list of unique entries in the specified column.
           - A numpy array with counts of each unique entry per community.
    """
    entries = df[column].unique()
    entries = [e for e in entries if str(e) != "nan"]
    out = []
    for community in df["community_name"].unique():
        community_df = df[df["community_name"] == community]
        data = np.zeros_like(entries)
        for e, i in zip(entries,range(len(data))):
            data[i] = int((community_df[column] == e).sum())
        out.append(data)
    return entries, np.array(out)

def column_reduction_n(df,mode):
    """
    Aggregates data in columns containing a specific substring and sums values for each community.

    Parameters:
    df (pd.DataFrame): The DataFrame to process.
    mode (str): The substring to identify relevant columns.

    Returns:
    tuple: A tuple containing:
           - A list of processed column names.
           - A numpy array with aggregated sums for each community
    """
    columns = df.columns
    types = []
    sum_list = []
    for c in columns:
        if mode in c:
            types.append(c)

    for community in df["community_name"].unique():
        community_df = df[df["community_name"] == community].fillna(0)
        sum_list.append(community_df[types].sum(axis = 0).values)
    return [process_name(c, mode = mode) for c in types], np.array(sum_list)

def remove_sparse_columns(df):
    """
    Removes columns from a DataFrame where the sum of values is zero.

    Parameters:
    df (pd.DataFrame): The DataFrame to process.

    Returns:
    pd.DataFrame: A DataFrame with sparse columns removed.
    """
    columns = list(df.columns)
    columns.remove("community_name")
    data = df[columns].sum(axis = 0)
    dout = ["community_name"]

    for c,d in zip(columns,data):
        if d != 0:
            dout.append(c)
    dout = df[dout]
    return dout

def process_data_survey(path = None, write_csv = True):
    """
    Processes survey data, reformats community names, reduces data in specified columns, 
    and writes the output to a CSV file.

    Parameters:
    path (str, optional): The file path to the survey data. If None, a default path is used.
    write_csv (bool): Flag to determine whether to write the processed data to a CSV file.

    Returns:
    pd.DataFrame: The processed DataFrame.
    """
    if path is None:
        df = pd.read_csv("../data/Survey/Consumption Monitoring Survey_modified.csv")
    else:
        df = pd.read_csv(path)
    df_out = pd.DataFrame({})

    df["community_name"] = df["community_name"].astype(str)
    for name in df["community_name"].unique():
        df.loc[df["community_name"] == name, "community_name"] = process_name(name,"community")

    df_out["community_name"] = df["community_name"].unique()

    columns_to_reduce = ["Participant_gender","Sensor_Type","connection_modality","rent_own"]
    columns_n_to_reduce = ["electricity_payment_to/","appliances/"]

    for column in columns_to_reduce:
        names, data = column_reduction(df,column)
        if "modality" in column:
            names = [f"modality/{name}" for name in names]
        elif "gender" in column:
            names = [f"gender/{name}" for name in names]
        elif "rent" in column:
            names = [f"ownership/{name}" for name in names]
        elif "Sensor" in column:
            names = [f"sensor/{name}" for name in names]
        df_out[names] = data

    for column in columns_n_to_reduce:
        names, data = column_reduction_n(df,column)
        if "appliances" in column:
            names = [f"appliance/{name}" for name in names]
        elif "payment" in column:
            names = [f"payment/{name}" for name in names]
        df_out[names] = data

    df_out = remove_sparse_columns(df_out)
    if write_csv:
        if path is None:
            df_out.to_csv("../data/Survey/survey_app_data.csv", index=False)
        else:
            df_out.to_csv(f"{path}/survey_app_data.csv", index=False)

    return df_out
