import streamlit as st
import pandas as pd
import numpy as np

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
