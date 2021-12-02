import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
from dash import Dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go  # pip install dash (version 2.0.0 or higher)
from django_plotly_dash import DjangoDash


app = DjangoDash(name="Tuition")


# -- Import our data into the code as a panda data frame.
df = pd.read_csv("https://raw.githubusercontent.com/chrisgbradley/itsc-3155-final-group-2/main/data/Tuition-CSV.csv")

# -- Our data is technically already "clean" due to how we formatted it in excel (thanks Christian).

# -- Needed variables for page formatting.

# Not to be confused with YEAR from our data CSV
YEARS = [2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019]


# -- Test print, if needed.
# print(df[:40])

# -------------------------------------------------------------------------------------------------------------------

plotly_layout = go.Layout(
    paper_bgcolor='rgb(81, 81, 89, 1)', plot_bgcolor='rgb(54, 54, 64, 1)'
)

# -- App Layout
app.layout = html.Div([

    # - HTML core components = 'html.'
    # - Dash core components = 'dcc.'

    html.H1("Test In State Tuition Graph", style={'text-align': 'center'}),

    html.Div(
        id="slider-container",
        children=[
            html.P(
                id="slider-text",
                children="Drag the slider to change the year:",
            ),
            dcc.Slider(
                id="years",
                min=min(YEARS),
                max=max(YEARS),
                value=min(YEARS),
                marks={
                    str(year): {
                        "label": str(year),
                        "style": {
                            "color": "#009688",
                            # "font-size": "20px",
                            # "font-family": "Roboto, Sans-Serif"
                        },
                    }
                    for year in YEARS
                },
                included=False
            ),
        ],
    ),

    html.Div(id='tabs', children=[
        # dcc.Graph(id='in_tuition_map', figure={}),
        # dcc.Graph(id='out_tuition_map', figure={})
        dcc.Tabs(id="in-out-tabs", value="in-state", children=[
            dcc.Tab(label="In-State Tuition", value="in-state"),
            dcc.Tab(label="Out-Of-State Tuition", value="out-state")
        ])
    ]),

    html.Br(),

    html.Div(id="tab-graph-output")
])

# ------------------------------------------------------------------------------

# Connect the Plotly graphs with Dash Components

# - The callback is what connects everything. Without the callback all you have is some interactive Dash components
# that don't do anything, and a pretty looking graph that can't change.

# - Here we have 2 outputs and 1 input. The output contianer is simply anything on the page that isn't a graph. The my
# bee map is for containing our plotly graph. The input is the users selected year. This will be changeable through the
# dropdown component.


def change(layout):
    # print(layout)
    # print(layout.template)
    modified_layout = layout
    modified_layout.height = 720
    modified_layout.width = 1320
    modified_layout.plot_bgcolor = 'rgb(54, 54, 64)'
    modified_layout.paper_bgcolor = 'rgb(81, 81, 89)'
    modified_layout.font.color = 'rgb(255, 255, 255)'
    modified_layout.coloraxis.colorscale = [
        [0.0,   '#ffffff'],
        [0.125, '#ccf8ee'],
        [0.25,  '#a9ecdf'],
        [0.375, '#8ddfd0'],
        [0.5,   '#73d1c1'],
        [0.625, '#5bc2b2'],
        [0.75,  '#43b4a4'],
        [0.875, '#2aa596'],
        [1.0,   '#009688'],
    ]
    modified_layout.geo.bgcolor = 'rgb(54, 54, 64)'
    modified_layout.geo.lakecolor = 'rgb(54, 54, 64)'

    return modified_layout


@app.callback(Output('tab-graph-output', 'children'),
              [Input('in-out-tabs', 'value'),
               Input('years', 'value')])
def render_content(tab, year):
    dff = df.copy()
    dff = dff[dff["YEAR"] == year]

    if tab == 'in-state':

        fig_in = px.choropleth(
            data_frame=dff,
            locationmode='USA-states',
            locations='STATE',
            scope="usa",
            color='TUITION_IN',
            hover_data=['STATE', 'TUITION_IN'],
            color_continuous_scale=px.colors.sequential.YlOrRd,
            labels={'TUITION_IN': 'Avg In-State Tuition'},
        )

        fig_in.layout = change(fig_in.layout)

        return html.Div([
            html.H3('In-State Tuition'),
            dcc.Graph(id='in-state-graph',
                      figure=fig_in)
        ])
    elif tab == 'out-state':

        fig_out = px.choropleth(
            data_frame=dff,
            locationmode='USA-states',
            locations='STATE',
            scope="usa",
            color='TUITION_OUT',
            hover_data=['STATE', 'TUITION_OUT'],
            color_continuous_scale=px.colors.sequential.YlOrRd,
            labels={'TUITION_OUT': 'Avg Out-of-State Tuition'},
        )

        fig_out.layout = change(fig_out.layout)

        return html.Div([
            html.H3('In-State Tuition'),
            dcc.Graph(id='in-state-graph',
                      figure=fig_out)
        ])


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)