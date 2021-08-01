import pandas as pd
import numpy as np
from datetime import datetime
import database
from sqlalchemy import create_engine

search_dic = {}
directions_dict = {
    'N': 1,
    'NNE': 2,
    'NE': 3,
    'ENE': 4,
    'E': 5,
    'ESE': 6,
    'SE': 7,
    'SSE': 8,
    'S': 9,
    'SSW': 10,
    'SW': 11,
    'WSW': 12,
    'W': 13,
    'WNW': 14,
    'NW': 15,
    'NNW': 16
}
hbt_dict = {
    'Head': 1,
    'Beam': 2,
    'Tail': 3
}
F04_3_cols_name = {
    'waveh': 'WAVEh',
    'bf': 'BF',
    'tw_head_beam_tail': 'TWhbt',
    'tw_direction_index': 'TWd',
    'tc_head_beam_tail': 'TChbt',
    'tc_direction_index': 'TCd',
    'twspeed': 'TWs',
    'tcspeed': 'TCs',
    'slip': 'SLIP',
    'stw': 'STW',
    'sog': 'SOG',
    'poweravgkw': 'BHP',
    'me_foc_hfo': 'FOC',
    'rpm': 'RPM'
}

def set_search_dic(search_str):
    # Parse URL querry string into dictionary
    global search_dic
    if(search_str != None and search_str != ''):
        # TODO: remove print statement before deploying
        print(search_str)
        search_str = search_str.replace('?', '').replace('%20', ' ')
        search_dic = {}
        search_dic = dict(item.split("=") for item in search_str.split("&"))
        # TODO: remove print statement before deploying
        print(search_dic)
    else:
        search_dic = {}

def get_search_dic():
    return search_dic

def to_datetime(date):
    return pd.to_datetime(date)

def create_dataframe():
    return pd.DataFrame()

def correlation_matrix(dataframe):
    cond = np.triu(np.ones(dataframe.shape)).astype(np.bool)
    return dataframe.where(cond).round(2).iloc[:, ::-1]

def isnan(element):
    return np.isnan(element)

def read_csv(file):
    return pd.read_csv(file)

def linear_reg_date(x_data, y_data):
    # transfer x_data from datetime to numerical value
    x = x_data.apply(lambda x: x.timestamp())
    y = y_data

    polyfit = np.polyfit(x, y, deg=1)
    poly = np.poly1d(polyfit)

    x_reg = np.arange(x.min(), x.max(), 1000)
    y_reg = poly(x_reg)

    x_reg = pd.Series(x_reg)
    y_reg = pd.Series(y_reg)

    # transfer x_reg back to datetime
    x_reg = x_reg.apply(lambda x: datetime.utcfromtimestamp(x))

    return x_reg, y_reg

def linear_reg_date_manual(x_data, y_data, coeff_1, coeff_2):
    # transfer x_data from datetime to numerical value
    x = x_data.apply(lambda x: x.timestamp())
    y = y_data

    poly = np.poly1d([coeff_1, coeff_2])

    x_reg = np.arange(x.min(), x.max(), 1000)
    y_reg = poly(x_reg)

    x_reg = pd.Series(x_reg)
    y_reg = pd.Series(y_reg)

    # transfer x_reg back to datetime
    x_reg = x_reg.apply(lambda x: datetime.utcfromtimestamp(x))

    return x_reg, y_reg

def linear_reg(x_data, y_data):
    polyfit = np.polyfit(x_data, y_data, deg=2)
    poly = np.poly1d(polyfit)

    x_reg = np.arange(x_data.min(), x_data.max(), 1)
    y_reg = poly(x_reg)

    return x_reg, y_reg

def get_fig_dataframe(fig_no, fig_dataset, cols):
    engine = create_engine(database.URL)

    # In case the DNS server broke, use IP directly
    # engine = create_engine(database.IP)

    fm_fig_data = pd.read_sql_table('fm_fig_data_0725', con=engine)
    fm_detail = pd.read_sql_table('fmtable0723', con=engine, columns=cols)

    if type(fig_dataset) == int:
        fm_fig_data = fm_fig_data[(fm_fig_data['fig_no'] == fig_no) & (fm_fig_data['fig_dataset'] == fig_dataset)]
    elif type(fig_dataset) == list:
        fm_fig_data = fm_fig_data[(fm_fig_data['fig_no'] == fig_no) & (fm_fig_data['fig_dataset'].isin(fig_dataset))]

    return fm_fig_data.merge(fm_detail, on='timeid', how='left').round(2)

def get_fig_table(table_name):
    engine = create_engine(database.URL)

    # In case the DNS server broke, use IP directly
    # engine = create_engine(database.IP)

    return pd.read_sql_table(table_name, con=engine)

def get_corr_data(cols):
    engine = create_engine(database.URL)

    # In case the DNS server broke, use IP directly
    # engine = create_engine(database.IP)

    return pd.read_sql_table('fmtable0723', con=engine, columns=cols)

def debug_info(file_name, n_intervals, columns, isempty):
    print('##############################')
    print(datetime.now())
    print(file_name)
    print('Interval(s): ' + str(n_intervals))
    print('Dataframe contains these columns:')
    print(columns)
    print('Dataframe is empty: ', end='')
    print(isempty)
    print('##############################')
