import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
from dash import Dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash

app = DjangoDash('AccRate')   # replaces dash.Dash
# -- Import our data into the code using raw git hub link
df = pd.read_csv("https://raw.githubusercontent.com/dgrant28/hello-world/main/AdmissionsData.csv")
# -- Creation of variable YEARS to be used in slider
YEARS = [2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018,
         2019]

# -- App Layout
app.layout = html.Div([

    # -- HTML header for title.
    html.H1("Test Acceptance Rate", style={'text-align': 'center'}),

    html.Div(
        id="slider-container",
        children=[
            html.P(
                id="slider-text",
                children="Drag the slider to change the year:",
            ),
            dcc.Slider(
                id="years-slider",
                min=min(YEARS),
                max=max(YEARS),
                value=min(YEARS),
                marks={
                    str(year): {
                        "label": str(year),
                        "style": {"color": "#7fafdf"},
                    }
                    for year in YEARS
                },
            ),
        ],
    ),

    html.Div(id='output_container', children=[]),

    html.Br(),

    dcc.Graph(id='my_acc_map', figure={})

])
# ------------------------------------------------------------------------------

# Connect the Plotly graphs with Dash Components

# - The callback is what connects everything. Without the callback all you have is some interactive Dash components
# that don't do anything, and a pretty looking graph that can't change.

# - Here we have 2 outputs and 1 input. The output contianer is simply anything on the page that isn't a graph. The my
# bee map is for containing our plotly graph. The input is the users selected year. This will be changeable through the
# dropdown component.

@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='my_acc_map', component_property='figure')],
    [Input(component_id='years-slider', component_property='value')]
)
# -- Takes user selection as its field
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))
    # -- Output message for what year the user selects
    container = "Year: {}".format(option_slctd)

    dff = df.copy()
    # -- Selects the correct year in the data based off what the user selects
    dff = dff[dff["YEAR"] == option_slctd]

    # -- Create actual chart
    fig = px.choropleth(
        data_frame=dff,
        locationmode='USA-states',
        locations='STATE',
        scope="usa",
        color='AVG_ADM_RATE',
        hover_data=['STATE', 'AVG_ADM_RATE'],
        color_continuous_scale=px.colors.sequential.YlGn,
        labels={'AVG_ADM_RATE': 'Average Acceptance Rate'},
    )
    # -- Return slider and chart
    return container, fig
