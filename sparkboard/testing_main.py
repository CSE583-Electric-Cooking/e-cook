import os
import unittest
import pandas as pd
import numpy as np
import plotting
from process_survey import *


plotting_path = os.path.abspath(plotting.__file__)
package_root_path = os.path.dirname(plotting_path)
parent_directory = os.path.dirname(package_root_path)
data_directory = os.path.join(parent_directory, 'data')

kosko_directory = os.path.join(data_directory, "Kosko/")
A2EI_directory = os.path.join(data_directory, "A2EI/")
survey_directory = os.path.join(data_directory, "Survey/")

### UNIT TEST FOR SURVEY DATA

df_survey = pd.read_csv(f"{survey_directory}/Consumption Monitoring Survey_modified.csv")

def survey_smoke():
    return #process_survey func

def one_shot_process_name_community():
    """
    test the functionality of community name processing, remove non alphabetical characters,
    replaces under scores with spaces
    """
    string_input = "$queen_ann$@"
    str(string_input)
    return process_name(string_input, mode = "community")

def one_shot_process_name_delinator():
    """
    test the functionality of the code to seperate a "/" from a list for later grouping of data

    mode must be in selected whitelist
    """
    string_input = "appliances/test"
    return process_name(string_input, mode = "appliances/")

def edge_whitelist():
    """
    Make sure a value error is raised if a mode is not in the whitelist
    """
    return process_name(" ", mode = "not in whitelist")

def edge_incorrect_data_type():
    """
    Make sure a value error is raised if a mode is not in the whitelist
    """
    return process_name(1, mode = "community")

def one_shot_column_reduction():
    # First community Kyebando Kisalosalo had 3-females 2-males
    community = df_survey["community_name"].unique()[0]
    data = df_survey[df_survey["community_name"] == community]
    return list(column_reduction(data,"Participant_gender")[-1][0])

def one_shot_column_reduction_n():
    # First community Kyebando Kisalosalo had 3-females 2-males
    community = df_survey["community_name"].unique()[0]
    data = df_survey[df_survey["community_name"] == community]
    vec = np.array(column_reduction_n(data,"appliances/")[-1][0])
    m = vec.shape
    return m[0], int(vec.sum())

def one_shot_remove_sparsity():
    community = df_survey["community_name"].unique()[0]
    data = pd.DataFrame({"community_name": community,"data": np.ones(5),"sparse":np.zeros(5)})
    return remove_sparse_columns(data)

def edge_remove_sparsity():
    community = df_survey["community_name"].unique()[0]
    data = pd.DataFrame({"community_name": community,"data": "a","sparse":np.zeros(5)})
    return remove_sparse_columns(data)

def smoke_test_survey():
    return process_data_survey(path = f"{survey_directory}/Consumption Monitoring Survey_modified.csv"
                               , write_csv = False)

def test_final_dim():
    df = process_data_survey(path = f"{survey_directory}/Consumption Monitoring Survey_modified.csv"
                             , write_csv = False)
    dim = len(df)
    return dim

class SurveyProcessing(unittest.TestCase):
    """
    Performs unit testing for survey processing

    Inheritance: unittest.TestCase

    Constructors: None

    """
    def test_smoke_survey(self):
        _ = smoke_test_survey()
        
    def test_one_shot_community(self):
        """Test one shot for community name processing
           
        Args: None

        Returns: None

        """
        self.assertEqual(one_shot_process_name_community(), "Queen Ann")

    def test_one_shot_deliniator(self):
        """Test one shot for splitting data
           
        Args: None

        Returns: None

        """
        self.assertEqual(one_shot_process_name_delinator(), "test")

    def test_edge_whitelist(self):
        """Test edge to trigger if not in user defined whitelist
                   
        Args: None

        Returns: None

        """
        with self.assertRaises(ValueError):
            edge_whitelist()

    def test_edge_incorrect_data_type(self):
        """Test edge to trigger if data type not in string format
                   
        Args: None

        Returns: None

        """
        with self.assertRaises(ValueError):
            edge_incorrect_data_type()

    def test_one_shot_column_reduction(self):
        """Test to make sure the column finds the right count
           
        Args: None

        Returns: None

        """
        self.assertEqual(one_shot_column_reduction(), ['3','2'])

    def test_one_shot_column_reduction_n(self):
        """Test to make sure the column space finds the right shape, count
           
        Args: None

        Returns: None

        """
        community = df_survey["community_name"].unique()[0]
        data = df_survey[df_survey["community_name"] == community]
        query_columns = []
        for c in data.columns:
            if "appliances/" in c:
                query_columns.append(c)
        count = np.count_nonzero(data[query_columns].values)
        _,m = data[query_columns].values.shape
        self.assertEqual(one_shot_column_reduction_n(), (m,count))

    def test_one_shot_remove_sparsity(self):
        community = df_survey["community_name"].unique()[0]
        data = pd.DataFrame({"community_name": community,"data": np.ones(5)})
        self.assertEqual(one_shot_remove_sparsity().values.all(), data.values.all())

    def test_final_dim(self):
        self.assertEqual(test_final_dim(), len(df_survey["community_name"].unique()))



    

if __name__ == "__main__":
    unittest.main()
    #print(smoke_test_survey())



