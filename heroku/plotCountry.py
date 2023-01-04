import pandas as pd
import streamlit as st

import calendar
from datetime import datetime

import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

import seaborn as sns

from statsmodels.tsa.arima.model import ARIMA
from statsmodels.graphics.tsaplots import plot_predict
from pmdarima.arima import ADFTest
from statsmodels.tsa.seasonal import seasonal_decompose

import warnings 
warnings.filterwarnings('ignore')
showPyplotGlobalUse = False

def new_df_treaty(df, str):
    
    df = pd.DataFrame(df).rename_axis('data').reset_index()
    df['data'] = pd.to_datetime(df['data'])
    df['day'] = df['data'].apply(lambda x : x.day)
    df['day_of_week'] = df['data'].apply(lambda x : calendar.day_name[x.weekday()])
    df['month'] = pd.DatetimeIndex(df['data']).month
    df['month_name'] = df["month"].map({1:"JAN",2:"FEB",3:"MAR",
                                        4:"APR",5:"MAY",6:"JUN",
                                        7:"JUL",8:"AUG",9:"SEP",
                                        10:"OCT",11:"NOV",12:"DEC"})
    df['difference'] = df[str].diff()
    df['ma7'] = df.difference.rolling(7).mean()
    df['ma14'] = df.difference.rolling(14).mean()
    df['ma21'] = df.difference.rolling(21).mean()
    df = df[(df[str] > 0 )]

    return df


def df_data_2020(df):
    
    df = df[(df['data'] >= '2020-01-01') & (df['data'] <= '2020-12-31') & (df['difference'] >= 0)]

    return df


def df_data_2021(df):
    
    df = df[(df['data'] >= '2021-01-01') & (df['data'] <= '2021-12-31') & (df['difference'] >= 0)]
    
    return df


def df_data_2022(df):
    
    df = df[(df['data'] >= '2022-01-01') & (df['data'] <= '2022-12-31') & (df['difference'] >= 0)]
    
    return df


def annotate_bar(ax):
    for p in ax.patches:
        y = p.get_height()
        ax.annotate(f'{int(y)}', xy=(p.get_x() + p.get_width()/2,y),
                    va = 'baseline', fontsize=10, color='black', xytext=(0,1),
                    textcoords='offset points', ha='center')


def annotate_bar_horizontal(ax):
    for p in ax.patches:
        x = p.get_width()
        ax.annotate(f'{int(x)}', xy=(x,p.get_y() + p.get_height()/2),
                    va = 'center', fontsize=10, color='black', xytext=(0,1),
                    textcoords='offset points', ha='left')


def trans_data(df, pais):
    
    df = pd.DataFrame(df).rename_axis('data')
    df['data'] = pd.to_datetime(df['data'])
    df = df.set_index('data')
    df = df[pais]
    
    return df

def plot_graf(df, pais):
    
    grup_day = (df.groupby('day')['difference']
                        .sum()
                        .to_frame()
                        .reset_index())
    
    grup_day_of_week = (df.groupby('day_of_week')['difference']
                        .sum()
                        .to_frame()
                        .reset_index())
    grup_day_of_week['day_of_week'] = grup_day_of_week['day_of_week'].map({'Monday':1,'Tuesday':2,'Wednesday':3,
                                                                                           'Thursday':4,'Friday':5,'Saturday':6, 
                                                                                           'Sunday':7})
    grup_day_of_week = grup_day_of_week.sort_values(by=['day_of_week'])
    grup_day_of_week['day_of_week'] = grup_day_of_week['day_of_week'].map({1:'Monday',2:'Tuesday',3:'Wednesday',
                                                                        4:'Thursday',5:'Friday',6:'Saturday', 
                                                                        7:'Sunday'})
    
    grup_month = (df.groupby('month_name')['difference']
                        .sum()
                        .to_frame()
                        .reset_index())
    grup_month['month_name'] = grup_month['month_name'].map({"JAN":1,"FEB":2,"MAR":3,
                                                             "APR":4,"MAY":5,"JUN":6,
                                                             "JUL":7,"AUG":8,"SEP":9,
                                                             "OCT":10,"NOV":11,"DEC":12})
    grup_month = grup_month.sort_values(by=['month_name'])
    grup_month['month_name'] = grup_month['month_name'].map({1:"JAN",2:"FEB",3:"MAR",
                                                             4:"APR",5:"MAY",6:"JUN",
                                                             7:"JUL",8:"AUG",9:"SEP",
                                                            10:"OCT",11:"NOV",12:"DEC"})
    
    
    data_min = df['data'].dt.strftime('%Y/%m/%d').min()
    data_max = df['data'].dt.strftime('%Y/%m/%d').max()
    
    mday_of_week = (grup_day_of_week['difference'].sum()/7)
    mday = (grup_day['difference'].sum()/31)
    mmonth = (grup_month['difference'].sum()/12)
    
    ts = df[['data', pais]]
    ts = trans_data(ts, pais)
    decomposicao = seasonal_decompose(ts, period=12)
    
    #tendencia
    tendencia = decomposicao.trend
    #sozonalidade
    sazonal = decomposicao.seasonal
    #erro
    aleatorio = decomposicao.resid
    
    modelo = ARIMA(ts, order=(2, 1, 2), freq=ts.index.inferred_freq) 
    modelo_treinado = modelo.fit()
    modelo_treinado.summary()
    
    fig = plt.figure(figsize=(20,15))

    fig.set_constrained_layout('w_pad')

    gs = fig.add_gridspec(4, 3)

    ax0 = fig.add_subplot(gs[0,:])

    plt.bar(df['data'], df['difference'], label = f'Casos {pais}', color='#03BB85') 
    sns.lineplot(x = df['data'],  y = 'ma7', data = df, label = 'Média Móvel 7 dias', color='black', linewidth=2)
    sns.lineplot(x = df['data'],  y = 'ma14', data = df, label = 'Média Móvel 14 dias', color='red', linewidth=2)
    sns.lineplot(x = df['data'],  y = 'ma21', data = df, label = 'Média Móvel 21 dias', color='purple', linewidth=2)
    plt.xticks(rotation=45)
    ax0.set(
        title= f'Quantidades de Casos de Covid-19 no período de {data_min} á {data_max}',
        ylabel='Quantidades de Casos',
        #yticks=[],
        #xticks=[],
        xlabel='Data')

    ax01 = fig.add_subplot(gs[1, 0])
    
    sns.barplot(data=grup_day_of_week, x='day_of_week', y='difference')
    plt.axhline(y=mday_of_week, xmin=0.0, xmax=1, color='black')
    plt.legend([f'Média {mday_of_week:.0f}'])
    annotate_bar(ax01)
    ax01.set(
        title='Quantidades de casos de Covid-19 por nome da semana',
        ylabel='Quantidades de Casos',
        #yticks=[],
        #xticks=[],
        xlabel='Nome da Semana')

    ax02 = fig.add_subplot(gs[1, 1])

    sns.barplot(data=grup_day, x='day', y='difference')
    plt.axhline(y=mday, xmin=0.0, xmax=1, color='black')
    plt.legend([f'Média {mday:.0f}'])
    ax02.set(
        title='Quantidades de casos de Covid-19 por dia da semana',
        ylabel='Quantidades de Casos',
        #yticks=[],
        #xticks=[],
        xlabel='Dias da Semana')

    ax03 = fig.add_subplot(gs[1, 2])

    sns.barplot(data=grup_month, x='month_name', y='difference')
    plt.axhline(y=mmonth, xmin=0.0, xmax=1, color='black')
    plt.legend([f'Média {mmonth:.0f}'])
    ax03.set(
        title='Quantidades de casos de Covid-19 por meses',
        ylabel='Quantidades de Casos',
        #yticks=[],
        #xticks=[],
        xlabel='Meses')

    ax04 = fig.add_subplot(gs[2, 0])
    plt.plot(sazonal)
    plt.xticks(rotation=45)
    ax04.set(
        title='Sazonalidade',
        #yticks=[],
        #xticks=[],
        xlabel='Data')

    ax05 = fig.add_subplot(gs[2, 1])
    plt.plot(tendencia)
    plt.xticks(rotation=45)
    ax05.set(
        title='Tendência',
        #yticks=[],
        #xticks=[],
        xlabel='Data')

    ax06 = fig.add_subplot(gs[2, 2])
    plt.plot(aleatorio)
    plt.xticks(rotation=45)
    ax06.set(
        title='Aleatoriedade',
        #yticks=[],
        #xticks=[],
        xlabel='Data')
    
    ax07 = fig.add_subplot(gs[-1, -1])
    plt.plot(df['data'], df[pais], label = f'Casos {pais}') 
    plt.xticks(rotation=45)
    ax07.set(
        title= 'Evolução de Casos de Covid-19',
        ylabel='Quantidades de Casos',
        #yticks=[],
        #xticks=[],
        xlabel='Data')

    ax08 = fig.add_subplot(gs[-1,:2])
    eixo = ts.plot()
    plot_predict(modelo_treinado, '2021-09-01', '2023-02-28', ax = eixo, plot_insample = True)
    ax08.set(
        title= f'Forecast dados infectados {pais}',
        ylabel='Quantidades de Casos',
        #yticks=[],
        #xticks=[],
        xlabel='Data')
    
    fig.suptitle(f'Análise Covid-19 {pais}', fontsize=20, y=1.05)

    view = plt.show()
    
    return st.pyplot(view)