import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
from dash import Dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from django_plotly_dash import DjangoDash

app = DjangoDash('Completion')   # replaces dash.Dash
# -- Import our data into the code using raw git hub link
df = pd.read_csv("https://raw.githubusercontent.com/chrisgbradley/itsc-3155-final-group-2/main/data/Completion-CSV.csv")
# -- Creation of variable YEARS to be used in slider
YEARS = [2019]

# -- App Layout
app.layout = html.Div([

    # -- HTML header for title.
    html.H1("Average Completion Rate by State 2019", style={'text-align': 'center'}),

    html.Div(
        id="slider-container",
        children=[
            html.P(
                id="slider-text",
                children="Only data from 2019 is available:",
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

    dcc.Graph(id='completion_graph', figure={})

])
# ------------------------------------------------------------------------------

# Connect the Plotly graphs with Dash Components

# - The callback is what connects everything. Without the callback all you have is some interactive Dash components
# that don't do anything, and a pretty looking graph that can't change.

# - Here we have 2 outputs and 1 input. The output contianer is simply anything on the page that isn't a graph. The my
# bee map is for containing our plotly graph. The input is the users selected year. This will be changeable through the
# dropdown component.
def change(layout): # -- Styling
    # print(layout)
    # print(layout.template)
    modified_layout = layout
    modified_layout.yaxis = dict(range=[0.3,.8])
    modified_layout.height = 720
    modified_layout.width = 1320
    modified_layout.plot_bgcolor = 'rgb(54, 54, 64)'
    modified_layout.paper_bgcolor = 'rgb(81, 81, 89)'
    modified_layout.font.color = 'rgb(255, 255, 255)'

    return modified_layout


@app.callback(
    [Output(component_id='output_container', component_property='children')],
    [Output(component_id='completion_graph', component_property='figure')],
    [Input(component_id='years-slider', component_property='value')]
)
# -- Takes user selection as its field
def update_graph(YEARS):
    print(YEARS)
    print(type(YEARS))
    # -- Output message for what year the user selects
    container = "Year: {}".format(YEARS)

    dff = df.copy()
    fig = px.bar(dff, x='STATE', y='AVG_COMP_R', hover_data=['NUM_OF_UNI'])

    fig.layout = change(fig.layout)
    fig.update_traces(marker_color='#73d1c1')

    # -- Return slider and chart
    return container, fig

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)