from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
from process_kosko import Kosko
from process_a2ei import A2EI
import pandas as pd

# Initialize your data
kosko = Kosko()  
a2ei = A2EI()    

df_kosko = kosko.df
df_a2ei = a2ei.df

# Initialize Dash app
app = Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(
        id='data-source-selection',
        options=[
            {'label': 'Kosko', 'value': 'kosko'},
            {'label': 'A2EI', 'value': 'a2ei'}
        ],
        value='kosko'  # Default value
    ),
    
    dcc.Dropdown(
        id='dropdown-selection',
        # The options will be updated based on the data source selection
    ),
    dcc.Graph(id='graph-content')
])


@callback(
    Output('dropdown-selection', 'options'),
    [Input('data-source-selection', 'value')]
)
def update_dropdown_options(selected_data_source):
    if selected_data_source == 'kosko':
        return [{'label': i, 'value': i} for i in df_kosko['ID'].unique()]
    elif selected_data_source == 'a2ei':
        return [{'label': i, 'value': i} for i in df_a2ei['ID'].unique()]
    else:
        return []


@callback(
    Output('graph-content', 'figure'),
    [Input('data-source-selection', 'value'), Input('dropdown-selection', 'value')]
)

def update_graph(selected_data_source, selected_account_id):
    if selected_data_source == 'kosko':
        dff = df_kosko[df_kosko['ID'] == selected_account_id]
    elif selected_data_source == 'a2ei':
        dff = df_a2ei[df_a2ei['ID'] == selected_account_id]
    else:
        dff = pd.DataFrame()
    return px.line(dff, x='TIME', y='VOLTAGE')  # Ensure these columns exist in both DataFrames

if __name__ == '__main__':
    app.run_server(debug=True)
