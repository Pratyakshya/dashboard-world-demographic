import dash                     # pip install dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px     # pip install plotly==5.2.2

import pandas as pd             # pip install pandas

df = pd.read_csv("wdi_wide.csv")
df = df.dropna(subset=['Region'])
print(df.info())


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div([
    html.H1("Analytics Dashboard of World Demographic Indicators Extract (Dash Plotly)", style={"textAlign":"center"}),
    html.Hr(),
    html.P("Choose the Region of Interest:"),
    html.Div(html.Div([
        dcc.Dropdown(id='region-type', clearable=False,
                     value="Asia",
                     options=[{'label': x, 'value': x} for x in
                              df["Region"].unique()]),
    ],className="two columns"),className="row"),

    html.Div(id="output-div", children=[]),
])


@app.callback(Output(component_id="output-div", component_property="children"),
              Input(component_id="region-type", component_property="value"),
)
def make_graphs(region_chosen):
    # HISTOGRAM
    df_hist = df[df["Region"]==region_chosen]
    fig_hist = px.histogram(df_hist, x="Internet use")
    fig_hist.update_xaxes(categoryorder="total descending")

    # STRIP CHART
    fig_strip = px.strip(df_hist, x="Physicians", y="Tertiary education, female")

    # AREA CHART
    fig_area = px.area(df_hist, x="International tourism", y="Internet use", color="Subregion",line_group="Country Name")

    # SCATTER CHART
    fig_scatter = px.scatter(df_hist, x="GNI", y="Life expectancy, male",
	                size="Population", color="Subregion",
                 hover_name="Country Name", log_x=True, size_max=60)

    # LINE CHART
    df_line = df.sort_values(by=["High Income Economy"], ascending=True)
    df_line = df_line.groupby(
        ["High Income Economy", "Region"]).size().reset_index(name="count")
    fig_line = px.line(df_line, x="High Income Economy", y="count",
                       color="Region", markers=True)

    return [
        html.Div([
            html.Div([dcc.Graph(figure=fig_hist)], className="six columns"),
            html.Div([dcc.Graph(figure=fig_strip)], className="six columns"),
        ], className="row"),
        html.Div([
            html.Div([dcc.Graph(figure=fig_area)], className="six columns"),
            html.Div([dcc.Graph(figure=fig_scatter)], className="six columns"),
        ], className="row"),
        html.H2("All Regions", style={"textAlign":"center"}),
        html.Hr(),
        html.Div([
            html.Div([dcc.Graph(figure=fig_line)], className="twelve columns"),
        ], className="row"),
    ]


if __name__ == '__main__':
    app.run_server(debug=True)
