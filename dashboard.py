import os 
from dash import Dash, html, dcc, callback, callback_context, dash_table, Output, Input
import dash_leaflet as dl
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objs as go
import pandas as pd
import module 


class plot_time_series:

    def __init__(self,dff,columns,selected_data_source, kosko_status):
        self.dff = dff
        self.columns = columns
        self.selected_data_source = selected_data_source
        self.kosko_logic = kosko_status != "ONOFF"

    def dash_plot(self):
        fig = make_subplots(rows=len(self.columns), cols=1, subplot_titles=self.columns)
        background_color = '#282828'  
        paper_color = '#343a40'       
        for i, col in enumerate(self.columns, start=1):
            method = f"{self.selected_data_source}"
  
            func = getattr(self, method, None)
            fig = func(fig,col,i)
        title = {"kosko": "Kosko Energy Report", "a2ei": "AE2I Energy Report"}

        fig.update_layout(
            title_text= title[self.selected_data_source],
            height=300*len(self.columns),
            plot_bgcolor=background_color,
            paper_bgcolor=paper_color,
            font=dict(color='white'),  # Set the font color to white
        )
        
        # Optionally, you can also set the grid color to be more subtle
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#444')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#444')
        return fig

    def kosko(self, fig, col, i):
        if self.kosko_logic:
            fig.add_trace(
                go.Scatter(x=self.dff["TIME"], y=self.dff[col], mode='lines', name=col,
                        line=dict(width=2), marker=dict(size=1)),
                row=i, col=1
            )
        else:
            t_on = self.dff["TIME"][self.dff["DEVICE STATUS"] == "OFF"]
            y_on = self.dff[col][self.dff["DEVICE STATUS"] == "OFF"]
            fig.add_trace(
                go.Scatter(x=t_on, y=y_on, mode='lines', name=f"{col} OFF",
                        line=dict(width=2), marker=dict(size=1)),
                row=i, col=1
            )

            t_off = self.dff["TIME"][self.dff["DEVICE STATUS"] == "ON"]
            y_off = self.dff[col][self.dff["DEVICE STATUS"] == "ON"]
            fig.add_trace(
                go.Scatter(x=t_off, y=y_off, mode='lines', name=f"{col} ON",
                        line=dict(width=2), marker=dict(size=1)),
                row=i, col=1
            )
        return fig

    def a2ei(self,fig,col,i):
        if col != "POWER FACTOR":
            fig.add_trace(
                go.Scatter(x=self.dff["TIME"], y=self.dff[col], mode='lines', name=col,
                        line=dict(width=2), marker=dict(size=1)),
                row=i, col=1
            )

        else:
            t = self.dff["TIME"][self.dff[col] != 0]
            y = self.dff[col][self.dff[col] != 0]
            fig.add_trace(
                go.Scatter(x=t, y=y, mode='lines', name=col,
                        line=dict(width=2), marker=dict(size=1)),
                row=i, col=1
            )
            
        return fig
    
    def __getattr__(self, name):
        if name.startswith("kosko"):
            def method(fig, col, i):
                return self.kosko(fig, col, i)
            return method
        elif name.startswith("a2ei"):
            def method(fig, col, i):
                return self.a2ei(fig, col, i)
            return method
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

class plot_survey:
    def __init__(self, dff, survey_selection):
        self.dff = dff[dff["community_name"] == survey_selection]
        
        self.groups = sorted(set(col.split("/")[0] for col in self.dff.columns if "/" in col))
        self.grouped_data = {group: self.dff[[col for col in self.dff.columns if col.startswith(group + "/")]] for group in self.groups}

    def dash_plot(self):
            fig = make_subplots(rows=len(self.grouped_data), cols=1, subplot_titles=[g.capitalize() for g in self.groups])
            background_color = '#282828'
            paper_color = '#343a40'

            for i, (group, data) in enumerate(self.grouped_data.items(), start=1):
                # Check if all values in the group are zero
                if (data == 0).all().all():
                    # Create an empty plot for the group
                    fig.add_trace(
                        go.Bar(x=[], y=[], name="No Data"),
                        row=i, col=1
                    )

                    fig.update_xaxes(showticklabels=False, row=i, col=1)
                    fig.update_yaxes(showticklabels=False, row=i, col=1)
                else:
                    for col in data.columns:
                        simplified_col = col.split("/")[-1]
                        if simplified_col == "a2ei":
                            simplified_col = simplified_col.upper()

                        Y = [data[col].values[0]]
                        if sum(Y) > 0:
                            fig.add_trace(
                                go.Bar(x=[simplified_col.replace("_", " ").capitalize()], y=[data[col].values[0]], name=simplified_col),
                                row=i, col=1
                            )

            fig.update_layout(
                height=300 * len(self.grouped_data),
                showlegend=False,
                plot_bgcolor=background_color,
                paper_bgcolor=paper_color,
                font=dict(color='white')
            )

            return fig

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


data_path = os.path.join(module.__path__[0], '..')
df_kosko = pd.read_csv(os.path.join(f"{data_path}/data/", 'Kosko/Kosko_processed.csv'))
df_a2ei = pd.read_csv(os.path.join(f"{data_path}/data/", 'A2EI/A2EI_processed.csv'))
df_survey = pd.read_csv(os.path.join(f"{data_path}/data/", 'Survey/survey_app_data.csv'))

app = Dash(__name__)

app.layout = html.Div([
    html.H1('Spark-Board', style={'color': '#ffffff', 'textAlign': 'center', 'background': '#343a40', 'padding': '10px', 'margin-bottom': '10px'}),
    
    html.Div([
        dcc.Dropdown(
            id='data-source-selection',
            options=[
                {'label': 'Kosko', 'value': 'kosko'},
                {'label': 'A2EI', 'value': 'a2ei'},
                {'label': 'Survey', 'value': 'survey'}
            ],
            value='kosko',  # Default value
            style={'background': '#333', 'color': '#FFF'}  # Dark background with white text
        ),

        dcc.Dropdown(
            id='dropdown-selection',
            style={'background': '#333', 'color': '#FFF', 'margin-top': '10px', 'margin-bottom': '10px'}  # Same styling with margin-top
        ),

        dcc.Dropdown(
            id='device-on-off',
            options=[
                {'label': 'Device ON', 'value': 'ON'},
                {'label': 'Device OFF', 'value': 'OFF'},
                {'label': 'Device ON/OFF', 'value': 'ONOFF'}
            ],
            value = "ONOFF",
            style={'background': '#333', 'color': '#FFF', 'margin-top': '30px', 'display': 'None'}  # Hidden initially
        ),

    ], style={'background': '#333','padding': '10px', 'width': '30%', 'display': 'inline-block'}),
    
    html.Div([
        html.Div([
            html.H1("Kampala, Uganda", style={'color': '#ffffff', 'textAlign': 'center', 'background': '#343a40', 'padding': '10px', 'margin-bottom': '10px'}),
            dl.Map(
                [dl.TileLayer()] + [
                    dl.CircleMarker(center=coordinates[name],
                                    radius=10,  # Size of the circle marker
                                    color='#333',  # Border color
                                    fill=True,
                                    fillColor='blue',  # Fill color
                                    fillOpacity=0.25, #Fill opacity
                                    id=name)  
                    for name in coordinates],
                style={'width': '1000px', 'height': '600px','backgroundColor': '#343a40'},
                center=(0.31628,32.58219),  # Center the map around one of the locations
                zoom=13,
                id="map"
            ),
        html.Div(id="location-info")
        ], id='map-container', style={'backgroundColor': '#343a40','display': 'block'})  # Initial display style
    ], style={'backgroundColor': '#343a40', 'padding': '30px', 'color': '#FFF', 'display': 'flex', 'justifyContent': 'center'}),

    html.Div(
        dcc.Graph(id='graph-content'),
        id='graph-container'  
    ),
],style={'backgroundColor': '#333','padding': '30px'})

@callback(
    Output('dropdown-selection', 'options'),
    [Input('data-source-selection', 'value')]
)
def update_dropdown_options(selected_data_source):
    if selected_data_source == 'kosko':
        def name(i): 
            if int(i) < 100: 
                return f"0{i}" 
            else:
                return i
        return [{'label': f"EM-{name(i)}", 'value': i} for i in df_kosko['ID'].unique()]
    elif selected_data_source == 'a2ei':
        return [{'label': i, 'value': i} for i in df_a2ei['ID'].unique()]
    else:
        return []
    
@callback(
    [Output('graph-content', 'style'),Output('dropdown-selection', 'style'), Output('map-container', 'style')],
    [Input('data-source-selection', 'value'),Input("location-info",'children')]
)
def hide_graph(selected_data_source,survey_selection):
    if selected_data_source == "survey":
        if survey_selection == None:
            return {'display': 'None'}, {'display': 'None'}, {'display':'block'}
        else:
            return {'display': 'block'}, {'display': 'None'}, {'display':'block'}
    else:
        return {'display': 'block'}, {'background': '#333'}, {'display': 'None'}

@callback(
    Output('graph-content', 'figure'),
    [Input('data-source-selection', 'value'), Input('dropdown-selection', 'value'),Input('device-on-off', 'value'),Input("location-info",'children')]
)
def update_graph(selected_data_source, selected_account_id, kosko_status, survey_selection):
    flag = True
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
        if survey_selection == None:
            return go.Figure()
        else:
            map_input = str(survey_selection[0]['props']['children'])
            subplot = plot_survey(df_survey, map_input)
            return subplot.dash_plot()
    else:
        dff = pd.DataFrame()
        columns_to_exclude = []
        
    columns = [col for col in dff.columns if col not in columns_to_exclude]
    subplot = plot_time_series(dff,columns,selected_data_source,kosko_status)

    
    return subplot.dash_plot()

@app.callback(
    Output('device-on-off', 'style'),
    [Input('data-source-selection', 'value')]
)
def show_hidden_dropdown(selected_data_source):
    if selected_data_source == 'kosko':
        return {'background': '#333'}  # Show the dropdown
    else:
        return {'display': 'none'}  # Hide the dropdown

@app.callback(
    Output("location-info", "children"),
    [Input(name, "n_clicks") for name in coordinates],
    prevent_initial_call=True
)
def display_location_info(*args):
    ctx = callback_context
    if not ctx.triggered:
        return None
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        out =html.H1(f"{button_id}", style={'color': '#ffffff', 'textAlign': 'center', 
                                            'background': '#343a40', 'padding': '10px', 
                                            'margin-bottom': '10px'}),

        return out

if __name__ == '__main__':
    app.run_server(debug=True)
