from tkinter import CENTER
from streamlit_echarts import st_echarts
import streamlit as st
import pandas as pd
import numpy as np
import functools

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
subs = get_all()[5]

df['total_goals'] = df['home_score']+df['away_score']


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
match_id = get_match_id(param_1, param_2)[0]


#SEZONA GÖRE TAKIMLARIN GOL SAYILARI BAR CHART
#------------------------------------------------------------------------------------

goals = get_all()[3]

lst_teams = np.unique(df[['home','away']]).tolist()
lst_goals = []

choose_season = st.selectbox(
    'Hangi Sezon?',
    df['season'].unique().tolist())

df = df[df['season'] == choose_season]
for j in lst_teams: 
    lst_goals.append(df[df['away'] == j]['away_score'].sum() + df[df['home'] == j]['home_score'].sum())

lst_teams = pd.Series(lst_teams, index=lst_goals)
lst_teams = lst_teams.reset_index().sort_values(by='index', ascending=False).iloc[:10]



options1 = {
    "xAxis": {
        "type": "category",
        "data": lst_teams[lst_teams.columns[1]].values.tolist(),
        "axisLabel": {
        "interval": 0,
        "rotate": 30
      }

    },
    "yAxis": {"type": "value"},
    "dataZoom": [
    {
      "type": "inside"
    }
  ],
    "series": [{"data": lst_teams[lst_teams.columns[0]].values.tolist(), "type": "bar"}],
}


if st.button('Getir'):
    st_echarts(options=options1, height="500px")


#Pie Chart Olusturma

pie_data = []

for i in range(0, len(lst_teams)):
    pie_data.append({'value': lst_teams[lst_teams.columns[0]].values.tolist()[i], 'name': lst_teams[lst_teams.columns[1]].values.tolist()[i]})



option = {
  "backgroundColor": "#2c343c",
  "title": {
    "text": "Customized Pie",
    "left": "center",
    "top": 20,
    "textStyle": {
      "color": "#ccc"
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
      "name": "",
      "type": "pie",
      "radius": "55%",
      "center": [
        "50%",
        "50%"
      ],
      "data": pie_data,
      "roseType": "radius",
      "label": {
        "color": "rgba(255, 255, 255, 0.3)"
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
        "color": "#c23531",
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

dataframes = [df, startings, subs]
df_final = functools.reduce(lambda left,right: pd.merge(left,right,on='id'), dataframes)
df_final = df_final.groupby(['id', 'season','exhibition_x','starting_player']).size().reset_index(name='total_goals')



data = get_all()[0]
st.write(startings)

row3_1, row3_2, row3_3, row3_4, row3_5 = st.columns([1, .1, 1, .1, 1])

with row3_1:
  season = st.selectbox("", data['season'].unique().tolist())

with row3_3:
  hafta = st.selectbox("", data['hafta'].unique().tolist())

data = data[(data['season'] == season) & (data['hafta'] == hafta)]

with row3_5:
  karsilasma = st.selectbox("", data['exhibition'].unique().tolist())

matchId = data[(data['season'] == season) & (data['hafta'] == hafta) & (data['exhibition'] == karsilasma)]['id'].values[0]


from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 

img = Image.open("saha.png")    #this is the image we want to add text to
draw = ImageDraw.Draw(img)  # Create a drawing object that is used to draw on the new image.
font_score = ImageFont.truetype('BankGthd.ttf', encoding="utf-8", size=120)  # Create the font object\
font_info = ImageFont.truetype('Roboto-Regular.ttf', encoding="utf-8", size=30) 


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
 
width, height = img.size
basewidth = 250
wpercent = (basewidth/float(img.size[0]))
hsize = int((float(img.size[1])*float(wpercent)))
img2 = img.resize((basewidth,hsize), Image.ANTIALIAS)
img2.save("saha2.png")


row3_1, row3_2, row3_3 = st.columns([1, 3, 1])

with row3_1:
  st.write("")
  st.markdown(f"<h3 style='text-align: center;'>{data[(data['id'] == matchId)]['home'].values[0]}</h3>", unsafe_allow_html=True)
  home_startings = startings[(startings['id'] == matchId)].loc[startings["variable"].str.startswith("h")][['starting_player']].sort_values(by='starting_player', ascending=False)
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

with row3_2:
  st.image(img, use_column_width=True)   # Display the image. 



with row3_3:
  st.write("")
  st.markdown(f"<h3 style='text-align: center;'>{data[(data['id'] == matchId)]['away'].values[0]}</h3>", unsafe_allow_html=True)
  away_startings = startings[(startings['id'] == matchId)].loc[startings["variable"].str.startswith("a")][['starting_player']].sort_values(by='starting_player', ascending=False)
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
  st.table(away_startings)  

st.write(matchId)

