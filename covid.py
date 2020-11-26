#!/usr/bin/env python
# coding: utf-8

# In[4]:


import pandas as pd
import streamlit as st
import altair as alt

@st.cache
def get_UN_date():
    df = pd.read_csv("dadosCovidPaises.csv")
    return df.set_index("Paises")


df = get_UN_date()

st.markdown("![Alt Center](https://media.giphy.com/media/JRsY1oIVA7IetTkKVO/giphy.gif)")

#st.title("Dados Covid-19 mundialmente")
st.title('🦠 Covid-19 Dashborad 🦠 ')
st.sidebar.markdown('🦠 **Covid-19 Dashborad** 🦠 ')
st.sidebar.markdown(''' 
Este aplicativo fornece informações sobre infecções por Covid-19 em todo o mundo.
Os dados considerados para esta análise são de 10 meses, começando de 22-01-2020 a 24-11-2020
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


tabela_dois = st.sidebar.checkbox('Tabela de dados completa')
if tabela_dois:
    st.markdown('### Tabela de dados ' + str(df.shape[0]) + ' linhas e ' + str(df.shape[1]) + ' colunas.')
    st.write(df)






