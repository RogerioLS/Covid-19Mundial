#!/usr/bin/env python
# coding: utf-8

# In[4]:


#!/usr/bin/env python
# coding: utf-8

# In[4]:

import plotCountry as pltC

from datetime import datetime

import pandas as pd
import streamlit as st

import altair as alt

from urllib.request import urlretrieve 

import warnings 
warnings.filterwarnings('ignore')
showPyplotGlobalUse = False


@st.cache_data
def get_UN_date():
    url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
    df = pd.read_csv(url)
    df = df.rename(columns = {'Country/Region':'Country'})
    df = df.groupby('Country').sum().rename_axis('Country')
    df = df.drop(['Lat', 'Long'], axis=1, inplace=False)
    df = df.reset_index()
    
    #df = pd.read_csv("dadosCovidPaises.csv")
    return df.set_index("Country") 


df = get_UN_date()

country = 'China'
dd = df.loc[country]
dd = pltC.new_df_treaty(dd, country)
data_min = dd['data'].dt.strftime('%Y/%m/%d').min()
data_max = dd['data'].dt.strftime('%Y/%m/%d').max()

d1 = datetime.strptime(data_min, '%Y/%m/%d').date()
d2 = datetime.strptime(data_max, '%Y/%m/%d').date()

diff = d2 - d1

months = diff.days // 30

st.markdown("![Alt Center](https://media.giphy.com/media/JRsY1oIVA7IetTkKVO/giphy.gif)")

#st.title("Dados Covid-19 mundialmente")
st.title('🦠 Covid-19 Dashboard 🦠 ')
st.sidebar.markdown('🦠 **Covid-19 Dashboard** 🦠 ')
st.sidebar.markdown(f'''
Este aplicativo fornece informações sobre infecções por Covid-19 em todo o mundo.
Os dados considerados para esta análise são de {months} meses, começando de {data_min} à {data_max}
Selecione os diferentes paises para variar a visualização do gráficos que é interativo.
Dica Role o mouse sobre o gráfico para sentir o recurso interativo para a melhor visualização de cada ponto.

Projetado por: 
**Rogério Lopes**  ''')

countries = st.sidebar.multiselect("Selecione o País", list(df.index), ["Brazil"])

data = df.loc[countries]

st.write("### Tabela com os dados", data.sort_index())

data = data.T.reset_index()
data = pd.melt(data, id_vars=["index"]).rename(
    columns={"index": "Meses", "value": "Numeros de infectados"}
)

chart = (
    alt.Chart(data, width=500, height=300)
    .mark_circle(interpolate="basis")
    .encode(
        x=alt.X("Meses:T"),
        y=alt.Y("Numeros de infectados:Q", stack=None),
        tooltip=["Paises:N", "Meses:T", "Numeros de infectados:Q"],
        color="Paises:N"
    ).interactive()
)

st.altair_chart(chart, use_container_width=True)


tabela_dois = st.sidebar.checkbox('Gráficos')
if tabela_dois:
    classifier_name = st.sidebar.selectbox('Selecione o País', (list(df.index)))
    dados = df.loc[classifier_name]
    name_country = str(classifier_name)
    dd = pltC.new_df_treaty(dados, name_country)
    data_min_country = dd['data'].dt.strftime('%Y/%m/%d').min()
    data_max_country = dd['data'].dt.strftime('%Y/%m/%d').max()
    
    st.markdown(f'''Nesses gráficos você encontrarar algumas análises desde quando início o contágio, média movel, quais dias da semana ocorreu o maior contágio, forecast desdo periodo de {data_min_country} à {data_max_country}.''')
    st.set_option('deprecation.showPyplotGlobalUse', False)
    showPyplotGlobalUse = False
    pltgraf = pltC.plot_graf(dd, name_country)


tabela_tres = st.sidebar.checkbox('Tabela de dados completa')
if tabela_tres:
    st.markdown('### Tabela de dados ' + str(df.shape[0]) + ' linhas e ' + str(df.shape[1]) + ' colunas.')
    st.write(df)

st.markdown('''
Para fazer a capturas dos dados que foram utilizar para realizar essa tarefa eu utilizei o 
Repositório de dados COVID-19 pelo Centro de Ciência e Engenharia de Sistemas (CSSE) da Universidade Johns Hopkins, 
esse repositório é atualizado com fraquencia com fonte de dados confiáveis do mundo todo.

**Link para ser direcionado para o repositório:**

[Clique aqui para olhar e entender melhor as fontes dos dados](https://github.com/CSSEGISandData/COVID-19)
''')
