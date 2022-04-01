import string
import streamlit as st
import pandas as pd
import numpy as np
from streamlit_echarts import st_echarts

st.title('Super Lig Analiz')

df = pd.read_csv('raw_data.csv')

st.write(df)

row6_1, row6_spacer2 = st.columns((7.1, .2))
with row6_1:
    st.subheader(f"Elimizde toplam {df['season'].nunique()} sezonluk bir veriseti var:")

row2_1, row2_spacer2, row2_2, row2_spacer3, row2_3, row2_spacer4, row2_4, row2_spacer5   = st.columns((1.6, .2, 1.6, .2, 1.6, .2, 1.6, .2))
with row2_1:
    unique_games_in_df = df.id.nunique()
    str_games = "🏟️ " + str(unique_games_in_df) + " Karşılaşma"
    st.markdown(str_games)
with row2_2:
    unique_teams_in_df = len(np.unique(df[['home','away']]).tolist())
    t = " Takım"
    str_teams = "🏃‍♂️ " + str(unique_teams_in_df) + t
    st.markdown(str_teams)
with row2_3:
    total_goals_in_df = df['home_score'].sum() + df['away_score'].sum()
    str_goals = "🥅 " + str(total_goals_in_df) + " Gol"
    st.markdown(str_goals)
with row2_4:
    total_shots_in_df = len(np.unique(df['ref_main']))
    str_refs = "🙅‍♂️ " + str(total_shots_in_df) + " Hakem"
    st.markdown(str_refs)

df_goals = pd.read_csv('goals.csv')
df_match_id = df_goals['id'].unique()

st.write(df_goals)

lst_teams = np.unique(df[['home','away']]).tolist()
lst_goals = []

choose_season = st.selectbox(
    'Hangi Sezon?',
    df_goals['season'].unique().tolist())

for j in lst_teams:
    count = 0
    count += df[(df['home'] == j) & (df['season'] == choose_season)]['home_score'].sum()
    count += df[(df['away'] == j) & (df['season'] == choose_season)]['away_score'].sum()
    lst_goals.append(count)

options = {
    "xAxis": {
        "type": "category",
        "data": lst_teams,
    },
    "yAxis": {"type": "value"},
    "series": [{"data": lst_goals, "type": "bar"}],}

if st.button('Takım kendi evinde kaç gol attı?'):
    st_echarts(options=options, height="500px")




row3_1, row3_spacer1, row3_2, row3_spacer2 = st.columns((1.6, .2, 1.6, .2))
with row3_1:
    option_team = st.selectbox(
        'Hangi takım?',
        df_goals['home'].unique().tolist())
with row3_2:
    option_season = st.selectbox(
        'Hangi takım?',
        df_goals['season'].unique().tolist())


count_goals = 0
for i in range(len(df_goals)):
    if df_goals['season'][i] == option_season and df_goals['home'][i] == option_team and df_goals['variable'][i][0] == 'h' and type(df_goals['goal'][i]) == str:
        count_goals += 1
    elif df_goals['season'][i] == option_season and df_goals['away'][i] == option_team and df_goals['variable'][i][0] == 'a' and type(df_goals['goal'][i]) == str:
        count_goals += 1


     