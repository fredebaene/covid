# COVID-19 - CONFIRMED CASES BY DATE, PROVINCE, AGE, AND SEX
# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------

# IMPORTING LIBRARIES
# ----------------------------------------------------------------------------------------------------
import pandas as pd
import plotly
import plotly.express as px

# READING DATA
# ----------------------------------------------------------------------------------------------------
data = pd.read_csv('./data/COVID19BE_CASES_AGESEX.csv')

# CLEANING DATA
# ----------------------------------------------------------------------------------------------------
data.dropna(axis=0, how='any', thresh=None, subset=None, inplace=True)
data['DATE'] = pd.to_datetime(data['DATE'], format='%Y-%m-%d')
data.reset_index(drop=True, inplace=True)

# DATA ANALYSIS
# ----------------------------------------------------------------------------------------------------
# Questions:
# - number of cases per province
# - number of cases per age group
# - number of cases per province per age group

data_by_province_date = data.groupby(by=['PROVINCE']).resample('D', on='DATE')['CASES'].sum().reset_index()
data_by_agegroup_date = data.groupby(by=['AGEGROUP']).resample('D', on='DATE')['CASES'].sum().reset_index()

# DATA VISUALIZATION
# ----------------------------------------------------------------------------------------------------
# cases by province
fig_cases_by_province = px.line(
    data_frame=data_by_province_date,
    x='DATE',
    y='CASES',
    line_group='PROVINCE',
    color='PROVINCE',
    labels={'CASES' : 'Confirmed Cases', 'PROVINCE' : 'Province', 'DATE' : 'Date'},
    title='Confirmed Cases by Province'
)

fig_cases_by_province.show()

# cases by age group
fig_cases_by_agegroup = px.line(
    data_frame=data_by_agegroup_date,
    x='DATE',
    y='CASES',
    line_group='AGEGROUP',
    color='AGEGROUP',
    labels={'CASES' : 'Confirmed Cases', 'AGEGROUP' : 'Age Group', 'DATE' : 'Date'},
    title='Confirmed Cases by Age Group'
)

fig_cases_by_agegroup.show()
