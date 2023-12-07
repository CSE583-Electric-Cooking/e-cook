import os 
from dash import Dash, html, dcc, callback, callback_context, Output, Input
import dash_leaflet as dl
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objs as go
import pandas as pd
import module 


class plot_ts:

    def __init__(self,dff,columns,selected_data_source, kosko_status):
        self.dff = dff
        self.columns = columns
        self.selected_data_source = selected_data_source
        self.kosko_logic = kosko_status != "ONOFF"

    def dash_plot(self):
        fig = make_subplots(rows=len(self.columns), cols=1, subplot_titles=self.columns)
        background_color = '#282828'  # Dark gray to match your app's background
        paper_color = '#343a40'       # Slightly lighter gray for the figure's background
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
df_survey = pd.read_csv(os.path.join(f"{data_path}/data/", 'Survey/Consumption Monitoring Survey_modified.csv'))

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']



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
    
    html.Div(
        dcc.Graph(id='graph-content'),
        id='graph-container'  
    ),

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
    ], style={'backgroundColor': '#343a40', 'padding': '30px', 'color': '#FFF', 'display': 'flex', 'justifyContent': 'center'})
    
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
    [Input('data-source-selection', 'value')]
)
def hide_graph(selected_data_source):
    if selected_data_source == "survey":
        return {'display': 'None'}, {'display': 'None'}, {'display':'block'}
    else:
        return {'display': 'block'}, {'background': '#333'}, {'display': 'None'}

@callback(
    Output('graph-content', 'figure'),
    [Input('data-source-selection', 'value'), Input('dropdown-selection', 'value'),Input('device-on-off', 'value')]
)
def update_graph(selected_data_source, selected_account_id, kosko_status):
    if selected_data_source == 'kosko':
        dff = df_kosko[df_kosko['ID'] == selected_account_id]
        columns_to_exclude = ["ID", "TIME", "DEVICE STATUS"]
        if not kosko_status == "ONOFF":
            dff = dff[dff["DEVICE STATUS"] == kosko_status]
    elif selected_data_source == 'a2ei':
        dff = df_a2ei[df_a2ei['ID'] == selected_account_id]
        columns_to_exclude = ["ID", "TIME"]
    elif selected_data_source == 'survey':
        return go.Figure()
    else:
        dff = pd.DataFrame()
        columns_to_exclude = []
        

    columns = [col for col in dff.columns if col not in columns_to_exclude]
    subplot = plot_ts(dff,columns,selected_data_source,kosko_status)
    
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
        return "Click on a marker to learn more about the location."
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        return html.P(f"Information about {button_id}: [Replace this with actual information about {button_id}]")

if __name__ == '__main__':
    app.run_server(debug=True)
