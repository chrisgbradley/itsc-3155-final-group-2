import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
from django_plotly_dash import DjangoDash

app = DjangoDash('MF4YR')   # replaces dash.Dash

# -- Import our data into the code using raw git hub link
df = pd.read_csv("https://raw.githubusercontent.com/dgrant28/hello-world/main/MFdata.csv")
# -- Creation of variable YEARS to be used in slider
YEARS = [2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017]

# -- App Layout
app.layout = html.Div([

    # -- HTML header for title.
    html.H1("Average Number of Students Graduating in 4 years per School by State from 2001-2017 ",
            style={'text-align': 'center'}),

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

    dcc.Graph(id='my_stack_map', figure={})

])


# ------------------------------------------------------------------------------

# Connect the Plotly graphs with Dash Components

# - The callback is what connects everything. Without the callback all you have is some interactive Dash components
# that don't do anything, and a pretty looking graph that can't change.

# - Here we have 2 outputs and 1 input. The output container is simply anything on the page that isn't a graph. The my
# bee map is for containing our plotly graph. The input is the users selected year. This will be changeable through the
# dropdown component.

@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='my_stack_map', component_property='figure')],
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
    # -- Groups the two columns
    new_df = dff.groupby(['STATE']).agg({'AVG_FEM_YR4': 'sum', 'AVG_MAL_YR4': 'sum'}).reset_index()
    # -- Creates two different traces for the columns
    trace1 = go.Bar(x=new_df['STATE'], y=new_df['AVG_FEM_YR4'], name='Females', marker={'color': 'purple'})
    trace2 = go.Bar(x=new_df['STATE'], y=new_df['AVG_MAL_YR4'], name='Males', marker={'color': 'teal'})
    # -- Combines the two traces
    data = [trace1, trace2]
    # -- Creates style of chart
    layout = go.Layout(
        barmode='stack',
    )
    # -- Creates actual chart
    fig = go.Figure(data=data, layout=layout)
    # -- Returns slider and chart
    return container, fig

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
