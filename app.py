<<<<<<< HEAD
import string
from streamlit_echarts import st_echarts
from cProfile import label
from re import A
import streamlit as st
import pandas as pd
import numpy as np
=======
from tkinter import CENTER
from streamlit_echarts import st_echarts
import streamlit as st
import pandas as pd
import numpy as np
import functools
import textwrap

st.set_page_config(layout="wide",page_title='Süper Lig', page_icon=':ball:')

>>>>>>> origin/main

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
<<<<<<< HEAD

df['total_goals'] = df['home_score']+df['away_score']

st.write(df)
=======
subs = get_all()[5]

df['total_goals'] = df['home_score']+df['away_score']

>>>>>>> origin/main

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
<<<<<<< HEAD
st.write(cards)
=======
>>>>>>> origin/main
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
<<<<<<< HEAD

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

lst_teams = pd.Series(lst_teams, index=lst_goals)
lst_teams = lst_teams.reset_index()

st.write(lst_teams)


options1 = {
    "xAxis": {
        "type": "category",
        "data": lst_teams[lst_teams.columns[1]].values.tolist(),
    },
    "yAxis": {"type": "value"},
    "series": [{"data": lst_teams[lst_teams.columns[0]].values.tolist(), "type": "bar"}],
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
=======
match_id = get_match_id(param_1, param_2)[0]


dataframes = [df, startings, subs]
df_final = functools.reduce(lambda left,right: pd.merge(left,right,on='id'), dataframes)
df_final = df_final.groupby(['id', 'season','exhibition_x','starting_player']).size().reset_index(name='total_goals')



data = get_all()[0]
st.write(data)

row3_1, row3_2, row3_3, row3_4, row3_5 = st.columns([1, .1, 1, .1, 1])

with row3_1:
  season = st.selectbox("", data['season'].sort_values().unique().tolist())

data_season = data[(data['season'] == season)]

with row3_3:
  hafta = st.selectbox("", data['hafta'].sort_values().unique().tolist())

data_hafta = data_season[(data_season['season'] == season) & (data_season['hafta'] == hafta)]

with row3_5:
  karsilasma = st.selectbox("", data_hafta['exhibition'].unique().tolist())

matchId = data_hafta[(data_hafta['season'] == season) & (data_hafta['hafta'] == hafta) & (data_hafta['exhibition'] == karsilasma)]['id'].values[0]

import PIL
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 

img = Image.open("saha.png")    #this is the image we want to add text to
team_img = Image.open("home.png")
away_img = Image.open("away.png")
draw = ImageDraw.Draw(img)  # Create a drawing object that is used to draw on the new image.
draw_team = ImageDraw.Draw(team_img)
draw_away = ImageDraw.Draw(away_img)
font_score = ImageFont.truetype('BankGthd.ttf', encoding="utf-8", size=120)  # Create the font object\
font_info = ImageFont.truetype('Roboto-Regular.ttf', encoding="utf-8", size=30) 
font_team = ImageFont.truetype('BankGthd.ttf', encoding="utf-8", size=30)  # Create the font object\


text1 = f"""{data[(data['id'] == matchId)]['home_score'].values[0]}
          """ 
text2 = f"""{data[(data['id'] == matchId)]['away_score'].values[0]}
          """ 
text3 = f"""{data[(data['id'] == matchId)]['stadium'].values[0]}
          """
w_3, h_3 = draw.textsize(text3, font=font_info)
text4 = f"""{data[(data['id'] == matchId)]['ref_main'].values[0]}
          """  
w_4, h_4 = draw.textsize(text4, font=font_info)
text5 = f"""{data[(data['id'] == matchId)]['date'].values[0]}
          """
w_5, h_5 = draw.textsize(text5, font=font_info)
text6 = f"""{data[(data['id'] == matchId)]['time'].values[0]}
          """
w_6, h_6 = draw.textsize(text6, font=font_info)


text_home = f"""{data[(data['id'] == matchId)]['home'].values[0]}
          """
text_home = textwrap.fill(text=text_home, width=15)
w_home, h_home = draw_team.textsize(text_home, font=font_info)

text_away = f"""{data[(data['id'] == matchId)]['away'].values[0]}
          """
text_away = textwrap.fill(text=text_away, width=15)
w_away, h_away = draw_away.textsize(text_away, font=font_info)


# drawing text size
draw.text((90, 50), text1, fill ="white", font = font_score, 
          align ='center') 
draw.text((530, 50), text2, fill ="white", font = font_score, 
          align ='center') 
W_3, H_3 = (1100, 1300)
draw.text(((W_3 - w_3)/2, (H_3 - h_3)/2), text3, fill ="white", font = font_info, 
          align ='center') 
W_4, H_4 = (1100, 500)
draw.text(((W_4 - w_4)/2, (H_4 - h_4)/2), text4, fill ="white", font = font_info, 
          align ='center') 
W_5, H_5 = (1100, 700)
draw.text(((W_5 - w_5)/2, (H_5 - h_5)/2), text5, fill ="white", font = font_info, 
          align ='center') 
W_6, H_6 = (1090, 900)
draw.text(((W_6 - w_6)/2, (H_6 - h_6)/2), text6, fill ="white", font = font_info, 
          align ='center')

W_T, H_T = (320, 70)
draw_team.text(((W_T - w_home)/2, (H_T - h_home)/2), text_home, fill ="white", font = font_team,
          align ='center')       
team_img = team_img.rotate(270, PIL.Image.NEAREST, expand = 1)

W_A, H_A = (320, 70)
draw_away.text(((W_A - w_away)/2, (H_A - h_away)/2), text_away, fill ="white", font = font_team,
          align ='center') 
away_img = away_img.rotate(90, PIL.Image.NEAREST, expand = 1)

Image.Image.paste(img, team_img, (45, 192))
Image.Image.paste(img, away_img, (896, 192))
width, height = img.size
basewidth = 250
wpercent = (basewidth/float(img.size[0]))
hsize = int((float(img.size[1])*float(wpercent)))
img2 = img.resize((basewidth,hsize), Image.ANTIALIAS)
img2.save("saha2.png")


goals = get_all()[3]
home_goals = goals[(goals['id'] == matchId) & (goals['variable'].str.startswith("h"))][['goal_player', 'goal_minute']].sort_values(by='goal_minute', ascending=True)
home_goals = home_goals.dropna()
away_goals = goals[(goals['id'] == matchId) & (goals['variable'].str.startswith("a"))][['goal_player', 'goal_minute']].sort_values(by='goal_minute', ascending=True)
away_goals = away_goals.dropna()

row3_1, row3_2, row3_3 = st.columns([1, 3, 1])

with row3_1:
  st.write("")
  st.markdown("<h3 style='text-align: center;'>Teknik Direktör</h1>", unsafe_allow_html=True)
  st.markdown(f"<h5 style='text-align: center;'>{data[data['id'] == matchId]['home_coach'].values[0]}</h1>", unsafe_allow_html=True)
  st.markdown("<h3 style='text-align: center;'>İlk 11</h3>", unsafe_allow_html=True)
  home_startings = startings[(startings['id'] == matchId)].loc[startings["variable"].str.startswith("h")][['starting_player']].sort_values(by='starting_player', ascending=False)
  home_subs = subs[(subs['id'] == matchId)].loc[subs["variable"].str.startswith("h")][['sub_player']].sort_values(by='sub_player', ascending=False)
  # CSS to inject contained in a string
  hide_table_row_index = """
              <style>
              tbody th {display:none}
              th {display:none}
              .blank {display:none}
              tr:hover {background-color: #018749;}
              </style>
              """

  # Inject CSS with Markdown
  st.markdown(hide_table_row_index, unsafe_allow_html=True)
  st.table(home_startings)
  st.markdown(f"<h3 style='text-align: center;'>Yedekler</h3>", unsafe_allow_html=True)
  st.table(home_subs)
  if len(home_goals) > 0:
    st.markdown(f"<h3 style='text-align: center;'>Gol(ler)</h3>", unsafe_allow_html=True)
    st.table(home_goals)



with row3_2:
  st.image(img, use_column_width=True)   # Display the image. 
  st.write("")
  lst_teams = np.unique(data[['home','away']]).tolist()
  lst_goals = []

  data_x = data[data['season'] == season]
  for j in lst_teams: 
      lst_goals.append(data_season[data_season['away'] == j]['away_score'].sum() + data_season[data_season['home'] == j]['home_score'].sum())

  lst_teams = pd.Series(lst_teams, index=lst_goals)
  lst_teams = lst_teams.reset_index().sort_values(by='index', ascending=False).iloc[:10]

  pie_data = []
  for i in range(0, len(data_hafta)):
      pie_data.append({'value': lst_teams[lst_teams.columns[0]].values.tolist()[i], 'name': lst_teams[lst_teams.columns[1]].values.tolist()[i]})

  option = {
    "backgroundColor": "#1A1F24",
    "title": {
      "text": f"{season} Sezonu En Çok Gol Atan 10 Takım",
      "left": "center",
      "top": 20,
      "textStyle": {
        "color": "#4FFFB0"
      }
    },
    "tooltip": {
      "trigger": "item"
    },
    "visualMap": {
      "show": "false",
      "min": 0,
      "max": 100,
      "inRange": {
        "colorLightness": [
          0,
          1
        ]
      }
    },
    "series": [
      {
        "type": "pie",
        "radius": "55%",
        "center": [
          "50%",
          "50%"
        ],
        "data": pie_data,
        "roseType": "radius",
        "label": {
          "color": "#ffffff"
        },
        "labelLine": {
          "lineStyle": {
            "color": "rgba(255, 255, 255, 0.3)"
          },
          "smooth": 0.2,
          "length": 10,
          "length2": 20
        },
        "itemStyle": {
          "color": "#357C3C",
          "shadowBlur": 200,
          "shadowColor": "rgba(0, 0, 0, 0.5)"
        },
        "animationType": "scale",
        "animationEasing": "elasticOut"
      }
    ]
  }

  st_echarts(
      options=option, height="600px",
  )

with row3_3:
  st.write("")
  st.markdown("<h3 style='text-align: center;'>Teknik Direktör</h1>", unsafe_allow_html=True)
  st.markdown(f"<h5 style='text-align: center;'>{data[data['id'] == matchId]['away_coach'].values[0]}</h1>", unsafe_allow_html=True)
  st.markdown(f"<h3 style='text-align: center;'>İlk 11</h3>", unsafe_allow_html=True)
  away_startings = startings[(startings['id'] == matchId)].loc[startings["variable"].str.startswith("a")][['starting_player']].sort_values(by='starting_player', ascending=False)
  away_subs = subs[(subs['id'] == matchId)].loc[subs["variable"].str.startswith("a")][['sub_player']].sort_values(by='sub_player', ascending=False)
  # CSS to inject contained in a string
  hide_table_row_index = """
              <style>
              tbody th {display:none}
              th {display:none}
              .blank {display:none}
              tr:hover {background-color: #018749;color: white;}
              </style>
              """

  # Inject CSS with Markdown
  st.markdown(hide_table_row_index, unsafe_allow_html=True)
  st.table(away_startings) 
  st.markdown(f"<h3 style='text-align: center;'>Yedekler</h3>", unsafe_allow_html=True)
  st.table(away_subs)
  if len(away_goals) > 0:
    st.markdown(f"<h3 style='text-align: center;'>Gol(ler)</h3>", unsafe_allow_html=True)
    st.table(away_goals)

st.write(matchId)

>>>>>>> origin/main
