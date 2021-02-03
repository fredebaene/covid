# IMPORTING LIBRARIES
# ----------------------------------------------------------------------------------------------------
import pandas as pd
import plotly
import plotly.express as px

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

# READING DATA
# ----------------------------------------------------------------------------------------------------
data = pd.read_csv('COVID19BE_tests.csv')
data.dropna(axis=0, how='any', inplace=True)
data['DATE'] = pd.to_datetime(data['DATE'], format='%Y-%m-%d')
data['PCT_TESTS_POS'] = (data['TESTS_ALL_POS'] / data['TESTS_ALL']) * 100

# APP LAYOUT
# ----------------------------------------------------------------------------------------------------
app.layout = html.Div([

    dcc.Dropdown(

        id='selected_province',

        options=[
            {'label' : 'Antwerpen', 'value' : 'Antwerpen'},
            {'label' : 'Oost-Vlaanderen', 'value' : 'OostVlaanderen'},
            {'label' : 'Vlaams-Brabant', 'value' : 'VlaamsBrabant'},
            {'label' : 'Limburg', 'value' : 'Limburg'},
            {'label' : 'West-Vlaanderen', 'value' : 'WestVlaanderen'},
            {'label' : 'Hainaut', 'value' : 'Hainaut'},
            {'label' : 'Liège', 'value' : 'Liège'},
            {'label' : 'Luxembourg', 'value' : 'Luxembourg'},
            {'label' : 'Namur', 'value' : 'Namur'},
            {'label' : 'Brabant Wallon', 'value' : 'BrabantWallon'},
            {'label' : 'Brussels', 'value' : 'Brussels'}
        ],

        optionHeight=35,
        searchable=True,
        clearable=True,
        placeholder='Select Province'

    ),

    dcc.Graph(

        id='graph'

    )

])

# CALLBACK
# ----------------------------------------------------------------------------------------------------
@app.callback(
    Output(component_id='graph', component_property='figure'),
    Input(component_id='selected_province', component_property='value')
)

def update_graph(selected_province):

    if selected_province is None:

        data_copy = data

        fig_positive_rate_by_day = px.line(

            data_frame=data_copy,
            x='DATE',
            y='PCT_TESTS_POS',
            title='Positive Rate by Date',
            labels={'DATE' : 'Date', 'PCT_TESTS_POS' : 'Positive Rate', 'PROVINCE' : 'Province'},
            line_group='PROVINCE',
            color='PROVINCE',
            range_y=[0, 75]

        )

    else:

        data_copy = data[data['PROVINCE'] == selected_province]

        fig_positive_rate_by_day = px.line(

            data_frame=data_copy,
            x='DATE',
            y='PCT_TESTS_POS',
            title='Positive Rate by Date',
            labels={'DATE' : 'Date', 'PCT_TESTS_POS' : 'Positive Rate', 'PROVINCE' : 'Province'},
            range_y=[0, 75]

        )

    return (fig_positive_rate_by_day)

# APPLICATION
# ----------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
