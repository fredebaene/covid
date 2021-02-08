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
data = pd.read_csv('../data/covid19be_tests.csv')
data['DATE'] = pd.to_datetime(data['DATE'], format='%Y-%m-%d')
min_date = data['DATE'].min()
max_date = data['DATE'].max()

for i in ['REGION', 'PROVINCE']:
    data[i].fillna('NA', inplace=True)

colors = {
    'Brussels' : 'maroon',
    'Antwerpen' : 'goldenrod',
    'WestVlaanderen' : 'black',
    'OostVlaanderen' : 'lightslategray',
    'Limburg' : 'mistyrose',
    'VlaamsBrabant' : 'indigo',
    'BrabantWallon' : 'orchid',
    'Hainaut' : 'navy',
    'Luxembourg' : 'chocolate',
    'Liège' : 'yellowgreen',
    'Namur' : 'coral',
    'NA' : 'orangered'
}

# APP LAYOUT
# ----------------------------------------------------------------------------------------------------
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SOLAR])

navbar = dbc.Navbar(
            children=[
                dbc.Col(dbc.NavbarBrand('COVID-19 Analysis', href='/#'), sm=3, md=2),
                dbc.Col(dbc.Nav(dbc.NavItem(dbc.NavLink('Tests', href='/tests', active='exact')), navbar=True), width='auto'),
                dbc.Col(dbc.Nav(dbc.NavItem(dbc.NavLink('Cases', href='/cases', active='exact')), navbar=True), width='auto')
            ],
            light=True,
            dark=False,
            color='light', # options : primary, light, dark
            sticky='top'
        )

content = dbc.Container([

    # CREDITS ROW
    dbc.Row([

        dbc.Col([

            html.P([
                'Data Source : Sciensano // Powered by : Python - Plotly - Dash // Produced by : fdeba'
            ], style={'font-size' : '12px'})

        ], width={'size' : 12})

    ]),

    # ROW WITH DATE RANGE PICKER
    dbc.Row([

        dbc.Col([

            dcc.DatePickerRange(

                id='dpr',
                min_date_allowed=min_date,
                max_date_allowed=max_date,
                clearable=True,
                display_format='DD/MM/YYYY',
                minimum_nights=1,
                initial_visible_month=max_date

            )

        ], width={'size' : 12})

    ]),

    # ROW WITH PROVINCE DROPDOWN
    dbc.Row([

        # ROW 3 - COL 1
        dbc.Col([

            dcc.Dropdown(

                id='dd_province',
                options=[{'label' : i, 'value' : i} for i in sorted(data['PROVINCE'].unique())],
                clearable=True,
                multi=True,
                searchable=True,
                value=[],
                className='my-2',
                placeholder='Select Province'

            )

        ], width={'size' : 12})

    ]),

    # FIRST ROW WITH TWO GRAPHS
    dbc.Row([

        dbc.Col([

            dcc.Graph(id='tests-by-day', figure={}, className='my-2'),

        ], width={'size' : 6}),

        dbc.Col([

            dcc.Graph(id='pos-tests-by-day', figure={}, className='my-2'),

        ], width={'size' : 6}),

    ]),

    # SECOND ROW WITH TWO GRAPHS
    dbc.Row([

        dbc.Col([

            dcc.Graph(id='pos-rate-by-day', figure={}, className='my-2')

        ], width={'size' : 6}),

        dbc.Col([

            dcc.Graph(id='pos-rate-by-week', figure={}, className='my-2')

        ], width={'size' : 6})

    ]),

], fluid=True)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    content
])

# CALLBACK
# ----------------------------------------------------------------------------------------------------
@app.callback(
    # OUTPUT
    [
        Output('tests-by-day', 'figure'),
        Output('pos-tests-by-day', 'figure'),
        Output('pos-rate-by-day', 'figure'),
        Output('pos-rate-by-week', 'figure')
    ],
    # INPUT
    [
        Input('dd_province', 'value'),
        Input('dpr', 'start_date'),
        Input('dpr', 'end_date')
    ]
)

def update_tests_by_day(selected_provinces, start_date, end_date):

    data_copy = data.copy()

    if not start_date is None and not end_date is None:
        start_date_datetime = datetime.strptime(start_date, '%Y-%m-%d')
        end_date_datetime = datetime.strptime(end_date, '%Y-%m-%d')
        data_copy = data_copy[(data_copy['DATE'] >= start_date_datetime) & (data_copy['DATE'] <= end_date_datetime)]
    elif start_date is None and not end_date is None:
        end_date_datetime = datetime.strptime(end_date, '%Y-%m-%d')
        data_copy = data_copy[data_copy['DATE'] <= end_date_datetime]
    elif not start_date is None and end_date is None:
        start_date_datetime = datetime.strptime(start_date, '%Y-%m-%d')
        data_copy = data_copy[data_copy['DATE'] >= start_date_datetime]

    if len(selected_provinces) == 0:

        data_copy_by_day = data_copy.groupby(by=pd.Grouper(key='DATE', freq='D'))[['TESTS_ALL', 'TESTS_ALL_POS']].sum().reset_index()
        data_copy_by_day['PCT_TESTS_POS'] = round((data_copy_by_day['TESTS_ALL_POS'] / data_copy_by_day['TESTS_ALL']) * 100, 2)
        data_copy_by_week = data_copy.groupby(by=pd.Grouper(key='DATE', freq='W'))[['TESTS_ALL_POS', 'TESTS_ALL']].sum().reset_index()
        data_copy_by_week['PCT_TESTS_POS'] = round((data_copy_by_week['TESTS_ALL_POS'] / data_copy_by_week['TESTS_ALL']) * 100, 2)

        fig_tests_by_day = px.line(

            data_frame=data_copy_by_day,
            x='DATE',
            y='TESTS_ALL',
            title='Total Number of Tests by Day',
            labels={'TESTS_ALL' : 'Number of Tests', 'DATE' : 'Date'}

        )

        fig_pos_tests_by_day = px.line(

            data_frame=data_copy_by_day,
            x='DATE',
            y='TESTS_ALL_POS',
            title='Total Number of Positive Tests by Day',
            labels={'TESTS_ALL_POS' : 'Number of Positive Tests', 'DATE' : 'Date'}

        )

        fig_pos_rate_by_day = px.line(

            data_frame=data_copy_by_day,
            title='Positivity Rate (%) by Day',
            x='DATE',
            y='PCT_TESTS_POS',
            labels={'DATE' : 'Date', 'PCT_TESTS_POS' : 'Positivity Rate (%)'}

        )

        fig_pos_rate_by_week = px.line(

            data_frame=data_copy_by_week,
            title='Positivity Rate (%) by Week',
            x='DATE',
            y='PCT_TESTS_POS',
            labels={'DATE' : 'Week', 'PCT_TESTS_POS' : 'Positivity Rate (%)'}

        )

        return fig_tests_by_day, fig_pos_tests_by_day, fig_pos_rate_by_day, fig_pos_rate_by_week

    else:

        data_copy = data_copy[data_copy['PROVINCE'].isin(selected_provinces)]
        data_copy_by_day_by_province = data_copy.groupby(by=[pd.Grouper(key='DATE', freq='D'), 'PROVINCE'])[['TESTS_ALL', 'TESTS_ALL_POS']].sum().reset_index()
        data_copy_by_day_by_province['PCT_TESTS_POS'] = round((data_copy_by_day_by_province['TESTS_ALL_POS'] / data_copy_by_day_by_province['TESTS_ALL']) * 100, 2)
        data_copy_by_week_by_province = data_copy.groupby(by=[pd.Grouper(key='DATE', freq='W'), 'PROVINCE'])[['TESTS_ALL_POS', 'TESTS_ALL']].sum().reset_index()
        data_copy_by_week_by_province['PCT_TESTS_POS'] = round((data_copy_by_week_by_province['TESTS_ALL_POS'] / data_copy_by_week_by_province['TESTS_ALL']) * 100, 2)
        color_mapping = {}
        for i in selected_provinces:
            color_mapping[i] = colors[i]

        fig_tests_by_day_province = px.line(

            data_frame=data_copy_by_day_by_province,
            x='DATE',
            y='TESTS_ALL',
            title='Total Number of Tests by Day',
            color='PROVINCE',
            labels={'TESTS_ALL' : 'Number of Tests', 'DATE' : 'Date'},
            color_discrete_map=color_mapping

        )

        fig_pos_tests_by_day_province = px.line(

            data_frame=data_copy_by_day_by_province,
            x='DATE',
            y='TESTS_ALL_POS',
            title='Total Number of Positive Tests by Day',
            color='PROVINCE',
            labels={'TESTS_ALL_POS' : 'Number of Positive Tests', 'DATE' : 'Date'},
            color_discrete_map=color_mapping

        )

        fig_pos_rate_by_day_province = px.line(

            data_frame=data_copy_by_day_by_province,
            x='DATE',
            y='PCT_TESTS_POS',
            title='Positivity Rate (%) by Day',
            color='PROVINCE',
            labels={'DATE' : 'Date', 'PCT_TESTS_POS' : 'Positivity Rate (%)'},
            color_discrete_map=color_mapping

        )

        fig_pos_rate_by_week_province = px.line(

            data_frame=data_copy_by_week_by_province,
            x='DATE',
            y='PCT_TESTS_POS',
            title='Positivity Rate (%) by Week',
            color='PROVINCE',
            labels={'DATE' : 'Week', 'PCT_TESTS_POS' : 'Positivity Rate (%)'},
            color_discrete_map=color_mapping

        )

        return fig_tests_by_day_province, fig_pos_tests_by_day_province, fig_pos_rate_by_day_province, fig_pos_rate_by_week_province

# APPLICATION
# ----------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
