#..............................UI design of Keyword Analysis.....................................

#Importing necessary Libraries

import pandas as pd # for Dataframes manipulation
import numpy as np # for arrays manipulation
import seaborn as sns # foe data visualization
import plotly.express as px # for data visualization
import matplotlib.pyplot as plt # for data visualization
from PIL import Image # to import images to User Interface (UI)
import requests # to assist importing images to User Interface (UI)
from io import BytesIO # to assist importing images to User Interface (UI)
from requests_html import HTMLSession # to extract the words from YouTube channel
from rake_nltk import Rake # to extract keywords
from fuzzywuzzy import fuzz #for hashtag rating
import streamlit as st # for UI design

st.set_page_config(
    page_title="Rukshan Yoga Studio | Keyword Analysis",
    page_icon="🕉️",
    layout="wide"
)

st.markdown(
    "<div style='text-align:left;margin-bottom:2px'>"
    "<h1>Keyword Analysis | Rukshan Yoga Studio</h1>"
    "</div>",
    unsafe_allow_html=True
)

#.................... Hashtag Analysis of YouTube............................
st.markdown(
    "<div style='text-align:left'>"
    "<h1 style='color:red; font-weight:bold;'>YouTube</h1>"
    "</div>",
    unsafe_allow_html=True
)

#text extraction from YouTube page

def extract_text_yt():
    s_yt = HTMLSession()
    url_yt = 'https://www.youtube.com/channel/UCWTn7VBGs6Om5RyVry18NRA'
    response_yt = s_yt.get(url_yt)
    return response_yt.html.find(first=True).text

# Separating keywords 

df_yt = pd.read_json("https://raw.githubusercontent.com/GehanPasindhu/datas/main/DataSets/ytkeywords.json")

#Finding the Fuzzywuzzy rating for Hashtags

hashtags_yt = ['#yoga','#mirissa','#srilanka','health','relax','#yogasrilanka','#mathara','#nature','#love','#peace','#kundalani','#online','#onlineclass','#teachertraining','#retreat','#officeyoga','#visit','#rukshan','#rukshanyoga']
rating_yt = []

for words_yt in hashtags_yt:
    ratio_yt = fuzz.WRatio(words_yt,df_yt)
    rating_yt.append(ratio_yt)

df_com_yt = pd.DataFrame({'Hashtags':hashtags_yt,
                     'Fuzzywuzzy Rating':rating_yt })  

# Visualization rating for top 20 YouTube Hashtags

hashtags_chart_yt = df_com_yt.groupby(by=["Hashtags"]).sum()[["Fuzzywuzzy Rating"]]
fig_keyword_yt= px.bar(
    hashtags_chart_yt,
    x=hashtags_chart_yt.index,
    y="Fuzzywuzzy Rating",
    title="<b>YouTube channel Hashtag Rating for top 20 Hashtags</b>",
    color_discrete_sequence=["#d62728"] * len(hashtags_chart_yt),
    template="plotly_dark",
    text_auto=True,
    #color="Fuzzywuzzy Rating"
)

st.plotly_chart(fig_keyword_yt,use_container_width=True)

#.................... Hashtag Analysis of Facebook............................
st.markdown(
    "<div style='text-align:left'>"
    "<h1 style='color:#4267B2; font-weight:bold;'>Meta</h1>"
    "</div>",
    unsafe_allow_html=True
)

#text extraction from Facebook page

def extract_text_fb():
    s_fb = HTMLSession()
    url_fb = 'https://www.facebook.com/RukshanYoga.SriLanka'
    response_fb = s_fb.get(url_fb)
    return response_fb.html.find(first=True).text

# Separating keywords 

df_fb = pd.read_json("https://raw.githubusercontent.com/GehanPasindhu/datas/main/DataSets/fbkeywords.json")

#Finding the Fuzzywuzzy rating for Hashtags

hashtags_fb = ['#yoga','#mirissa','#srilanka','health','relax','#yogasrilanka','#mathara','#nature','#love','#peace','#kundalani','#online','#onlineclass','#teachertraining','#retreat','#officeyoga','#visit','#rukshan','#rukshanyoga']
rating_fb = []

for words_fb in hashtags_fb:
    ratio_fb = fuzz.WRatio(words_fb,df_fb)
    rating_fb.append(ratio_fb)

df_com_fb = pd.DataFrame({'Hashtags':hashtags_fb,
                     'Fuzzywuzzy Rating':rating_fb})  


hashtags_chart_fb = df_com_fb.groupby(by=["Hashtags"]).sum()[["Fuzzywuzzy Rating"]]
fig_keyword_fb= px.bar(
    hashtags_chart_fb,
    x=hashtags_chart_fb.index,
    y="Fuzzywuzzy Rating",
    title="<b>Facebook page Hashtag Rating for top 20 Hashtags</b>",
    color_discrete_sequence=["#0083B8"] * len(hashtags_chart_fb),
    template="plotly_dark",
    text_auto=True,
    #color="Fuzzywuzzy Rating"
)

st.plotly_chart(fig_keyword_fb,use_container_width=True)

#.................... Hashtag Analysis of Instagram............................

st.markdown(
    "<div style='text-align:left'>"
    "<h1 style='color:#C13584; font-weight:bold;'>Instagram</h1>"
    "</div>",
    unsafe_allow_html=True
)

#text extraction from Instagram page

def extract_text_in():
    s_in = HTMLSession()
    url_in = 'https://www.instagram.com/rukshanyoga_srilanka/'
    response_in = s_in.get(url_in)
    return response_in.html.find(first=True).text

# Separating keywords 

df_in = pd.read_json("https://raw.githubusercontent.com/GehanPasindhu/datas/main/DataSets/igkeywords.json")

#Finding the Fuzzywuzzy rating for Hashtags

hashtags_in = ['#yoga','#mirissa','#srilanka','health','relax','#yogasrilanka','#mathara','#nature','#love','#peace','#kundalani','#online','#onlineclass','#teachertraining','#retreat','#officeyoga','#visit','#rukshan','#rukshanyoga']
rating_in = []

for words_in in hashtags_in:
    ratio_in = fuzz.WRatio(words_in,df_in)
    rating_in.append(ratio_in)

df_com_in = pd.DataFrame({'Hashtags':hashtags_in,
                     'Fuzzywuzzy Rating':rating_in})  


hashtags_chart_in = df_com_in.groupby(by=["Hashtags"]).sum()[["Fuzzywuzzy Rating"]]
fig_keyword_in= px.bar(
    hashtags_chart_in,
    x=hashtags_chart_in.index,
    y="Fuzzywuzzy Rating",
    title="<b>Instagram page Hashtag Rating for top 20 Hashtags</b>",
    color_discrete_sequence=["#9467bd"] * len(hashtags_chart_in),
    template="plotly_dark",
    text_auto=True,
    #color="Fuzzywuzzy Rating"
)

st.plotly_chart(fig_keyword_in,use_container_width=True)


hide_stremlit_style = """
<style>
#MainMenu{visibility:hidden}
footer{visibility:hidden}
</style>

"""
st.markdown(hide_stremlit_style,unsafe_allow_html=True)