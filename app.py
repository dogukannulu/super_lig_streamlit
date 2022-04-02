import string
from streamlit_echarts import st_echarts
from cProfile import label
from re import A
import streamlit as st
import pandas as pd
import numpy as np

#MIN/MAX GOALS/CARDS IN A GAME/STADIUM
#----------------------------------------------------------------
def get_match_id(param_1, param_2):
    search_attribute = label_fact_dict[param_2]
    column = imple_1_3[search_attribute]

    if param_1 == 'En Çok':
        index = column.idxmax()
    else:
        index = column.idxmin()

    game_id = imple_1_3.at[index, 'id']
    value = imple_1_3.at[index, search_attribute]
    team = ""
    team = imple_1_3.at[index, 'exhibition_y_y']
    stad = ""
    stad = imple_1_3.at[index, 'stadium_y']

    df_match_result = df.loc[df['id'] == game_id]

    return game_id, df_match_result, team, stad, value






st.title('Super Lig Analiz')

label_fact_dict = {"Gol Atılan":'total_goals',"Kart Yenilen":'card_counts'}

@st.cache(allow_output_mutation=True)
def get_all():
    df = pd.read_csv('raw_data.csv')
    cards = pd.read_csv('cards.csv')
    changes = pd.read_csv('changes.csv')
    goals = pd.read_csv('goals.csv')
    startings = pd.read_csv('startings.csv')
    subs = pd.read_csv('subs.csv')
    return df, cards, changes, goals, startings, subs

get_all()

df = get_all()[0]
startings = get_all()[4]

df['total_goals'] = df['home_score']+df['away_score']

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


cards = get_all()[1]
st.write(cards)
#cool analiz

row2_1, row2_spacer2, row2_2, row2_spacer3, row2_3   = st.columns((1.6, .2, 1.6, .2, 1.6))

with row2_1:
    param_1 = st.selectbox("",('En Çok', 'En Az '))

with row2_2:
    param_2 = st.selectbox("",('Gol Atılan', 'Kart Yenilen'))

with row2_3:
    param_3 = st.selectbox("",('Maç','Stad'))


imple_1 = pd.merge(df,cards,on='id',how='left')
imple_1_1 = imple_1.groupby(['id', 'exhibition_y','stadium']).size().reset_index(name='card_counts')
imple_1_2 = imple_1.groupby(['id','exhibition_y','stadium'])['total_goals'].mean().reset_index(name='total_goals')

imple_1_3 = pd.merge(imple_1_1, imple_1_2, on='id',how='left')

asd = get_match_id(param_1, param_2)

st.write(asd[1])

#SEZONA GÖRE TAKIMLARIN GOL SAYILARI BAR CHART
#------------------------------------------------------------------------------------

goals = get_all()[3]
st.write(goals)

lst_teams = np.unique(df[['home','away']]).tolist()
lst_goals = []

choose_season = st.selectbox(
    'Hangi Sezon?',
    df['season'].unique().tolist())

df = df[df['season'] == choose_season]
for j in lst_teams: 
    lst_goals.append(df[df['away'] == j]['away_score'].sum() + df[df['home'] == j]['home_score'].sum())


options1 = {
    "xAxis": {
        "type": "category",
        "data": lst_teams,
    },
    "yAxis": {"type": "value"},
    "series": [{"data": lst_goals, "type": "bar"}],
}

if st.button('Getir'):
    st_echarts(options=options1, height="500px")


#------------------------------------------------------------------------------------

row3_1, row3_spacer1, row3_2, row3_spacer2 = st.columns((1.6, .2, 1.6, .2))
with row3_1:
    option_team = st.selectbox(
        'Hangi takım?',
        goals['home'].unique().tolist())
with row3_2:
    option_season = st.selectbox(
        'Hangi takım?',
        goals['season'].unique().tolist())


count_goals = 0
for i in range(len(goals)):
    if goals['season'][i] == option_season and goals['home'][i] == option_team and goals['variable'][i][0] == 'h' and type(goals['goal'][i]) == str:
        count_goals += 1
    elif goals['season'][i] == option_season and goals['away'][i] == option_team and goals['variable'][i][0] == 'a' and type(goals['goal'][i]) == str:
        count_goals += 1


     