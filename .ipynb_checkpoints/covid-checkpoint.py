#!/usr/bin/env python
# coding: utf-8

# In[4]:


#!/usr/bin/env python
# coding: utf-8

# In[4]:


import pandas as pd
import streamlit as st
import altair as alt

import matplotlib.pyplot as plt
from datetime import datetime
from statsmodels.tsa.arima_model import ARIMA
from pmdarima.arima import ADFTest
import warnings 
warnings.filterwarnings('ignore')
showPyplotGlobalUse = False


@st.cache
def get_UN_date():
    df = pd.read_csv("dadosCovidPaises.csv")
    return df.set_index("Paises")


df = get_UN_date()

st.markdown("![Alt Center](https://media.giphy.com/media/JRsY1oIVA7IetTkKVO/giphy.gif)")

#st.title("Dados Covid-19 mundialmente")
st.title('🦠 Covid-19 Dashboard 🦠 ')
st.sidebar.markdown('🦠 **Covid-19 Dashboard** 🦠 ')
st.sidebar.markdown(''' 
Este aplicativo fornece informações sobre infecções por Covid-19 em todo o mundo.
Os dados considerados para esta análise são de 19 meses, começando de 22-01-2020 a 25-07-2021
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

def trans_data(data):
    dados = pd.DataFrame(data).rename_axis('data')
    dados.reset_index(level=0, inplace = True)
    dados['data'] = pd.to_datetime(dados['data'])
    dados = dados.set_index('data')
    dados = dados.fillna(method = 'ffill')
    adf_test = ADFTest(alpha = 0.05)
    adf_test.should_diff(dados)
    modelo = ARIMA(dados, order=(2, 1, 2),freq=dados.index.inferred_freq) 
    modelo_treinado = modelo.fit(disp=False)
    #plt.rcParams.update({'font.size': 15})
    plt.rcParams['xtick.labelsize'] = 15
    plt.rcParams['ytick.labelsize'] = 15
    eixo = dados.plot(figsize=(12, 8))
    modelo_treinado.plot_predict('2021-04-30', '2021-08-15', ax = eixo, plot_insample = True)
    plt.title('Forecast dados Infectados', fontweight='bold', fontsize=15)
    plt.xlabel('Meses', fontweight='bold', fontsize=15) 
    plt.ylabel('Valor em milhões', fontweight='bold',  fontsize=15)
    return st.pyplot()

tabela_dois = st.sidebar.checkbox('Gráfico de Forecast')
if tabela_dois:
    st.markdown('''Esse gráfico é totalmente dedicado para o Forecast com os números de infectados 
                    com o periodo de '2021-04-30', '2021-08-15'.''')
    classifier_name = st.sidebar.selectbox('Selecione o País', (list(df.index)))
    dados = df.loc[classifier_name]
    dados = dados[dados > 0]
    data = trans_data(dados)
    showPyplotGlobalUse = False
    st.write(data)


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




