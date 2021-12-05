import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
from dash import Dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go  # pip install dash (version 2.0.0 or higher)
from django_plotly_dash import DjangoDash

app = DjangoDash(name="completion_rate")


# -- Import our data into the code as a panda data frame.
df = pd.read_csv("https://raw.githubusercontent.com/chrisgbradley/itsc-3155-final-group-2/main/data/Tuition-CSV.csv")

# -- Our data is technically already "clean" due to how we formatted it in excel (thanks Christian).

# -- Needed variables for page formatting.

# Not to be confused with YEAR from our data CSV
YEARS = [2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019]


# -- Test print, if needed.
# print(df[:40])
