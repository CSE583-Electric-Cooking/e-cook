"""
PLaceholder module docustrings
"""
from plotly.subplots import make_subplots
import plotly.graph_objs as go

class PlotTimeSeries:
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
            font={'color':'white'},
        )
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
            t_data = self.dff["TIME"][self.dff[col] != 0]
            y_data = self.dff[col][self.dff[col] != 0]
            fig.add_trace(
                go.Scatter(x=t_data, y=y_data, mode='lines', name=col,
                        line=dict(width=2), marker=dict(size=1)),
                row=i, col=1
            )
        return fig

    def __getattr__(self, name):
        if name.startswith("kosko"):
            def method(fig, col, i):
                return self.kosko(fig, col, i)
            return method
        if name.startswith("a2ei"):
            def method(fig, col, i):
                return self.a2ei(fig, col, i)
            return method
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

class PlotSurvey:
    def __init__(self, dff, survey_selection):
        self.dff = dff[dff["community_name"] == survey_selection]
        self.groups = sorted(set(col.split("/")[0] for col in self.dff.columns if "/" in col))
        columns = self.dff.columns
        def column_func(group):
            return [col for col in columns if col.startswith(group + "/")]
        self.grouped_data = {group: self.dff[column_func(group)] for group in self.groups}

    def dash_plot(self):
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
        if (data == 0).all().all():
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
