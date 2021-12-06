import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from django_plotly_dash import DjangoDash

app = DjangoDash('acceptance_rate')   # replaces dash.Dash

# -- Import our data into the code using raw git hub link
df = pd.read_csv("https://raw.githubusercontent.com/dgrant28/hello-world/main/AdmissionsData.csv")
# -- Creation of variable YEARS to be used in slider
YEARS = [2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018,
         2019]

# -- App Layout
app.layout = html.Div([
    html.Div(
        id="slider-container",
        children=[
            html.P(
                id="slider-text",
                children="Drag the slider to change the year:",
                style={'color': '#fff'},
            ),
            dcc.Slider(
                id="years-slider",
                min=min(YEARS),
                max=max(YEARS),
                value=min(YEARS),
                marks={
                    str(year): {
                        "label": str(year),
                        "style": {
                            "color": "#009688",
                            "font-size": "16px",
                            "font-family": "Roboto, Sans-Serif",
                            "padding-top": "15px",
                        },
                    }
                    for year in YEARS
                },
                className='dash_app_slider',
                included=False
            ),
        ],
        style={
            'margin': '32px 0',
        }
    ),

    html.Div(id='output_container', children=[]),

    dcc.Graph(id='acceptance_bar', figure={}),
    dcc.Graph(id='acceptance_choropleth', figure={})

])
# ------------------------------------------------------------------------------

# Connect the Plotly graphs with Dash Components

# - The callback is what connects everything. Without the callback all you have is some interactive Dash components
# that don't do anything, and a pretty looking graph that can't change.

# - Here we have 2 outputs and 1 input. The output contianer is simply anything on the page that isn't a graph. The my
# bee map is for containing our plotly graph. The input is the users selected year. This will be changeable through the
# dropdown component.

def change(layout): # -- Styling
    print(layout)
    print(layout.template)
    modified_layout = layout
    modified_layout.height = 600
    modified_layout.plot_bgcolor = 'rgb(54, 54, 64)'
    modified_layout.paper_bgcolor = 'rgb(81, 81, 89)'
    modified_layout.font.color = 'rgb(255, 255, 255)'
    modified_layout.yaxis = dict(range=[0.5, 1])
    modified_layout.coloraxis.colorscale = [
        [0.0, '#ffffff'],
        [0.125, '#ccf8ee'],
        [0.25, '#a9ecdf'],
        [0.375, '#8ddfd0'],
        [0.5, '#73d1c1'],
        [0.625, '#5bc2b2'],
        [0.75, '#43b4a4'],
        [0.875, '#2aa596'],
        [1.0, '#009688'],
    ]
    modified_layout.geo.bgcolor = 'rgb(54, 54, 64)'
    modified_layout.geo.lakecolor = 'rgb(54, 54, 64)'

    return modified_layout

@app.callback(
     [Output(component_id='acceptance_bar', component_property='figure'),
      Output(component_id='acceptance_choropleth', component_property='figure')],
    [Input(component_id='years-slider', component_property='value')]
)
# -- Takes user selection as its field
def update_graph(option_slctd):
    # print(option_slctd)
    # print(type(option_slctd))

    dff = df.copy()
    # -- Selects the correct year in the data based off what the user selects
    dff = dff[dff["YEAR"] == option_slctd]

    fig_bar = px.bar(
        data_frame=dff,
        x='STATE',
        y='AVG_ADM_RATE',
    )

    fig_bar.layout = {
        'xaxis': {
            'categoryorder': 'total descending'
        }
    }

    fig_bar.update_traces(marker_color='#009688')

    fig_bar.layout = change(fig_bar.layout)

    # -- Create actual chart
    fig_choropleth = px.choropleth(
        data_frame=dff,
        locationmode='USA-states',
        locations='STATE',
        scope="usa",
        color='AVG_ADM_RATE',
        hover_data=['STATE', 'AVG_ADM_RATE'],
        color_continuous_scale=px.colors.sequential.YlGn,
        labels={'AVG_ADM_RATE': 'Average Acceptance Rate'},
    )

    fig_choropleth.layout = change(fig_choropleth.layout)
    # -- Return slider and chart
    return fig_bar, fig_choropleth
