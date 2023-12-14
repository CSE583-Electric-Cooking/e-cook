"""
This module provides the testing framework for the development of the processing 
and plotting scripts. Imports relevant packages, navigates to data directory for
samples to embedd in tests. Performs basic image comparisons.
"""
import os
import unittest
import pandas as pd
import numpy as np
from PIL import Image, ImageOps

from ..plotting import plotting
from ..process_survey import process_name, column_reduction, column_reduction_n
from ..process_survey import remove_sparse_columns,process_data_survey
from ..process_kosko import Kosko
from ..process_a2ei import A2EI


plotting_path = os.path.abspath(plotting.__file__)
parent_directory = os.path.dirname(plotting_path)
package_root_path = os.path.dirname(parent_directory)
ecook = os.path.dirname(package_root_path)
data_directory = os.path.join(ecook, 'data')

kosko_directory = os.path.join(data_directory, "Kosko")
A2EI_directory = os.path.join(data_directory, "A2EI")
survey_directory = os.path.join(data_directory, "Survey")


### Helper Functions
def image_similarity(path1,path2):
    """
    Simple function to open two images and compute the norm (Frobenius) of the error

    input:

    path1 (str): path to image 1
    path2 (str): path to image 2

    return:

    norm (float): value of the norm, if two images are close, norm should be close to
    zero
    """
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
    """
    Test overall processing script
    """
    return process_data_survey(write_csv = False)

def one_shot_process_name_community():
    """
    Test the functionality of community name processing, remove non alphabetical characters,
    replaces under scores with spaces
    """
    string_input = "$queen_ann$@"
    str(string_input)
    return process_name(string_input, mode = "community")

def one_shot_process_name_delinator():
    """
    Test the functionality of the code to seperate a "/" from a list for later grouping of data

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
    """
    Evaluate if the community Kyebando Kisalosalo contains the right ratio
    """
    community = df_survey["community_name"].unique()[0]
    data = df_survey[df_survey["community_name"] == community]
    return list(column_reduction(data,"Participant_gender")[-1][0])

def one_shot_column_reduction_n():
    """
    Evaluate if the applicance matirix is being correctly reduced to a vector
    """
    community = df_survey["community_name"].unique()[0]
    data = df_survey[df_survey["community_name"] == community]
    vec = np.array(column_reduction_n(data,"appliances/")[-1][0])
    m = vec.shape
    return m[0], int(vec.sum())

def one_shot_remove_sparsity():
    """
    Test empty data matrices (0) are being removed
    """
    community = df_survey["community_name"].unique()[0]
    data = pd.DataFrame({"community_name": community,"data": np.ones(5),"sparse":np.zeros(5)})
    return remove_sparse_columns(data)

def edge_remove_sparsity():
    """
    Test nonnumerical entries persisting
    """
    community = df_survey["community_name"].unique()[0]
    data = pd.DataFrame({"community_name": community,"data": "a","sparse":np.zeros(5)})
    return remove_sparse_columns(data)

def one_shot_final_dim():
    """
    Test final dimensions of survey processing
    """
    df = process_data_survey(write_csv = False)
    dim = len(df)
    return dim

def smoke_kosko():
    """
    Smoke test to see if Kosko runs
    """
    return Kosko(write_csv = False)

def one_shot_kosko_output():
    """
    Test to see is columns names, and number are as expected
    """
    kosko = Kosko(write_csv=False)
    columns = kosko.df.columns
    return list(columns),len(columns)

def one_shot_kosko_output_data_types():
    """
    Test to see is data types are as expected
    """
    kosko = Kosko(write_csv=False)
    query = kosko.df.values[0]
    return query

def smoke_a2ei():
    """
    Smoke test to see if A2EI runs
    """
    return A2EI(write_csv = False)

def one_shot_a2ei_output():
    """
    Test to see is columns names, and number are as expected
    """
    a2ei = A2EI(write_csv=False)
    columns = a2ei.df.columns
    return list(columns),len(columns)

def one_shot_a2ei_output_data_types():
    """
    Test to see is data types are as expected
    """
    a2ei = A2EI(write_csv=False)
    query = a2ei.df.values[0]
    return query

def smoke_time_series_kosko_onoff():
    """
    Test to see if call to the plotting function runs on ON/OFF
    """
    dff = df_kosko[df_kosko['ID'] == df_kosko['ID'][0]]
    columns_to_exclude = ['ID', "TIME", "DEVICE STATUS"]
    kosko_status = "ONOFF"
    columns = [col for col in dff.columns if col not in columns_to_exclude]
    subplot = plotting.PlotTimeSeries(dff,columns,"kosko",kosko_status)
    fig = subplot.dash_plot()
    return fig

def smoke_time_series_kosko_on():
    """
    Test to see if call to the plotting function runs ON
    """
    dff = df_kosko[df_kosko['ID'] == df_kosko['ID'][0]]
    columns_to_exclude = ['ID', "TIME", "DEVICE STATUS"]
    kosko_status = "ON"
    dff = dff[dff["DEVICE STATUS"] == kosko_status]
    columns = [col for col in dff.columns if col not in columns_to_exclude]
    subplot = plotting.PlotTimeSeries(dff,columns,"kosko",kosko_status)
    fig = subplot.dash_plot()
    return fig

def smoke_time_series_kosko_off():
    """
    Kosko
    Test to see if call to the plotting function runs OFF
    """
    dff = df_kosko[df_kosko['ID'] == df_kosko['ID'][0]]
    columns_to_exclude = ['ID', "TIME", "DEVICE STATUS"]
    kosko_status = "OFF"
    dff = dff[dff["DEVICE STATUS"] == kosko_status]
    columns = [col for col in dff.columns if col not in columns_to_exclude]
    subplot = plotting.PlotTimeSeries(dff,columns,"kosko",kosko_status)
    fig = subplot.dash_plot()
    return fig

def one_shot_kosko_time_series_plotting_nominal_onoff():
    """
    Kosko
    Compare output png to freshly generated png, compare based on Frobenius norm of error (ONOFF)
    """
    dff = df_kosko[df_kosko['ID'] == df_kosko['ID'][0]]
    columns_to_exclude = ['ID', "TIME", "DEVICE STATUS"]
    kosko_status = "ONOFF"
    columns = [col for col in dff.columns if col not in columns_to_exclude]
    subplot = plotting.PlotTimeSeries(dff,columns,"kosko",kosko_status)
    fig = subplot.dash_plot()
    fig.write_image(f"{package_root_path}/images/test_{df_kosko['ID'][0]}_{kosko_status}.png")
    path1 = f"{package_root_path}/images/test_{df_kosko['ID'][0]}_{kosko_status}.png"
    path2 = f"{package_root_path}/images/kosko_{df_kosko['ID'][0]}_{kosko_status}.png"
    return image_similarity(path1,path2)

def one_shot_kosko_time_series_plotting_nominal_on():
    """
    Kosko
    Compare output png to freshly generated png, compare based on Frobenius norm of error (ON)
    """
    dff = df_kosko[df_kosko['ID'] == df_kosko['ID'][0]]
    columns_to_exclude = ['ID', "TIME", "DEVICE STATUS"]
    kosko_status = "ON"
    dff = dff[dff["DEVICE STATUS"] == kosko_status]
    columns = [col for col in dff.columns if col not in columns_to_exclude]
    subplot = plotting.PlotTimeSeries(dff,columns,"kosko",kosko_status)
    fig = subplot.dash_plot()
    fig.write_image(f"{package_root_path}/images/test_{df_kosko['ID'][0]}_{kosko_status}.png")
    path1 = f"{package_root_path}/images/test_{df_kosko['ID'][0]}_{kosko_status}.png"
    path2 = f"{package_root_path}/images/kosko_{df_kosko['ID'][0]}_{kosko_status}.png"
    return image_similarity(path1,path2)

def one_shot_kosko_time_series_plotting_nominal_off():
    """
    Kosko
    Compare output png to freshly generated png, compare based on Frobenius norm of error (OFF)
    """
    dff = df_kosko[df_kosko['ID'] == df_kosko['ID'][0]]
    columns_to_exclude = ['ID', "TIME", "DEVICE STATUS"]
    kosko_status = "OFF"
    dff = dff[dff["DEVICE STATUS"] == kosko_status]
    columns = [col for col in dff.columns if col not in columns_to_exclude]
    subplot = plotting.PlotTimeSeries(dff,columns,"kosko",kosko_status)
    fig = subplot.dash_plot()
    fig.write_image(f"{package_root_path}/images/test_{df_kosko['ID'][0]}_{kosko_status}.png")
    path1 = f"{package_root_path}/images/test_{df_kosko['ID'][0]}_{kosko_status}.png"
    path2 = f"{package_root_path}/images/kosko_{df_kosko['ID'][0]}_{kosko_status}.png"
    return image_similarity(path1,path2)

def one_shot_kosko_time_series_plotting_abnormal_onoff():
    """
    Kosko
    Compare output png to freshly generated incorrectpng, 
    compare based on Frobenius norm of error (ONOFF)
    """
    id_ = df_kosko['ID'].unique()[1]
    dff = df_kosko[df_kosko['ID'] == id_]
    columns_to_exclude = ['ID', "TIME", "DEVICE STATUS"]
    kosko_status = "ONOFF"
    columns = [col for col in dff.columns if col not in columns_to_exclude]
    subplot = plotting.PlotTimeSeries(dff,columns,"kosko",kosko_status)
    fig = subplot.dash_plot()
    fig.write_image(f"{package_root_path}/images/test_{id_}_{kosko_status}.png")
    path1 = f"{package_root_path}/images/test_{id_}_{kosko_status}.png"
    path2 = f"{package_root_path}/images/kosko_{df_kosko['ID'][0]}_{kosko_status}.png"
    return image_similarity(path1,path2)

def one_shot_kosko_time_series_plotting_abnormal_on():
    """
    Kosko
    Compare output png to freshly generated incorrectpng, 
    compare based on Frobenius norm of error (ON)
    """
    id_ = df_kosko['ID'].unique()[1]
    dff = df_kosko[df_kosko['ID'] == id_]
    columns_to_exclude = ['ID', "TIME", "DEVICE STATUS"]
    kosko_status = "ON"
    dff = dff[dff["DEVICE STATUS"] == kosko_status]
    columns = [col for col in dff.columns if col not in columns_to_exclude]
    subplot = plotting.PlotTimeSeries(dff,columns,"kosko",kosko_status)
    fig = subplot.dash_plot()
    fig.write_image(f"{package_root_path}/images/test_{id_}_{kosko_status}.png")
    path1 = f"{package_root_path}/images/test_{id_}_{kosko_status}.png"
    path2 = f"{package_root_path}/images/kosko_{df_kosko['ID'][0]}_{kosko_status}.png"
    return image_similarity(path1,path2)

def one_shot_kosko_time_series_plotting_abnormal_off():
    """
    Kosko
    Compare output png to freshly generated incorrectpng, 
    compare based on Frobenius norm of error (OFF)
    """
    id_ = df_kosko['ID'].unique()[1]
    dff = df_kosko[df_kosko['ID'] == id_]
    columns_to_exclude = ['ID', "TIME", "DEVICE STATUS"]
    kosko_status = "OFF"
    dff = dff[dff["DEVICE STATUS"] == kosko_status]
    columns = [col for col in dff.columns if col not in columns_to_exclude]
    subplot = plotting.PlotTimeSeries(dff,columns,"kosko",kosko_status)
    fig = subplot.dash_plot()
    fig.write_image(f"{package_root_path}/images/test_{id_}_{kosko_status}.png")
    path1 = f"{package_root_path}/images/test_{id_}_{kosko_status}.png"
    path2 = f"{package_root_path}/images/kosko_{df_kosko['ID'][0]}_{kosko_status}.png"
    return image_similarity(path1,path2)

def smoke_time_series_a2ei():
    """
    Kosko
    Test to see if call to the plotting function runs 
    """
    dff = df_a2ei[df_a2ei['ID'] == 1935]
    columns_to_exclude = ['ID', "TIME"]
    columns = [col for col in dff.columns if col not in columns_to_exclude]
    subplot = plotting.PlotTimeSeries(dff,columns,"a2ei",None)
    fig = subplot.dash_plot()
    return fig

def one_shot_a2ei_time_series_plotting_nominal():
    """
    A2EI
    Compare output png to freshly generated png, compare based on Frobenius norm of error
    """
    dff = df_a2ei[df_a2ei['ID'] == 1935]
    columns_to_exclude = ['ID', "TIME"]
    columns = [col for col in dff.columns if col not in columns_to_exclude]
    subplot = plotting.PlotTimeSeries(dff,columns,"a2ei",None)
    fig = subplot.dash_plot()

    fig.write_image(f"{package_root_path}/images/test_A2EI_{1935}.png")
    path1 = f"{package_root_path}/images/test_A2EI_{1935}.png"
    path2 = f"{package_root_path}/images/A2EI_1935.png"
    return image_similarity(path1,path2)

def one_shot_a2ei_time_series_plotting_abnominal():
    """
    A2EI
    Compare output png to freshly generated incorrect png, 
    compare based on Frobenius norm of error
    """
    dff = df_a2ei[df_a2ei['ID'] == 1931]
    columns_to_exclude = ['ID', "TIME"]
    columns = [col for col in dff.columns if col not in columns_to_exclude]
    subplot = plotting.PlotTimeSeries(dff,columns,"a2ei",None)
    fig = subplot.dash_plot()

    fig.write_image(f"{package_root_path}/images/test_A2EI_{1931}.png")
    path1 = f"{package_root_path}/images/test_A2EI_{1931}.png"
    path2 = f"{package_root_path}/images/A2EI_1935.png"
    return image_similarity(path1,path2)

def smoke_survey_plot():
    """
    Test to see if the code generates a bar graph
    """
    map_input = "Bwaise"
    subplot = plotting.PlotSurvey(df_survey_processed, map_input)
    fig = subplot.dash_plot()
    return fig

def one_shot_survey_plotting_nominal():
    """
    Compare output png to freshly generated png, compare based on Frobenius norm of error
    """
    map_input = "Bwaise"
    subplot = plotting.PlotSurvey(df_survey_processed, map_input)
    fig = subplot.dash_plot()
    fig.write_image(f"{package_root_path}/images/test_{map_input}.png")
    path1 = f"{package_root_path}/images/test_{map_input}.png"
    path2 = f"{package_root_path}/images/survey_{map_input}.png"
    return image_similarity(path1,path2)

def one_shot_survey_plotting_abnormal():
    """
    Compare output png to freshly generated incorrect png, 
    compare based on Frobenius norm of error
    """
    map_input = "Lubya"
    subplot = plotting.PlotSurvey(df_survey_processed, map_input)
    fig = subplot.dash_plot()
    fig.write_image(f"{package_root_path}/images/test_{map_input}.png")
    path1 = f"{package_root_path}/images/test_{map_input}.png"
    path2 = f"{package_root_path}/images/survey_Bwaise.png"
    return image_similarity(path1,path2)

def one_shot_attribute_kosko():
    """
    Test atttribute call returning proper method Kosko
    """
    dff = df_kosko[df_kosko['ID'] == df_kosko['ID'][0]]
    columns_to_exclude = ['ID', "TIME", "DEVICE STATUS"]
    kosko_status = "ONOFF"
    columns = [col for col in dff.columns if col not in columns_to_exclude]
    subplot = plotting.PlotTimeSeries(dff,columns,"kosko",kosko_status)
    method = getattr(subplot, "kosko")
    return method == subplot.kosko

def one_shot_attribute_a2ei():
    """
    Test atttribute call returning proper method A2EI
    """
    dff = df_a2ei[df_a2ei['ID'] == 1935]
    columns_to_exclude = ['ID', "TIME"]
    columns = [col for col in dff.columns if col not in columns_to_exclude]
    subplot = plotting.PlotTimeSeries(dff,columns,"a2ei",None)
    method = getattr(subplot, "a2ei")
    return method == subplot.a2ei

def edge_attribute_improper():
    """
    Test atttribute call raising AttributeError for incorrect input
    """
    dff = df_a2ei[df_a2ei['ID'] == 1935]
    columns_to_exclude = ['ID', "TIME"]
    columns = [col for col in dff.columns if col not in columns_to_exclude]
    subplot = plotting.PlotTimeSeries(dff,columns,"a2ei",None)
    method = getattr(subplot, "IMPROPER")
    return method

class SurveyProcessing(unittest.TestCase):
    """
    Performs unit testing for survey processing
    """
    def test_smoke_survey(self):
        """Test basic functionality of survey processing."""
        _ = survey_smoke()

    def test_one_shot_community(self):
        """Ensure correct processing of community names."""
        self.assertEqual(one_shot_process_name_community(), "Queen Ann")

    def test_one_shot_deliniator(self):
        """Check delimiter functionality in name processing."""
        self.assertEqual(one_shot_process_name_delinator(), "test")

    def test_edge_whitelist(self):
        """Ensure ValueError is raised for non-whitelisted modes."""
        with self.assertRaises(ValueError):
            edge_whitelist()

    def test_edge_incorrect_data_type(self):
        """Test error handling for incorrect data types."""
        with self.assertRaises(ValueError):
            edge_incorrect_data_type()

    def test_one_shot_column_reduction(self):
        """Verify correct column reduction in survey data."""
        self.assertEqual(one_shot_column_reduction(), ['3','2'])

    def test_one_shot_column_reduction_n(self):
        """Ensure matrix-to-vector reduction works correctly."""
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
        """Check if sparse data columns are removed properly."""
        community = df_survey["community_name"].unique()[0]
        data = pd.DataFrame({"community_name": community,"data": np.ones(5)})
        self.assertEqual(one_shot_remove_sparsity().values.all(), data.values.all())

    def test_one_shot_final_dim(self):
        """Test if final dimension of processed survey data is correct."""
        self.assertEqual(one_shot_final_dim(), len(df_survey["community_name"].unique()))

class KoskoProcessing(unittest.TestCase):
    """
    Performs unit testing for Kosko processing.
    """
    def test_smoke_kosko(self):
        """Smoke test for basic functionality of Kosko."""
        _ = smoke_kosko()

    def test_one_shot_kosko_output(self):
        """Verify Kosko output columns and length."""
        columns, length = one_shot_kosko_output()
        names = ["TIME","VOLTAGE","CURRENT","WATT","KWH","DEVICE STATUS",'ID']
        self.assertEqual((columns,length), (names,len(names)))

    def test_final_data_types_kosko(self):
        """Check if Kosko data types are as expected."""
        query =one_shot_kosko_output_data_types()
        data_type = [pd.Timestamp, float,float,float,float,str,str]
        out = [isinstance(q,d) for q,d in zip(query,data_type)]
        self.assertEqual(sum(out), len(data_type))

class A2EIProcessing(unittest.TestCase):
    """
    Performs unit testing for A2EI processing
    """
    def test_smoke_a2ei(self):
        """Smoke test for basic functionality of A2EI."""
        _ = smoke_a2ei()

    def test_one_shot_a2ei_output(self):
        """Verify A2EI output columns and length."""
        columns, length = one_shot_a2ei_output()
        names = ["TIME","VOLTAGE","CURRENT","FREQUENCY","POWER","POWER FACTOR",'ID']
        self.assertEqual((columns,length), (names,len(names)))

    def test_one_shot_a2ei_output_data_types(self):
        """Check if A2EI data types are as expected."""
        query = one_shot_a2ei_output_data_types()
        data_type = [str, float,float,float,float,float,int]
        out = [isinstance(q,d) for q,d in zip(query,data_type)]
        self.assertEqual(sum(out), len(data_type))

class PlotTimeSeriesTesting(unittest.TestCase):
    """Perform unit testing for time series plotting."""
    def test_smoke_time_series_kosko_onoff(self):
        """Test plotting functionality for Kosko ON/OFF status."""
        _ = smoke_time_series_kosko_onoff()

    def test_smoke_time_series_kosko_on(self):
        """Test plotting functionality for Kosko ON status."""
        _ = smoke_time_series_kosko_on()

    def test_smoke_time_series_kosko_off(self):
        """Test plotting functionality for Kosko OFF status."""
        _ = smoke_time_series_kosko_off()

    def test_kosko_time_series_plotting_nominal_onoff(self):
        """Compare nominal and generated plots for Kosko ON/OFF status."""
        self.assertAlmostEqual(one_shot_kosko_time_series_plotting_nominal_onoff(),0.0)

    def test_kosko_time_series_plotting_nominal_on(self):
        """Compare nominal and generated plots for Kosko ON status."""
        self.assertAlmostEqual(one_shot_kosko_time_series_plotting_nominal_on(),0.0)

    def test_kosko_time_series_plotting_nominal_off(self):
        """Compare nominal and generated plots for Kosko OFF status."""
        self.assertAlmostEqual(one_shot_kosko_time_series_plotting_nominal_off(),0.0)

    def test_kosko_time_series_plotting_abnormal_onoff(self):
        """Test plot comparison for abnormal cases in Kosko ON/OFF status."""
        self.assertEqual(not np.isclose(one_shot_kosko_time_series_plotting_abnormal_onoff(),0),1)

    def test_kosko_time_series_plotting_abnormal_on(self):
        """Test plot comparison for abnormal cases in Kosko ON status."""
        self.assertEqual(not np.isclose(one_shot_kosko_time_series_plotting_abnormal_on(),0),1)

    def test_kosko_time_series_plotting_abnormal_off(self):
        """Test plot comparison for abnormal cases in Kosko OFF status."""
        self.assertEqual(not np.isclose(one_shot_kosko_time_series_plotting_abnormal_off(),0),1)

    def test_smoke_time_series_a2ei(self):
        """Smoke test for A2EI time series plotting."""
        _ = smoke_time_series_a2ei()

    def test_a2ei_time_series_plotting_nominal(self):
        """Compare nominal and generated plots for A2EI."""
        self.assertAlmostEqual(one_shot_a2ei_time_series_plotting_nominal(),0.0)

    def test_a2ei_time_series_plotting_abnormal(self):
        """"Test plot comparison for abnormal cases in A2EI."""
        self.assertEqual(not np.isclose(one_shot_kosko_time_series_plotting_abnormal_off(),0.0),1)

    def test_attribute_kosko(self):
        """Ensure correct attribute retrieval for Kosko."""
        self.assertEqual(one_shot_attribute_kosko(),True)

    def test_attribute_a2ei(self):
        """Ensure correct attribute retrieval for A2EI."""
        self.assertEqual(one_shot_attribute_a2ei(),True)

    def test_attribute_improper(self):
        """Check for AttributeError on invalid attribute access."""
        with self.assertRaises(AttributeError):
            edge_attribute_improper()

class PlotSurveyTesting(unittest.TestCase):
    """Perform unit testing for survey plotting."""
    def test_smoke_survey(self):
        """Smoke test for survey plotting functionality."""
        _ = smoke_survey_plot()

    def test_similar_plot(self):
        """Ensure similarity in expected and actual survey plots."""
        self.assertAlmostEqual(one_shot_survey_plotting_nominal(),0.0)

    def test_dissimilar_plot(self):
        """Test for differences in expected and actual survey plots."""
        self.assertEqual(not np.isclose(one_shot_survey_plotting_abnormal(),0.0),1)

if __name__ == "__main__":
    unittest.main()
