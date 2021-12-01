import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
from dash import Dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go  # pip install dash (version 2.0.0 or higher)
from django_plotly_dash import DjangoDash


app = DjangoDash("Tuition")


# -- Import our data into the code as a panda data frame.
df = pd.read_csv("https://raw.githubusercontent.com/chrisgbradley/itsc-3155-final-group-2/main/AdmissionsData.csv")

# -- Our data is technically already "clean" due to how we formatted it in excel (thanks Christian).

# -- Needed variables for page formatting.

# Not to be confused with YEAR from our data CSV
YEARS = [1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019]


# -- Test print, if needed.
# print(df[:40])

# -------------------------------------------------------------------------------------------------------------------

# -- App Layout
app.layout = html.Div([

    # - HTML core components = 'html.'
    # - Dash core components = 'dcc.'

    html.H1("Test In State Tuition Graph", style={'text-align': 'center'}),

#   html.Div(
#        id="dropdown-container",
#        children=[
#            html.P(
#                id="dropdown-text",
#               children="Select whether you want In State or Out of State Tution",
#            ),
#            dcc.Dropdown(
#                id="in-or-out",
#                options=[
#                    {'label' : 'In State Tuition', 'value' : "TUITION_IN"},
#                    {'label' : 'Out of State Tuition', 'value' : "TUITION_OUT"},
#                ],
#                value='TUITION_IN',
#                multi=False
#            ),
#        ],
#    ),

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

    dcc.Graph(id='in_tuition_map', figure={}),
    dcc.Graph(id='out_tuition_map', figure={})
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
     Output(component_id='in_tuition_map', component_property='figure')],
    [Input(component_id='years-slider', component_property='value')]
)

def update_in_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "The year chosen by user was: {}".format(option_slctd)

    dff = df.copy()
    dff = dff[dff["YEAR"] == option_slctd]

    fig = px.choropleth(
        data_frame=dff,
        locationmode='USA-states',
        locations='STATE',
        scope="usa",
        color='TUITION_IN',
        hover_data=['STATE', 'TUITION_IN'],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        labels={'TUITION_IN': 'Average In State Tuition'},
        template='plotly_dark'
    )

    return container, fig

@app.callback(
    [Output(component_id='out_tuition_map', component_property='figure')],
    [Input(component_id='years-slider', component_property='value')]
)

def update_out_graph(YEARS):

    dff_out = df.copy()
    dff_out = dff_out[dff_out["YEAR"] == YEARS]

    fig = px.choropleth(
        data_frame=dff_out,
        locationmode='USA-states',
        locations='STATE',
        scope="usa",
        color='TUITION_OUT',
        hover_data=['STATE', 'TUITION_OUT'],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        labels={'TUITION_OUT': 'Average Out of State Tuition'},
        template='plotly_dark'
    )

    return fig


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)