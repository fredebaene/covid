# COVID-19 - NUMBER OF PERFORMED AND POSITIVE TESTS BY PROVINCE AND DATE
# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------

# IMPORTING LIBRARIES
# ----------------------------------------------------------------------------------------------------
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
import plotly
import plotly.express as px
from datetime import date
from datetime import datetime

# READING DATA
# ----------------------------------------------------------------------------------------------------
data = pd.read_csv('../data/covid19be_hosp.csv')
data.dropna(subset=['DATE'], inplace=True)
data['DATE'] = pd.to_datetime(data['DATE'])

for i in ['REGION', 'PROVINCE']:
    data[i].fillna('NA', inplace=True)

# APP LAYOUT
# ----------------------------------------------------------------------------------------------------
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SOLAR])

content = dbc.Container([

    dbc.Row([

        dbc.Col([

            html.P([
                'Data Source : Sciensano // Powered by : Python - Plotly - Dash // Produced by : fdeba'
            ], style={'font-size' : '12px'}),

        ], width={'size' : 12}),

    ], style={'margin-bottom' : '12px'}),

    dbc.Row([

        dbc.Col([

            dcc.Dropdown(

                id='dd_province',
                placeholder='Select Province',
                clearable=True,
                searchable=True,
                multi=True,
                value=[],
                options=[{'label' : i, 'value' : i} for i in sorted(data['PROVINCE'].unique())]

            ),

        ], width={'size' : 12}),

    ], style={'margin-bottom' : '12px'}),

    dbc.Row([

        dbc.Col([

            dcc.Graph(id='intakes-by-date'),

        ], width={'size' : 6}),

        dbc.Col([

            dcc.Graph(id='discharges-by-date'),

        ], width={'size' : 6}),

    ], style={'margin-bottom' : '12px'}),

], fluid=True)

app.layout = html.Div([content])

# CALLBACK
# ----------------------------------------------------------------------------------------------------
@app.callback(
    # OUTPUT
    [
        Output('intakes-by-date', 'figure'),
        Output('discharges-by-date', 'figure')
    ],
    # INPUT
    [
        Input('dd_province', 'value')
    ]
)

def update_graphs(selected_provinces):

    data_copy = data.copy()

    if len(selected_provinces) == 0:

        data_copy_by_date = data_copy.groupby(by=pd.Grouper(key='DATE', freq='D'))[['NEW_IN', 'NEW_OUT']].sum().reset_index()

        fig_intakes_by_date = px.line(

            data_frame=data_copy_by_date,
            x='DATE',
            y='NEW_IN'

        )

        fig_discharges_by_date = px.line(

            data_frame=data_copy_by_date,
            x='DATE',
            y='NEW_OUT'

        )

        return fig_intakes_by_date, fig_discharges_by_date

    else:

        data_copy = data_copy[data_copy['PROVINCE'].isin(selected_provinces)]
        data_copy_by_date = data_copy.groupby(by=[pd.Grouper(key='DATE', freq='D'), 'PROVINCE'])[['NEW_IN', 'NEW_OUT']].sum().reset_index()

        fig_intakes_by_date = px.line(

            data_frame=data_copy_by_date,
            x='DATE',
            y='NEW_IN',
            color='PROVINCE'

        )

        fig_discharges_by_date = px.line(

            data_frame=data_copy_by_date,
            x='DATE',
            y='NEW_OUT',
            color='PROVINCE'

        )

        return fig_intakes_by_date, fig_discharges_by_date

# APPLICATION
# ----------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
