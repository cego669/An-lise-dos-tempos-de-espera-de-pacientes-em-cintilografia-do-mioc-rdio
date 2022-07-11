"""
Created on Sat Jul 22 08:03:23 2022

@author: Carlos Eduardo Gonçalves de Oliveira (cego669), Alessandro Ramos Junior (allhazred)

Description: file containing script for the webapp.
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from datetime import datetime

# carregando os dados
data = pd.read_excel("horarios_tabela_final_preenchida.xlsx")
etapas = ["cadastro", "1_injecao", "1_imagem", "2_injecao", "2_imagem", "alta"]
data.dropna(subset = etapas, inplace = True)

# cálculo do tempo total de espera dos pacientes
data["tempo_espera"] = (data["alta"] - data["cadastro"]).apply(lambda x: x.total_seconds()/3600)

# agrupando os pacientes por dia
data_grouped = data.groupby(["dia", "dia_formatado"])["tempo_espera"]

# com os dados agrupados, calcula-se a média do tempo total de espera e o desvio padrão, para cada dia
x = data_grouped.apply(np.mean).reset_index().sort_values("dia")["tempo_espera"]
y = data_grouped.apply(np.mean).reset_index().sort_values("dia")["dia_formatado"]
error_x = data_grouped.apply(np.std).reset_index().sort_values("dia")["tempo_espera"]

st.markdown("""
<h1 style='text-align: center;'>Análise dos tempos de espera de pacientes em cintilografia do miocárdio na clínica CDI</h1>
""", unsafe_allow_html=True)

# autores
st.markdown("""
---

**Autores:** Carlos Eduardo G. de Oliveira e Alessando Ramos Júnior.

**Github:** *https://github.com/cego669/An-lise-dos-tempos-de-espera-de-pacientes-em-cintilografia-do-mioc-rdio/*""")

st.markdown("""
**Nota sobre os dados**: *quando houve horários faltantes para os pacientes, preencheu-se usando 
a mediana (referente ao dia, e não a geral) dos tempos de espera entre as etapas do exame. Optou-se por essa
metodologia para não gerar vieses nos cálculos ou no fluxo diário de pacientes.*
""", unsafe_allow_html=True)

st.markdown("""
---

### Tempo médio de espera por dia

O gráfico abaixo apresenta os valores da <ins>**média**</ins> e <ins>**desvio padrão**</ins> dos tempos de espera dos pacientes nos dias destacados. A escala de cores representa o valor de tempo de espera médio, quanto mais <ins>**vermelha**</ins> a cor <ins>**maior o valor respectivo**</ins>.
""",unsafe_allow_html=True)

# figura da média do tempo total de espera por dia
fig = px.bar(x = np.round(x, 2), y = y, error_x = np.round(error_x, 2), labels={"x": "Tempo total de espera (horas)",
                                                        "y": "Dia"}, color = -np.round(x, 2),
                                                        color_continuous_scale = 'Bluered_r',
                                                        width=800, height=800)
fig.update_layout(coloraxis_showscale=False)
st.plotly_chart(fig)

st.markdown("""
**Resumo geral:** *a média de tempo de espera dos pacientes ao longo de todos os dias foi de {} +- {} horas.*
""".format(np.round(data["tempo_espera"].mean(), 2), np.round(data["tempo_espera"].std(), 2)), unsafe_allow_html=True)

st.markdown("""
---

### Análise dos intervalos entre as principais etapas

Ao selecionar o <ins>**dia**</ins> é apresentado um gráfico onde são mostrados a <ins>**média**</ins> e o  <ins>**desvio padrão**</ins> dos tempos de espera (em minutos) entre as principais etapas do exame. 
Em seguida é apresentado um <ins>**vídeo**</ins> do <ins>**fluxo de pacientes**</ins>, onde cada bolinha representa um paciente a espera de ser encaminhado a próxima etapa.
""", unsafe_allow_html=True)

# seleção do dia para a análise dos intervalos de tempo entre as etapas do exame
day = st.selectbox("Selecione o dia:", y)

# filtrando o dataset para o dia específico
data_filtered = data.loc[data["dia_formatado"] == day, etapas + ["dia"]]
stages = ["cadastro", "1_injecao", "1_imagem", "2_injecao", "2_imagem", "alta"]
# para o dia em questão, calcula-se os intervalos de tempo entre as etapas
for i in range(len(stages)):
    try:
        data_filtered["Tempo_{}".format(i)] = (data[stages[i + 1]] - data[stages[i]]).apply(lambda x: x.total_seconds()/60)
    except:
        pass

# para cada intervalo de tempo no dia em questão, calcula-se a média e o desvio padrão
y = data_filtered.loc[:, ["Tempo_{}".format(i) for i in range(5)]].mean()
error_y = data_filtered.loc[:, ["Tempo_{}".format(i) for i in range(5)]].std()
x = ["Recepção - 1° injeção", "1° injeção - 1° imagem", "1° imagem - 2° injeção", "2° injeção - 2° imagem", "2° imagem - Alta"]

st.markdown("""
### Tempo de espera médio entre as principais etapas por paciente ({})
""".format(day))

# figura dos tempos de espera entre as etapas para o dia selecionado
fig = px.bar(x = x, y = np.round(y, 2), error_y = np.round(error_y, 2), labels = {"x": "Intervalo entre etapas", "y": "Tempo de espera (minutos)"})
fig.update_layout(yaxis_range=[0, 250])
st.plotly_chart(fig)

st.markdown("""
### Fluxo de pacientes ({})
""".format(day))

# abrindo vídeo referente ao dia selecionado
video_folder = data_filtered["dia"].reset_index().loc[0, "dia"].strftime("%d%m2022")
video_file = open("videos_mp4/" + video_folder + "/video.mp4", 'rb')
video_bytes = video_file.read()

# mostrando o vídeo
st.video(video_bytes)
