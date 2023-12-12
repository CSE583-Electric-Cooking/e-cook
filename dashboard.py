"""
This dashboard generates an interactive web app in which users can quickly query
and parse data from a collection of qualitative and quantiative results. This 
includes time series and survery data regarding power usage.

Depencies:
    - os: file naviaigation
    - pandas: CSV/Dataframe manipulation
    - dash: Framework for the development of the app functionality
    - plotly.graph_objs: plotting framework integrated into dash app
    - sparkboard/sparkboard.plotting: custom module for the generation of plotly graphs
"""
import os
import pandas as pd
from dash import Dash, html, dcc, callback, callback_context, Output, Input
import dash_leaflet as dl
import plotly.graph_objs as go
import sparkboard as sb
from sparkboard.plotting import PlotSurvey,PlotTimeSeries
# Decimal GPS Coordinates for different communities in Kampala, Uganda
coordinates = {
    "Kyebando Kisalosalo": (0.3561, 32.5800),
    "Makerere": (0.3350, 32.5700),
    "Kibuye": (0.2936, 32.5731),
    "Banda": (0.3539, 32.6325),
    "Lubya": (0.3296, 32.5459),
    "Katwe": (0.2967, 32.5756),
    "Nsambya Gogonya": (0.2992, 32.5881),
    "Mengo": (0.3017, 32.5661),
    "Bwaise": (0.3500, 32.5611),
    "Kanyanya": (0.3736, 32.5772)
}

# Load data from path, navigates to data directory, loads data frames
data_path = os.path.join(sb.__path__[0], '..')
df_kosko = pd.read_csv(os.path.join(f"{data_path}/data/", 'Kosko/Kosko_processed.csv'))
df_a2ei = pd.read_csv(os.path.join(f"{data_path}/data/", 'A2EI/A2EI_processed.csv'))
df_survey = pd.read_csv(os.path.join(f"{data_path}/data/", 'Survey/survey_app_data.csv'))

# App inialization
app = Dash(__name__)

app.layout = html.Div([
    html.H1('Spark-Board', style={'color': '#ffffff',
                                  'textAlign': 'center',
                                  'background': '#343a40',
                                  'padding': '10px',
                                  'margin-bottom': '10px'}),
    # HTML Div to structure the drop down options
    html.Div([
        dcc.Dropdown(
            id='data-source-selection',
            options=[
                {'label': 'Kosko', 'value': 'kosko'},
                {'label': 'A2EI', 'value': 'a2ei'},
                {'label': 'Survey', 'value': 'survey'}
            ],
            value='kosko',
            style={'background': '#333',
                   'color': '#FFF'}
        ), #Drop down to control which data set is being used
        dcc.Dropdown(
            id='dropdown-selection',
            style={'background': '#333',
                   'color': '#FFF',
                   'margin-top': '10px',
                   'margin-bottom': '10px'}
        ), #Drop down to control which user time series to observe
        dcc.Dropdown(
            id='device-on-off',
            options=[
                {'label': 'Device ON', 'value': 'ON'},
                {'label': 'Device OFF', 'value': 'OFF'},
                {'label': 'Device ON/OFF', 'value': 'ONOFF'}
            ],
            value = "ONOFF",
            style={'background': '#333',
                   'color': '#FFF',
                   'margin-top': '30px',
                   'display': 'None'}
        ), #Specifcally for kosko, drop down to control how the data is being overlayed
    ], style={'background': '#333',
              'padding': '10px',
              'width': '30%',
              'display':
              'inline-block'}),
    html.Div([
        html.Div([
            html.H1("Kampala, Uganda", style={'color': '#ffffff',
                                              'textAlign': 'center',
                                              'background': '#343a40',
                                              'padding': '10px',
                                              'margin-bottom': '10px'}),
            dl.Map(
                [dl.TileLayer()] + [
                    dl.CircleMarker(center=coordinates[name],
                                    radius=10,
                                    color='#333',
                                    fill=True,
                                    fillColor='blue',
                                    fillOpacity=0.25,
                                    id=name)
                    for name in df_survey["community_name"].unique()],
                style={'width': '1000px',
                       'height': '600px',
                       'backgroundColor': '#343a40'},
                center=(0.31628,32.58219),
                zoom=13,
                id="map"
            ),
        html.Div(id="location-info")
        ], id='map-container', style={'backgroundColor': '#343a40',
                                      'display': 'block'})
    ], style={'backgroundColor': '#343a40',
              'padding': '30px', 'color':
              '#FFF', 'display': 'flex',
              'justifyContent': 'center'}),
    #Defines interactable circle map markers to toggle display of bar graphs center in kampala
    html.Div(
        dcc.Graph(id='graph-content'),
        id='graph-container'
    ),
    #Graph object used either for plotting time series or bar graphs
],style={'backgroundColor': '#333',
         'padding': '30px'})

@callback(
    Output('dropdown-selection', 'options'),
    [Input('data-source-selection', 'value')]
)
def update_dropdown_options(selected_data_source):
    """
    Update dropdown options based on the selected data source.

    Args:
    selected_data_source (str): The selected data source.

    Returns:
    list: A list of options for the dropdown.
    """

    if selected_data_source == 'kosko':
        return [{'label': f"EM-{i}", 'value': i} for i in df_kosko['ID'].unique()]
    if selected_data_source == 'a2ei':
        return [{'label': i, 'value': i} for i in df_a2ei['ID'].unique()]
    return []

@callback(
    [Output('graph-content', 'style'),
     Output('dropdown-selection', 'style'),
     Output('map-container', 'style'),
     Output('device-on-off', 'style')],
    [Input('data-source-selection', 'value'),Input("location-info",'children')]
)
def display_logic(selected_data_source,survey_selection):
    """
    Define the display logic for different components based on the selected data source 
    and survey selection.

    Args:
    selected_data_source (str): The selected data source.
    survey_selection: (tuple or None) The selected survey data.

    Returns:
    tuple: Styles for graph content, dropdown selection, map container, and device on-off switch.
    """
    if selected_data_source == "survey":
        if survey_selection is None:
            return {'display': 'None'}, {'display': 'None'}, {'display':'block'},{'display':'None'}
        return {'display': 'block'}, {'display': 'None'}, {'display':'block'},{'display':'None'}
    if selected_data_source == "kosko":
        return {'display':'block'},{'background':'#333'},{'display':'None'},{'background':'#333'}
    if selected_data_source == "a2ei":
        return {'display':'block'},{'background': 'None'},{'display':'None'},{'display':'None'}
    return {'display': 'None'},{'background': 'None'},{'display': 'None'},{'display':'None'}

@callback(
    Output('graph-content', 'figure'),
    [Input('data-source-selection', 'value'),
     Input('dropdown-selection', 'value'),
     Input('device-on-off', 'value'),
     Input("location-info",'children')]
)
def update_graph(selected_data_source, selected_account_id, kosko_status, survey_selection):
    """
    Update the graph based on various inputs like data source, 
    account ID, device status, and survey selection.

    Args:
    selected_data_source (str): The selected data source.
    selected_account_id (str): Selected account ID.
    kosko_status (str): The status of the Kosko device (ON/OFF).
    survey_selection (tuple or None): The selected survey data.

    Returns:
    object: Plotly graph object.
    """
    if selected_data_source == 'kosko':
        dff = df_kosko[df_kosko['ID'] == selected_account_id]
        columns_to_exclude = ["ID", "TIME", "DEVICE STATUS"]
        if not kosko_status == "ONOFF":
            dff = dff[dff["DEVICE STATUS"] == kosko_status]
    elif selected_data_source == 'a2ei':
        dff = df_a2ei[df_a2ei['ID'] == selected_account_id]
        columns_to_exclude = ["ID", "TIME"]
    elif selected_data_source == 'survey':
        ### GET DATA FROM MAP CLICKS
        if survey_selection is None:
            return go.Figure()
        map_input = str(survey_selection['props']['children'])
        subplot = PlotSurvey(df_survey, map_input)
        return subplot.dash_plot()
    else:
        return go.Figure()
    columns = [col for col in dff.columns if col not in columns_to_exclude]
    subplot = PlotTimeSeries(dff,columns,selected_data_source,kosko_status)

    return subplot.dash_plot()

@app.callback(
    Output("location-info", "children"),
    [Input(name, "n_clicks") for name in coordinates],
    prevent_initial_call=True
)
def display_location_info(*args):
    """
    Display location information based on user interactions with the map.

    Args:
    args: Arguments passed from the callback, representing the number of clicks for each location.

    Returns:
    html component: Displaying the location information.
    """
    ctx = callback_context
    if not ctx.triggered:
        return None
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    args = str(args)
    out =html.H1(f"{button_id}", style={'color': '#ffffff', 'textAlign': 'center',
                                        'background': '#343a40', 'padding': '10px',
                                        'margin-bottom': '10px'})

    return out

if __name__ == '__main__':
    app.run_server(debug=True)
