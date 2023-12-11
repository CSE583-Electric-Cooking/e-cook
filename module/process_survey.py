import pandas as pd 
import numpy as np

def process_name(string_in, mode):
    """
    Reformating community names in csv such that they match the dashboard

    #TESTING
        -String_in incorrect datatype 
    """
    try:
        string_in = str(string_in)
    except ValueError:
        raise ValueError("Incorrect data type for name processing")
    
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

    if mode in ["electricity_payment_to/","appliances/"]:
        string_in = string_in.split("/")[-1]

    return string_in

def column_reduction(df, column):
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
    ADD TEST DATA MUST BE NONNUMERIC
    """
    columns = list(df.columns)
    columns.remove("community_name")
    try:
        data = df[columns].sum(axis = 0)
    except ValueError:
        raise ValueError("Data must be numerical")
    dout = ["community_name"]
    
    for c,d in zip(columns,data):
        if d != 0:
            dout.append(c)
    dout = df[dout]
    return dout

if __name__ == "__main__":
    df = pd.read_csv("../data/Survey/Consumption Monitoring Survey_modified.csv")
    df_out = pd.DataFrame({})

    df["community_name"] = df["community_name"].astype(str)
    for name in df["community_name"].unique():
        df.loc[df["community_name"] == name, "community_name"] = process_name(name,"community")

    df_out["community_name"] = df["community_name"].unique()

    
    columns_to_reduce = ["Participant_gender","Sensor_Type","connection_modality","rent_own"]
    columns_n_to_reduce = ["electricity_payment_to/","appliances/"]

    for column in columns_to_reduce:
        names, data = column_reduction(df,column)
        df_out[names] = data

    for column in columns_n_to_reduce:
        names, data = column_reduction_n(df,column)
        df_out[names] = data

    df_out = remove_sparse_columns(df_out)
    df_out.to_csv("../data/Survey/survey_app_data.csv")
    
   

