# COVID-19 - CONFIRMED CASES BY DATE, PROVINCE, AGE, AND SEX
# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------

# IMPORTING LIBRARIES
# ----------------------------------------------------------------------------------------------------
import pandas as pd
import plotly
import plotly.express as px

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
from datetime import date
from datetime import datetime

# READING AND CLEANING DATA
# ----------------------------------------------------------------------------------------------------
data = pd.read_csv('../data/covid19be_cases_agesex.csv')
data.dropna(axis=0, how='any', thresh=None, subset=['DATE'], inplace=True)
data['DATE'] = pd.to_datetime(data['DATE'], format='%Y-%m-%d')
data['PROVINCE'].fillna('MISSING', inplace=True)
data.reset_index(drop=True, inplace=True)

min_date = data['DATE'].min()
max_date = data['DATE'].max()

# APP LAYOUT
# ----------------------------------------------------------------------------------------------------
app = dash.Dash(__name__)

app.layout = html.Div([

    # DROPDOWN : CHOOSE PROVINCE
    dcc.Dropdown(

        id='dd_province',
        options=[{'label' : x, 'value' : x} for x in data['PROVINCE'].unique()],
        clearable=True,
        multi=True,
        placeholder='Select Province',
        searchable=True,
        value=[]

    ),

    dcc.DatePickerRange(

        id='dpr',
        calendar_orientation='horizontal',
        end_date_placeholder_text='End Date',
        start_date_placeholder_text='Start Date',
        first_day_of_week=1,
        clearable=True,
        display_format='DD-MM-YYYY',
        updatemode='singledate',
        min_date_allowed=min_date.to_pydatetime(),
        max_date_allowed=max_date.to_pydatetime(),
        initial_visible_month=date.today()

    ),

    dcc.Graph(id='confirmed_cases')

])

# CALLBACK
# ----------------------------------------------------------------------------------------------------
@app.callback(
    Output('confirmed_cases', 'figure'),
    [Input('dd_province', 'value'), Input('dpr', 'start_date'), Input('dpr', 'end_date')]
)

def update_confirmed_cases(selected_provinces, start_date, end_date):

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

        data_by_date = data_copy.resample('D', on='DATE')['CASES'].sum().reset_index()

        fig = px.line(
            data_frame=data_by_date,
            x='DATE',
            y='CASES',
            labels={'CASES' : 'Confirmed Cases', 'DATE' : 'Date'},
            title='Confirmed Cases by Date'
        )

        return fig

    else:

        data_copy = data_copy[data_copy['PROVINCE'].isin(selected_provinces)].reset_index()
        data_by_province_date = data_copy.groupby(by=['PROVINCE']).resample('D', on='DATE')['CASES'].sum().reset_index()

        fig = px.line(
            data_frame=data_by_province_date,
            x='DATE',
            y='CASES',
            line_group='PROVINCE',
            color='PROVINCE',
            labels={'CASES' : 'Confirmed Cases', 'PROVINCE' : 'Province', 'DATE' : 'Date'},
            title='Confirmed Cases by Date by Province'
        )

        return fig

# APPLICATION
# ----------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
