# ..............................UI design of Polarity Analysis.....................................

# Importing necessary Libraries

import pandas as pd  # for Dataframes manipulation
import numpy as np  # for arrays manipulation
import plotly.express as px  # for data visualization
from textblob import TextBlob  # For natural language processing
import streamlit as st  # for UI design

st.set_page_config(
    page_title="Rukshan Yoga Studio | Polarity Analysis",
    page_icon="🕉️",
    layout="wide"
)

st.markdown(
    "<div style='text-align:left;margin-bottom:2px'>"
    "<h1>Polarity Analysis | Rukshan Yoga Studio</h1>"
    "</div>",
    unsafe_allow_html=True
)

# ....................Polarity Analysis of YouTube Comments..............................

st.markdown(
    "<div style='text-align:left'>"
    "<h1 style='color:red; font-weight:bold;'>YouTube</h1>"
    "</div>",
    unsafe_allow_html=True
)


df_yt_com = pd.read_json(
    'https://raw.githubusercontent.com/GehanPasindhu/datas/main/DataSets/youtubecomments.json')

# Polarity Analysis using NLP

comments = df_yt_com["Comment"]
polarity = []

for comment in comments:
    review_1 = TextBlob(comment)
    rev1 = review_1.sentiment.polarity
    polarity.append(rev1)

x = {"No": np.arange(len(comments)), "Comments": comments,
     "Polarity": polarity}

df_yt_pol = pd.DataFrame(x)

# KPIs
avg_polarity_yt = df_yt_pol['Polarity'].sum()/len(polarity)

st.markdown(
    f'<h1 style="font-size:25px;">Average Polarity of  YouTube Channel <span style="color:#33ff33;padding-left:10px;">{avg_polarity_yt} *</span></h1>'
    '<p>For the comments received for the <b style="color:red"; font-size:20px; padding-left:10px; padding-right:10px>Top 10 Most Viewed </b> YouTube Videos *</p>',
    unsafe_allow_html=True
    )

yt_polarity_chart = df_yt_pol.groupby(by=["No"]).sum()[["Polarity"]]
fig_yt_pol = px.bar(
    yt_polarity_chart,
    x=df_yt_pol["No"],
    y="Polarity",
    title="<b>Polarity of the comments received for the top 10 YouTube video with the most number of views</b>",
    color_discrete_sequence=["#d62728"] * len(yt_polarity_chart),
    template="plotly_dark",
    text_auto=True
)

st.plotly_chart(fig_yt_pol, use_container_width=True,)


# ....................Polarity Analysis of Facebook Comments..............................

st.markdown(
    "<div style='text-align:left'>"
    "<h1 style='color:#4267B2; font-weight:bold;'>Meta</h1>"
    "</div>",
    unsafe_allow_html=True
)


df_fb_com = pd.read_json(
    'https://raw.githubusercontent.com/GehanPasindhu/datas/main/DataSets/fbcomments.json')

# Polarity Analysis using NLP

comments_fb = df_fb_com["Comment"]
polarity_fb = []

for comment_fb in comments_fb:
    review_fb1 = TextBlob(comment_fb)
    rev_fb1 = review_fb1.sentiment.polarity
    polarity_fb.append(rev_fb1)

y = {"No": np.arange(len(comments_fb)),
     "Comments": comments_fb, "Polarity": polarity_fb}

df_fb_pol = pd.DataFrame(y)

# KPIs
avg_polarity_fb = df_fb_pol['Polarity'].sum()/len(polarity_fb)

st.markdown(
    f'<h1 style="font-size:25px;">Average Polarity of Facebook <span style="color:#33ff33;padding-left:10px;">{avg_polarity_yt} *</span></h1>'
    '<p>For the comments received for last Facebook page posts *</p>',
    unsafe_allow_html=True
    )

fb_polarity_chart = df_fb_pol.groupby(by=["No"]).sum()[["Polarity"]]
fig_fb_pol = px.bar(
    fb_polarity_chart,
    x=df_fb_pol["No"],
    y="Polarity",
    title="<b>Polarity of the comments received for the last twenty Facebook page posts</b>",
    color_discrete_sequence=["#0083B8"] * len(yt_polarity_chart),
    template="plotly_dark",
    text_auto=True
)

st.plotly_chart(fig_fb_pol, use_container_width=True,)

hide_stremlit_style = """
<style>
#MainMenu{visibility:hidden}
footer{visibility:hidden}
</style>

"""
st.markdown(hide_stremlit_style, unsafe_allow_html=True)
