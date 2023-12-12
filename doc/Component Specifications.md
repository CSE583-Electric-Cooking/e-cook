## Software Components
The SparkBoard software is primarily a data management and visualization tool that serves to illustrate trends in electricity consumption pertaining to the location in which electricity sensor meters are deployed. The software integrates both quantitative data from electric meter sensors as well as qualitative data from survey respondents regarding behavioral patterns in electricity consumption. The software components can be broken up into three components: input, processing and output. The following highlights and describes the functions of each of the individual Python modules that comprise the software package. Each module has been equipped with testing functions to validate and confirm that data input is processed appropriately to minimize errors in results.

#### Input
* ##### extract_data.py
  Raw csv data from electric meter sensors that has previously been formatted is extracted and appended for use in the software.
  This module is only able to take in csv files and will raise an error if any other file types are input for processing by the software.
* ##### organize_data.py
  Disaggregates any combined data or data that needs to be formatted to adhere to software processing requirements.

#### Processing
* ##### process_A2EI.py & process_Kosko.py
  Csv data is processed through scripts to create temporal plots of the following parameters (Voltage - nominal value 240 V, Current
  (A), Power (W), Energy (kWh), Frequency - nominal value 50 Hz). The scripts ensure that temporal date and time measurements are
  converted to appropriate data type formats to ensure consistency with software capabilities.
* ##### process_survey.py <br>
  Survey data is synthesized to identify neighborhoods in which data was collected and identify socioeconomic trends as outlined below. Delineate the type of meter installed in each neighbordhood  
  * Types of electric appliances that are being used in each household
  * Who is the electricity bill payments are being made to
  * Type of connection modality
  * Gender split amongst survey respondents

#### Output
* ##### plotting.py
  Data from CSVs and surveys are plotted along a time seris. These plots are then pashed to the dashboard module for final visualization
  results.
* ##### dashboard.py
  Interactive dashboard built with Plotly Dash to visualize the survey and electric meter data using toggle features to switch between
  quantitative meter and qualitative survey data
