# COVID-19 - HOSPITALISATIONS BY DATE AND PROVINCE
# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------

# IMPORTING LIBRARIES
# ----------------------------------------------------------------------------------------------------
import pandas as pd
import plotly
import plotly.express as px

# READING DATA
# ----------------------------------------------------------------------------------------------------
data = pd.read_csv('./data/COVID19BE_HOSP.csv')

# CLEANING DATA
# ----------------------------------------------------------------------------------------------------
data.dropna(inplace=True)
data.reset_index(drop=True, inplace=True)
data['DATE'] = pd.to_datetime(data['DATE'])

# DATA ANALYSIS
# ----------------------------------------------------------------------------------------------------
data_by_date = data.resample('D', on='DATE')[['TOTAL_IN', 'TOTAL_IN_ICU', 'NEW_IN', 'NEW_OUT']].sum().reset_index()
data_by_date['PCT_IN_ICU'] = (data_by_date['TOTAL_IN_ICU'] / data_by_date['TOTAL_IN']) * 100
data_by_date['NEW_DIFF'] = data['NEW_IN'] - data['NEW_OUT']
data_by_date['PCT_IN_ICU'] = data_by_date['PCT_IN_ICU'].round(2)

# DATA VISUALIZATION
# ----------------------------------------------------------------------------------------------------
# total number of hospitalized patients per date
# total number of hospitalized patients in the ICU per date
fig_total_per_date = px.line(
    data_frame = data_by_date,
    x='DATE',
    y=['TOTAL_IN', 'TOTAL_IN_ICU'],
    title='Total Number of Hospitalized Patients and Patients in the ICU',
    labels={'DATE' : 'Date'}
)

fig_total_per_date.update_yaxes({
    'title' : {'text' : 'Number of Patients'},
    'rangemode' : 'nonnegative'
})

fig_total_per_date.show()

# % of total number of all hospitalized patients who are in the ICU per date
fig_pct_in_icu_per_date = px.line(
    data_frame=data_by_date,
    x='DATE',
    y='PCT_IN_ICU',
    title='Percentage of all Hospitalized patients in the ICU',
    labels={'DATE' : 'Date', 'PCT_IN_ICU' : 'Pct in ICU'}
)

fig_pct_in_icu_per_date.show()

# total number of intakes per date
# total number of discharges per date
fig_int_dis_per_date = px.line(
    data_frame=data_by_date,
    x='DATE',
    y=['NEW_IN', 'NEW_OUT'],
    title='Number of Intakes and Discharges per 24 Hours',
    labels={'DATE' : 'Date'}
)

fig_int_dis_per_date.update_yaxes({
    'title' : {'text' : 'Number of Patients'},
    'rangemode' : 'nonnegative',
})

fig_int_dis_per_date.show()

# difference between total number of intakes and discharges per date
fig_int_dis_diff_per_date = px.line(
    data_frame=data_by_date,
    x='DATE',
    y='NEW_DIFF',
    title='Difference Between Intakes and Discharges per 24 Hours',
    labels={'DATE' : 'Date', 'NEW_DIFF' : 'Number of Patients'}
)

fig_int_dis_diff_per_date.show()

# total number of hospitalized patients per date per province
# total number of hospitalized patients in the ICU per date per province
fig_total_per_province = px.line(
    data_frame=data,
    x='DATE',
    y=['TOTAL_IN', 'TOTAL_IN_ICU'],
    color='PROVINCE',
    title='Total Number of Hospitalized Patients and Patients in the ICU per Province',
    labels={'DATE' : 'Date', 'PROVINCE' : 'Province'}
)

fig_total_per_province.update_yaxes({
    'title' : {'text' : 'Number of Patients'},
    'rangemode' : 'nonnegative'
})

fig_total_per_province.show()

# % of total number of all hospitalized patients who are in the ICU per date per province
data['PCT_IN_ICU'] = (data['TOTAL_IN_ICU'] / data['TOTAL_IN']) * 100
data['PCT_IN_ICU'] = data['PCT_IN_ICU'].round(2)

fig_pct_in_icu_per_date_per_province = px.line(
    data_frame=data,
    x='DATE',
    y='PCT_IN_ICU',
    color='PROVINCE',
    title='Percentage of all Hospitalized patients in the ICU per Province',
    labels={'DATE' : 'Date', 'PCT_IN_ICU' : 'Pct in ICU'}
)

fig_pct_in_icu_per_date_per_province.show()

# total number of intakes per date per province
# total number of discharges per date per province
data['NEW_DIFF'] = data['NEW_IN'] - data['NEW_OUT']

fig_int_dis_per_date_per_province = px.line(
    data_frame=data,
    x='DATE',
    y=['NEW_IN', 'NEW_OUT'],
    color='PROVINCE',
    title='Number of Intakes and Discharges per 24 Hours per Province',
    labels={'DATE' : 'Date'}
)

fig_int_dis_per_date_per_province.update_yaxes({
    'title' : {'text' : 'Number of Patients'},
    'rangemode' : 'nonnegative',
})

fig_int_dis_per_date_per_province.show()

# difference between total number of intakes and discharges per date per province
fig_int_dis_diff_per_date_per_province = px.line(
    data_frame=data,
    x='DATE',
    y='NEW_DIFF',
    color='PROVINCE',
    title='Difference Between Intakes and Discharges per Day per 24 Hours per Province',
    labels={'DATE' : 'Date', 'NEW_DIFF' : 'Number of Patients'}
)

fig_int_dis_diff_per_date_per_province.show()
