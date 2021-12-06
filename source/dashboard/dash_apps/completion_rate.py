import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
from dash import Dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from django_plotly_dash import DjangoDash

app = DjangoDash(name='completion_rate')   # replaces dash.Dash
# -- Import our data into the code using raw git hub link
df = pd.read_csv("https://raw.githubusercontent.com/chrisgbradley/itsc-3155-final-group-2/main/data/Completion-CSV.csv")
# -- Creation of variable YEARS to be used in slider
YEARS = [2019]

def change(layout): # -- Styling
    # print(layout)
    # print(layout.template)
    modified_layout = layout
    modified_layout.yaxis = dict(range=[0.3,.8], tickformat=".2%")
    modified_layout.height = 600
    modified_layout.plot_bgcolor = 'rgb(54, 54, 64)'
    modified_layout.paper_bgcolor = 'rgb(81, 81, 89)'
    modified_layout.font.color = 'rgb(255, 255, 255)'

    return modified_layout


fig = px.bar(df, x='STATE', y='AVG_COMP_R', hover_data=['NUM_OF_UNI'])

fig.layout = change(fig.layout)
fig.update_traces(marker_color='#73d1c1')

# -- App Layout
app.layout = html.Div([

    dcc.Graph(id='completion_graph', figure=fig)

])

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)