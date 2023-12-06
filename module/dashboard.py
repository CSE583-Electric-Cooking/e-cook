from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
from process_kosko import Kosko
from process_a2ei import A2EI
from plotly.subplots import make_subplots
import plotly.graph_objs as go
import pandas as pd

# Initialize your data
kosko = Kosko()  
a2ei = A2EI()

class plotting:

    def __init__(self):
        pass

    def data_query(self):
        pass

    def kosko_voltage(self): 
        pass
    
    def kosko_current(self):
        pass

    def kosko_current(self):
        pass


df_kosko = kosko.df
df_a2ei = a2ei.df

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1('Spark-Board', style={'color': '#ffffff', 'textAlign': 'center', 'background': '#343a40', 'padding': '10px', 'margin-bottom': '10px'}),
    
    html.Div([
        dcc.Dropdown(
            id='data-source-selection',
            options=[
                {'label': 'Kosko', 'value': 'kosko'},
                {'label': 'A2EI', 'value': 'a2ei'}
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

    ], style={'padding': '10px', 'width': '30%', 'display': 'inline-block'}),
    
    html.Div(
        dcc.Graph(id='graph-content'),
        id='graph-container'  
    )
], style={'backgroundColor': '#282828', 'padding': '50px', 'color': '#FFF'})


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
    else:
        dff = pd.DataFrame()
        columns_to_exclude = []

    columns = [col for col in dff.columns if col not in columns_to_exclude]

    num_cols = len(columns)
    fig = make_subplots(rows=num_cols, cols=1, subplot_titles=columns)
    background_color = '#282828'  # Dark gray to match your app's background
    paper_color = '#343a40'       # Slightly lighter gray for the figure's background
    
    
    for i, col in enumerate(columns, start=1):
        fig.add_trace(
            go.Scatter(x=dff["TIME"], y=dff[col], mode='markers+lines', name=col,
                    line=dict(width=2), marker=dict(size=1)),
            row=i, col=1
        )


        
    sensor = selected_data_source.capitalize()
    if selected_data_source == "a2ei": 
        sensor = sensor.upper()

    
    fig.update_layout(

        title_text= f"{sensor} Energy Report",
        height=300*num_cols,
        plot_bgcolor=background_color,
        paper_bgcolor=paper_color,
        font=dict(color='white'),  # Set the font color to white
    )
    
    # Optionally, you can also set the grid color to be more subtle
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#444')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#444')
    
    return fig

@app.callback(
    Output('device-on-off', 'style'),
    [Input('data-source-selection', 'value')]
)
def show_hidden_dropdown(selected_data_source):
    if selected_data_source == 'kosko':
        return {'background': '#333'}  # Show the dropdown
    else:
        return {'display': 'none'}  # Hide the dropdown
    
if __name__ == '__main__':
    app.run_server(debug=True)
