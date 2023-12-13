import os
import unittest
import pandas as pd
import numpy as np
from PIL import Image, ImageOps
import plotting
from plotting import PlotSurvey, PlotTimeSeries
from process_survey import *
from process_kosko import Kosko
from process_a2ei import A2EI

plotting_path = os.path.abspath(plotting.__file__)
package_root_path = os.path.dirname(plotting_path)
parent_directory = os.path.dirname(package_root_path)
data_directory = os.path.join(parent_directory, 'data')

kosko_directory = os.path.join(data_directory, "Kosko/")
A2EI_directory = os.path.join(data_directory, "A2EI/")
survey_directory = os.path.join(data_directory, "Survey/")

### Helper Functions

def image_similarity(path1,path2):
    im1 = ImageOps.grayscale(Image.open(path1))
    im2 = ImageOps.grayscale(Image.open(path2))
    im1 = np.asarray(im1).flatten()
    im2 = np.asarray(im2).flatten()
    norm = np.linalg.norm(im1-im2)
    return norm

df_survey = pd.read_csv(f"{survey_directory}/Consumption Monitoring Survey_modified.csv")
df_survey_processed = pd.read_csv(f"{survey_directory}/survey_app_data.csv")
df_kosko = pd.read_csv(f"{kosko_directory}/Kosko_processed.csv")
df_a2ei = pd.read_csv(f"{A2EI_directory}/A2EI_processed.csv")

def survey_smoke():
    return process_data_survey(write_csv = False)

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

def one_shot_final_dim():
    df = process_data_survey(write_csv = False)
    dim = len(df)
    return dim

def smoke_kosko():
    return Kosko(write_csv = False)

def one_shot_kosko_output():
    kosko = Kosko(write_csv=False)
    columns = kosko.df.columns
    return list(columns),len(columns)

def one_shot_kosko_output_data_types():
    kosko = Kosko(write_csv=False)
    query = kosko.df.values[0]
    return query

def smoke_A2EI():
    return A2EI(write_csv = False)

def one_shot_A2EI_output():
    a2ei = A2EI(write_csv=False)
    columns = a2ei.df.columns
    return list(columns),len(columns)

def one_shot_A2EI_output_data_types():
    a2ei = A2EI(write_csv=False)
    query = a2ei.df.values[0]
    return query

def smoke_time_series_kosko_onoff():
    dff = df_kosko[df_kosko['ID'] == df_kosko["ID"][0]]
    columns_to_exclude = ["ID", "TIME", "DEVICE STATUS"]
    kosko_status = "ONOFF"
    columns = [col for col in dff.columns if col not in columns_to_exclude]
    subplot = PlotTimeSeries(dff,columns,"kosko",kosko_status)
    fig = subplot.dash_plot()
    return fig

def smoke_time_series_kosko_on():
    dff = df_kosko[df_kosko['ID'] == df_kosko["ID"][0]]
    columns_to_exclude = ["ID", "TIME", "DEVICE STATUS"]
    kosko_status = "ON"
    dff = dff[dff["DEVICE STATUS"] == kosko_status]
    columns = [col for col in dff.columns if col not in columns_to_exclude]
    subplot = PlotTimeSeries(dff,columns,"kosko",kosko_status)
    fig = subplot.dash_plot()
    return fig

def smoke_time_series_kosko_off():
    dff = df_kosko[df_kosko['ID'] == df_kosko["ID"][0]]
    columns_to_exclude = ["ID", "TIME", "DEVICE STATUS"]
    kosko_status = "OFF"
    dff = dff[dff["DEVICE STATUS"] == kosko_status]
    columns = [col for col in dff.columns if col not in columns_to_exclude]
    subplot = PlotTimeSeries(dff,columns,"kosko",kosko_status)
    fig = subplot.dash_plot()
    return fig

def one_shot_kosko_time_series_plotting_nominal_onoff():
    dff = df_kosko[df_kosko['ID'] == df_kosko["ID"][0]]
    columns_to_exclude = ["ID", "TIME", "DEVICE STATUS"]
    kosko_status = "ONOFF"
    columns = [col for col in dff.columns if col not in columns_to_exclude]
    subplot = PlotTimeSeries(dff,columns,"kosko",kosko_status)
    fig = subplot.dash_plot()
    fig.write_image(f"{package_root_path}/images/test_{df_kosko["ID"][0]}_{kosko_status}.png")
    path1 = f"{package_root_path}/images/test_{df_kosko["ID"][0]}_{kosko_status}.png"
    path2 = f"{package_root_path}/images/kosko_{df_kosko["ID"][0]}_{kosko_status}.png"
    return image_similarity(path1,path2)

def one_shot_kosko_time_series_plotting_nominal_on():
    dff = df_kosko[df_kosko['ID'] == df_kosko["ID"][0]]
    columns_to_exclude = ["ID", "TIME", "DEVICE STATUS"]
    kosko_status = "ON"
    dff = dff[dff["DEVICE STATUS"] == kosko_status]
    columns = [col for col in dff.columns if col not in columns_to_exclude]
    subplot = PlotTimeSeries(dff,columns,"kosko",kosko_status)
    fig = subplot.dash_plot()
    fig.write_image(f"{package_root_path}/images/test_{df_kosko["ID"][0]}_{kosko_status}.png")
    path1 = f"{package_root_path}/images/test_{df_kosko["ID"][0]}_{kosko_status}.png"
    path2 = f"{package_root_path}/images/kosko_{df_kosko["ID"][0]}_{kosko_status}.png"
    return image_similarity(path1,path2)

def one_shot_kosko_time_series_plotting_nominal_off():
    dff = df_kosko[df_kosko['ID'] == df_kosko["ID"][0]]
    columns_to_exclude = ["ID", "TIME", "DEVICE STATUS"]
    kosko_status = "OFF"
    dff = dff[dff["DEVICE STATUS"] == kosko_status]
    columns = [col for col in dff.columns if col not in columns_to_exclude]
    subplot = PlotTimeSeries(dff,columns,"kosko",kosko_status)
    fig = subplot.dash_plot()
    fig.write_image(f"{package_root_path}/images/test_{df_kosko["ID"][0]}_{kosko_status}.png")
    path1 = f"{package_root_path}/images/test_{df_kosko["ID"][0]}_{kosko_status}.png"
    path2 = f"{package_root_path}/images/kosko_{df_kosko["ID"][0]}_{kosko_status}.png"
    return image_similarity(path1,path2)

def one_shot_kosko_time_series_plotting_abnormal_onoff():
    ID = df_kosko["ID"].unique()[1]
    dff = df_kosko[df_kosko['ID'] == ID]
    columns_to_exclude = ["ID", "TIME", "DEVICE STATUS"]
    kosko_status = "ONOFF"
    columns = [col for col in dff.columns if col not in columns_to_exclude]
    subplot = PlotTimeSeries(dff,columns,"kosko",kosko_status)
    fig = subplot.dash_plot()
    fig.write_image(f"{package_root_path}/images/test_{ID}_{kosko_status}.png")
    path1 = f"{package_root_path}/images/test_{ID}_{kosko_status}.png"
    path2 = f"{package_root_path}/images/kosko_{df_kosko["ID"][0]}_{kosko_status}.png"
    return image_similarity(path1,path2)

def one_shot_kosko_time_series_plotting_abnormal_on():
    ID = df_kosko["ID"].unique()[1]
    dff = df_kosko[df_kosko['ID'] == ID]
    columns_to_exclude = ["ID", "TIME", "DEVICE STATUS"]
    kosko_status = "ON"
    dff = dff[dff["DEVICE STATUS"] == kosko_status]
    columns = [col for col in dff.columns if col not in columns_to_exclude]
    subplot = PlotTimeSeries(dff,columns,"kosko",kosko_status)
    fig = subplot.dash_plot()
    fig.write_image(f"{package_root_path}/images/test_{ID}_{kosko_status}.png")
    path1 = f"{package_root_path}/images/test_{ID}_{kosko_status}.png"
    path2 = f"{package_root_path}/images/kosko_{df_kosko["ID"][0]}_{kosko_status}.png"
    return image_similarity(path1,path2)

def one_shot_kosko_time_series_plotting_abnormal_off():
    ID = df_kosko["ID"].unique()[1]
    dff = df_kosko[df_kosko['ID'] == ID]
    columns_to_exclude = ["ID", "TIME", "DEVICE STATUS"]
    kosko_status = "OFF"
    dff = dff[dff["DEVICE STATUS"] == kosko_status]
    columns = [col for col in dff.columns if col not in columns_to_exclude]
    subplot = PlotTimeSeries(dff,columns,"kosko",kosko_status)
    fig = subplot.dash_plot()
    fig.write_image(f"{package_root_path}/images/test_{ID}_{kosko_status}.png")
    path1 = f"{package_root_path}/images/test_{ID}_{kosko_status}.png"
    path2 = f"{package_root_path}/images/kosko_{df_kosko["ID"][0]}_{kosko_status}.png"
    return image_similarity(path1,path2)

def smoke_time_series_a2ei():
    dff = df_a2ei[df_a2ei['ID'] == 1935]
    columns_to_exclude = ["ID", "TIME"]
    columns = [col for col in dff.columns if col not in columns_to_exclude]
    subplot = PlotTimeSeries(dff,columns,"a2ei",None)
    fig = subplot.dash_plot()
    return fig

def one_shot_a2ei_time_series_plotting_nominal():
    dff = df_a2ei[df_a2ei['ID'] == 1935]
    columns_to_exclude = ["ID", "TIME"]
    columns = [col for col in dff.columns if col not in columns_to_exclude]
    subplot = PlotTimeSeries(dff,columns,"a2ei",None)
    fig = subplot.dash_plot()

    fig.write_image(f"{package_root_path}/images/test_A2EI_{1935}.png")
    path1 = f"{package_root_path}/images/test_A2EI_{1935}.png"
    path2 = f"{package_root_path}/images/A2EI_1935.png"
    return image_similarity(path1,path2)

def one_shot_a2ei_time_series_plotting_abnominal():
    dff = df_a2ei[df_a2ei['ID'] == 1931]
    columns_to_exclude = ["ID", "TIME"]
    columns = [col for col in dff.columns if col not in columns_to_exclude]
    subplot = PlotTimeSeries(dff,columns,"a2ei",None)
    fig = subplot.dash_plot()

    fig.write_image(f"{package_root_path}/images/test_A2EI_{1931}.png")
    path1 = f"{package_root_path}/images/test_A2EI_{1931}.png"
    path2 = f"{package_root_path}/images/A2EI_1935.png"
    return image_similarity(path1,path2)

def smoke_survey_plot():
    map_input = "Bwaise"
    subplot = PlotSurvey(df_survey_processed, map_input)
    fig = subplot.dash_plot()
    return fig

def one_shot_survey_plotting_nominal():
    map_input = "Bwaise"
    subplot = PlotSurvey(df_survey_processed, map_input)
    fig = subplot.dash_plot()
    fig.write_image(f"{package_root_path}/images/test_{map_input}.png")
    path1 = f"{package_root_path}/images/test_{map_input}.png"
    path2 = f"{package_root_path}/images/survey_{map_input}.png"
    return image_similarity(path1,path2)

def one_shot_survey_plotting_abnormal():
    map_input = "Lubya"
    subplot = PlotSurvey(df_survey_processed, map_input)
    fig = subplot.dash_plot()
    fig.write_image(f"{package_root_path}/images/test_{map_input}.png")
    path1 = f"{package_root_path}/images/test_{map_input}.png"
    path2 = f"{package_root_path}/images/survey_Bwaise.png"
    return image_similarity(path1,path2)

def one_shot_attribute_kosko():
    dff = df_kosko[df_kosko['ID'] == df_kosko["ID"][0]]
    columns_to_exclude = ["ID", "TIME", "DEVICE STATUS"]
    kosko_status = "ONOFF"
    columns = [col for col in dff.columns if col not in columns_to_exclude]
    subplot = PlotTimeSeries(dff,columns,"kosko",kosko_status)
    method = getattr(subplot, "kosko")
    return method == subplot.kosko

def one_shot_attribute_a2ei():
    dff = df_a2ei[df_a2ei['ID'] == 1935]
    columns_to_exclude = ["ID", "TIME"]
    columns = [col for col in dff.columns if col not in columns_to_exclude]
    subplot = PlotTimeSeries(dff,columns,"a2ei",None)
    method = getattr(subplot, "a2ei")
    return method == subplot.a2ei

def edge_attribute_improper():
    dff = df_a2ei[df_a2ei['ID'] == 1935]
    columns_to_exclude = ["ID", "TIME"]
    columns = [col for col in dff.columns if col not in columns_to_exclude]
    subplot = PlotTimeSeries(dff,columns,"a2ei",None)
    method = getattr(subplot, "IMPROPER")
    return method

class SurveyProcessing(unittest.TestCase):
    """
    Performs unit testing for survey processing

    Inheritance: unittest.TestCase

    Constructors: None

    """
    def test_smoke_survey(self):
        _ = survey_smoke()
        
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

    def test_one_shot_final_dim(self):
        self.assertEqual(one_shot_final_dim(), len(df_survey["community_name"].unique()))

class KoskoProcessing(unittest.TestCase):
    def test_smoke_kosko(self):
        _ = smoke_kosko()
    
    def test_one_shot_kosko_output(self):
        columns, length = one_shot_kosko_output()
        names = ["TIME","VOLTAGE","CURRENT","WATT","KWH","DEVICE STATUS","ID"]
        N = len(names)
        self.assertEqual((columns,length), (names,N))
    
    def test_final_data_types_kosko(self):
        query =one_shot_kosko_output_data_types()
        data_type = [pd.Timestamp, float,float,float,float,str,str]
        out = np.zeros_like(query)
        i = 0
        for q, d in zip(query,data_type):
            out[i] = isinstance(q,d)
            i += 1
        self.assertEqual(out.sum(), len(data_type))

class A2EIProcessing(unittest.TestCase):
    def test_smoke_A2EI(self):
        _ = smoke_A2EI()
    
    def test_one_shot_A2EI_output(self):
        columns, length = one_shot_A2EI_output()
        names = ["TIME","VOLTAGE","CURRENT","FREQUENCY","POWER","POWER FACTOR","ID"]
        N = len(names)
        self.assertEqual((columns,length), (names,N))
    
    def test_one_shot_A2EI_output_data_types(self):
        query = one_shot_A2EI_output_data_types()
        data_type = [str, float,float,float,float,float,int]
        out = np.zeros_like(query)
        i = 0
        for q, d in zip(query,data_type):
            out[i] = isinstance(q,d)
            i += 1
        self.assertEqual(out.sum(), len(data_type))

class PlotTimeSeriesTesting(unittest.TestCase):
    def test_smoke_time_series_kosko_onoff(self):
        _ = smoke_time_series_kosko_onoff()

    def test_smoke_time_series_kosko_on(self):
        _ = smoke_time_series_kosko_on()

    def test_smoke_time_series_kosko_off(self):
        _ = smoke_time_series_kosko_off()

    def test_kosko_time_series_plotting_nominal_onoff(self):
        self.assertAlmostEqual(one_shot_kosko_time_series_plotting_nominal_onoff(),0.0)
    
    def test_kosko_time_series_plotting_nominal_on(self):
        self.assertAlmostEqual(one_shot_kosko_time_series_plotting_nominal_on(),0.0)

    def test_kosko_time_series_plotting_nominal_off(self):
        self.assertAlmostEqual(one_shot_kosko_time_series_plotting_nominal_off(),0.0)

    def test_kosko_time_series_plotting_abnormal_onoff(self):
        self.assertEqual(not np.isclose(one_shot_kosko_time_series_plotting_abnormal_onoff(),0.0),True)

    def test_kosko_time_series_plotting_abnormal_on(self):
        self.assertEqual(not np.isclose(one_shot_kosko_time_series_plotting_abnormal_on(),0.0),True)

    def test_kosko_time_series_plotting_abnormal_off(self):
        self.assertEqual(not np.isclose(one_shot_kosko_time_series_plotting_abnormal_off(),0.0),True)

    def test_smoke_time_series_a2ei(self):
        _ = smoke_time_series_a2ei()

    def test_a2ei_time_series_plotting_nominal(self):
        self.assertAlmostEqual(one_shot_a2ei_time_series_plotting_nominal(),0.0)

    def test_a2ei_time_series_plotting_abnormal(self):
        self.assertEqual(not np.isclose(one_shot_kosko_time_series_plotting_abnormal_off(),0.0),True)
    
    def test_attribute_kosko(self):
        self.assertEqual(one_shot_attribute_kosko(),True)

    def test_attribute_a2ei(self):
        self.assertEqual(one_shot_attribute_a2ei(),True)

    def test_attribute_improper(self):
        with self.assertRaises(AttributeError):
            edge_attribute_improper()

class PlotSurveyTesting(unittest.TestCase):
    def test_smoke_survey(self):
        _ = smoke_survey_plot()

    def test_similar_plot(self):
        self.assertAlmostEqual(one_shot_survey_plotting_nominal(),0.0)

    def test_dissimilar_plot(self):
        self.assertEqual(not np.isclose(one_shot_survey_plotting_abnormal(),0.0),True)


if __name__ == "__main__":
    unittest.main()









