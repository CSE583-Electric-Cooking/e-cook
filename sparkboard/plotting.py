"""
This file provides an object oriented structure for the generation of plots to be embedded
into the dashboard.py framework. Two classes are defined as such:

    PlotTimeSeries: Class to generate time series plots
    PlotSurvey: Class to generate bar graphs of filtered survey data


Depencies:
    plotly.subplots: Framework to make complex multi layer figures
    plotly.graph_objs: Framework to populate subplots with either time series or bar graphs

For example usage see dashboard.py
"""
from plotly.subplots import make_subplots
import plotly.graph_objs as go

class PlotTimeSeries:
    """
    This class is designed to create time series plots for different data sources using Plotly.

    __init__:
        Constructs with the following objects:

        dff (DataFrame): The pandas DataFrame containing the time series data.
        columns (list): A list of column names from the DataFrame to be plotted.
        selected_data_source (str): A string representing the selected data source ('kosko'/'a2ei').
        kosko_logic (bool): A boolean representing specific logic for the 'kosko' data source.

    __getattr__:
        String based logic on input to correctly navigate to either the generic kosko or ae2i plot
    
        name (string): Input for get attribute

    Inheritance: None
    """
    def __init__(self,dff,columns,selected_data_source, kosko_status):
        self.dff = dff
        self.columns = columns
        self.selected_data_source = selected_data_source
        self.kosko_logic = kosko_status != "ONOFF"

    def dash_plot(self):
        """
        Generates a Plotly subplot for time series data.

        Returns:
            go.Figure: A Plotly figure object containing the generated subplot.
        """
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
            font={'color':'white'},
        )
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#444')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#444')
        return fig

    def kosko(self, fig, col, i):
        """
        Adds time series traces specific to the 'kosko' data source to the provided figure.

        Args:
            fig (go.Figure): The Plotly figure object to which traces are added.
            col (str): The name of the column to plot.
            i (int): The index representing the row position in the subplot layout.

        Returns:
            go.Figure: The updated figure with 'kosko' specific traces added.
        """
        if self.kosko_logic:
            fig.add_trace(
                go.Scatter(x=self.dff["TIME"], y=self.dff[col], mode='lines', name=col,
                        line={"width": 2}, marker={"size": 1}),
                row=i, col=1
            )
        else:
            t_on = self.dff["TIME"][self.dff["DEVICE STATUS"] == "OFF"]
            y_on = self.dff[col][self.dff["DEVICE STATUS"] == "OFF"]
            fig.add_trace(
                go.Scatter(x=t_on, y=y_on, mode='lines', name=f"{col} OFF",
                        line={"width": 2}, marker={"size": 1}),
                row=i, col=1
            )
            t_off = self.dff["TIME"][self.dff["DEVICE STATUS"] == "ON"]
            y_off = self.dff[col][self.dff["DEVICE STATUS"] == "ON"]
            fig.add_trace(
                go.Scatter(x=t_off, y=y_off, mode='lines', name=f"{col} ON",
                        line={"width": 2}, marker={"size": 1}),
                row=i, col=1
            )
        return fig

    def a2ei(self,fig,col,i):
        """
        Adds time series traces specific to the 'a2ei' data source to the provided figure.

        Args:
            fig (go.Figure): The Plotly figure object to which traces are added.
            col (str): The name of the column to plot.
            i (int): The index representing the row position in the subplot layout.

        Returns:
            go.Figure: The updated figure with 'a2ei' specific traces added.
        """
        if col != "POWER FACTOR":
            fig.add_trace(
                go.Scatter(x=self.dff["TIME"], y=self.dff[col], mode='lines', name=col,
                        line={"width": 2}, marker={"size": 1}),
                row=i, col=1
            )
        else:
            t_data = self.dff["TIME"][self.dff[col] != 0]
            y_data = self.dff[col][self.dff[col] != 0]
            fig.add_trace(
                go.Scatter(x=t_data, y=y_data, mode='lines', name=col,
                        line={"width": 2}, marker={"size": 1}),
                row=i, col=1
            )
        return fig

    def __getattr__(self, name):
        if name.startswith("kosko"):
            def method_kosko(fig, col, i):
                return self.kosko(fig, col, i)
            return method_kosko
        if name.startswith("a2ei"):
            def method_ae2i(fig, col, i):
                return self.a2ei(fig, col, i)
            return method_ae2i
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

class PlotSurvey:
    """
    This class is designed for creating survey data plots using Plotly.

    __init__:
        Constructs with the following objects:

        dff (DataFrame): The pandas DataFrame containing the survey data.
        groups (list): A list of groups/categories identified in the survey data.
        grouped_data (dict): A dictionary grouping the survey data by categories.
    """
    def __init__(self, dff, survey_selection):
        self.dff = dff[dff["community_name"] == survey_selection]
        self.groups = sorted(set(col.split("/")[0] for col in self.dff.columns if "/" in col))
        columns = self.dff.columns
        def column_func(group):
            return [col for col in columns if col.startswith(group + "/")]
        self.grouped_data = {group: self.dff[column_func(group)] for group in self.groups}

    def dash_plot(self):
        """
        Generates a Plotly subplot for survey data.

        Returns:
            go.Figure: A Plotly figure object containing the generated subplot for the survey data.
        """
        fig = make_subplots(rows=len(self.grouped_data),
                            cols=1,
                            subplot_titles=[g.capitalize() for g in self.groups])
        background_color = '#282828'
        paper_color = '#343a40'
        for i, (_, data) in enumerate(self.grouped_data.items(), start=1):
            self.bar_graph(fig,data,i)
        fig.update_layout(
            height=300 * len(self.grouped_data),
            showlegend=False,
            plot_bgcolor=background_color,
            paper_bgcolor=paper_color,
            font=dict(color='white')
        )
        return fig

    def bar_graph(self,fig,data,i):
        """
        Adds bar graph to the provided subplot for a specific survey data group.

        Args:
            fig (go.Figure): The Plotly figure object to which bar plot traces are added.
            data (DataFrame): The pandas DataFrame containing data for the specific survey group.
            i (int): The index representing the row position in the subplot layout.

        Returns:
            go.Figure: The updated figure with bar plot traces added for the survey group.
        """
        if (data == 0).all().all(): # Logical check, displays an empty bar graph
            fig.add_trace(
                go.Bar(x=[], y=[], name="No Data"),
                row=i, col=1
            )
            fig.update_xaxes(showticklabels=False, row=i, col=1)
            fig.update_yaxes(showticklabels=False, row=i, col=1)
        else:
            for col in data.columns:
                simple_col = col.split("/")[-1]
                if simple_col == "a2ei":
                    simple_col = simple_col.upper()
                y_data = [data[col].values[0]]
                if sum(y_data) > 0:
                    fig.add_trace(
                        go.Bar(x=[simple_col.replace("_", " ").capitalize()],
                               y=y_data, name=simple_col),
                        row=i, col=1
                        )
        return fig
