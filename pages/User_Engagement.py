#..............................UI design of User Engagement Page.....................................

import streamlit as st # for data visualization in the web application
import pandas as pd # for dataframe manipulation
import plotly.express as px # for data visualization
from googleapiclient.discovery import build # for data extraction via API

#Importing Images to user interface (UI)
st.set_page_config(
    page_title="Rukshan Yoga Studio | User Engagement Analysis",
    page_icon="🕉️",
    layout="wide"
)

st.markdown(
    "<div style='text-align:left;margin-bottom:2px'>"
    "<h1>User Engagement | Rukshan Yoga Studio</h1>"
    "</div>",
    unsafe_allow_html=True
)

#.......Extraction of Rukshan Yoga YouTube channel user engagement data..................


st.markdown(
    "<div style='text-align:left'>"
    "<h1 style='color:red; font-weight:bold;'>YouTube</h1>"
    "</div>",
    unsafe_allow_html=True
)

api_key = 'AIzaSyDq2D0F4DrXjqKC623DcYFUDSR90VMwgic'  


channel_ids = ['UCWTn7VBGs6Om5RyVry18NRA', # Rukshan Yoga
               'UCfTCfcZwZ9U0jMO-6fVEYoQ', # Arogya
               'UC2oL57TkQp6bMfz-1wa5fqg', # Uthpola
              ] 


youtube = build('youtube', 'v3', developerKey=api_key)

def get_channel_stats(youtube, channel_ids):
    all_data = []
    request = youtube.channels().list(
                part='snippet,contentDetails,statistics',
                id=','.join(channel_ids))
    response = request.execute() 
    
    for i in range(len(response['items'])):
        data = dict(Channel_name = response['items'][i]['snippet']['title'],
                    Subscribers = response['items'][i]['statistics']['subscriberCount'],
                    Views = response['items'][i]['statistics']['viewCount'],
                    Total_videos = response['items'][i]['statistics']['videoCount'],
                    playlist_id = response['items'][i]['contentDetails']['relatedPlaylists']['uploads'])
        all_data.append(data)
    
    return all_data

channel_statistics = get_channel_stats(youtube, channel_ids)

channel_data = pd.DataFrame(channel_statistics)

channel_data['Subscribers'] = pd.to_numeric(channel_data['Subscribers'])
channel_data['Views'] = pd.to_numeric(channel_data['Views'])
channel_data['Total_videos'] = pd.to_numeric(channel_data['Total_videos'])

playlist_id = channel_data.loc[channel_data['Channel_name']=='Rukshan Yoga Studio', 'playlist_id'].iloc[0]

def get_video_ids(youtube, playlist_id):
    
    request = youtube.playlistItems().list(
                part='contentDetails',
                playlistId = playlist_id,
                maxResults = 50)
    response = request.execute()
    
    video_ids = []
    
    for i in range(len(response['items'])):
        video_ids.append(response['items'][i]['contentDetails']['videoId'])
        
    next_page_token = response.get('nextPageToken')
    more_pages = True
    
    while more_pages:
        if next_page_token is None:
            more_pages = False
        else:
            request = youtube.playlistItems().list(
                        part='contentDetails',
                        playlistId = playlist_id,
                        maxResults = 50,
                        pageToken = next_page_token)
            response = request.execute()
    
            for i in range(len(response['items'])):
                video_ids.append(response['items'][i]['contentDetails']['videoId'])
            
            next_page_token = response.get('nextPageToken')
        
    return video_ids

video_ids = get_video_ids(youtube, playlist_id)

def get_video_details(youtube, video_ids):
    all_video_stats = []
    
    for i in range(0, len(video_ids), 50):
        request = youtube.videos().list(
                    part='snippet,statistics',
                    id=','.join(video_ids[i:i+50]))
        response = request.execute()
        
        for video in response['items']:
            video_stats = dict(Title = video['snippet']['title'],
                               Published_date = video['snippet']['publishedAt'],
                               Views = video['statistics']['viewCount'],
                               Likes = video['statistics']['likeCount'],
                               #Dislikes = video['statistics']['dislikeCount'],
                               Comments = video['statistics']['commentCount']
                               )
            all_video_stats.append(video_stats)
    
    return all_video_stats

video_details = get_video_details(youtube, video_ids)

video_data = pd.DataFrame(video_details)

video_data['Published_date'] = pd.to_datetime(video_data['Published_date']).dt.date
video_data['Views'] = pd.to_numeric(video_data['Views'])
video_data['Likes'] = pd.to_numeric(video_data['Likes'])
video_data['Views'] = pd.to_numeric(video_data['Views'])

video_data['Comments'] = video_data['Comments'].astype('int')

top10_videos = video_data.sort_values(by='Views', ascending=False).head(10)

video_data['Month'] = pd.to_datetime(video_data['Published_date']).dt.strftime('%b')

videos_per_month = video_data.groupby('Month', as_index=False).size()

sort_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
             'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

videos_per_month.index = pd.CategoricalIndex(videos_per_month['Month'], categories=sort_order, ordered=True)

videos_per_month = videos_per_month.sort_index()
videos_per_month['Months'] = ['Jan', 'Mar', 'May', 'Jun','Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# KPIs visualization

channel_data_alk = channel_data
ch_al = channel_data_alk.set_index("Channel_name")

subscibers = ch_al['Subscribers']['Rukshan Yoga Studio']
total_likes = video_data['Likes'].sum()
total_comments = video_data['Comments'].sum()

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.markdown(
    f'<h1 style="font-size:30px; text-transform:uppercase">Subscribers <span style="color:red;padding-left:10px;">{subscibers}</span></h1>',
    unsafe_allow_html=True
    )
with middle_column:
    st.markdown(
    f'<h1 style="font-size:30px;text-transform:uppercase">Total Likes <span style="color:red;padding-left:10px;">{total_likes}</span></h1>',
    unsafe_allow_html=True
    )
with right_column:
    st.markdown(
    f'<h1 style="font-size:30px;text-transform:uppercase">Total Comments<span style="color:red;padding-left:10px;">{total_comments}</span></h1>',
    unsafe_allow_html=True
    )

#........................YouTube Data Visualization...................................

# chart of posted videos in each month 
vids_per_month_chart = videos_per_month.groupby(by=["Months"]).sum()[["size"]]
fig_vids_month= px.line(
    vids_per_month_chart,
    y= "size",
    x= videos_per_month.index,
    title="<b>Number of Posted Videos in each month</b>",
    color_discrete_sequence=["#d62728"] * len(vids_per_month_chart),
    template="plotly_dark",
    text="size",
    markers=True
)

#top10 videos chart
top10_vids_chart = top10_videos.groupby(by=["Title"]).sum()[["Views"]]
fig_top10_vids= px.bar(
    top10_vids_chart,
    x= "Views",
    y= top10_videos['Title'],
    title="<b>Top Ten Videos with most number of Views</b>",
    color_discrete_sequence=["#d62728"] * len(top10_vids_chart),
    template="plotly_dark",
    text_auto=True
)

# Competitor analysis charts
sub_chart = channel_data.groupby(by=["Channel_name"]).sum()[["Subscribers"]]
fig_subs= px.bar(
    sub_chart,
    x=sub_chart.index,
    y="Subscribers",
    title="<b>Subscribers</b>",
    color_discrete_sequence=["#d62728"] * len(sub_chart),
    template="plotly_dark",
    text_auto=True
)

view_chart = channel_data.groupby(by=["Channel_name"]).sum()[["Views"]]
fig_views = px.bar(
    view_chart,
    x=view_chart.index,
    y="Views",
    title="<b>Views</b>",
    color_discrete_sequence=["#d62728"] * len(view_chart),
    template="plotly_dark",
    text_auto=True
)

vid_chart = channel_data.groupby(by=["Channel_name"]).sum()[["Total_videos"]]
fig_vids = px.bar(
    vid_chart,
    x=vid_chart.index,
    y="Total_videos",
    title="<b>Total Videos</b>",
    color_discrete_sequence=["#d62728"] * len(vid_chart),
    template="plotly_dark",
    text_auto=True
)


st.plotly_chart(fig_top10_vids,use_container_width=True)
st.plotly_chart(fig_vids_month,use_container_width=True)

st.markdown("<h3 style='text-align: left;'>COMPETITOR ANALYSIS</h3>", unsafe_allow_html=True)

st.dataframe(channel_data[['Channel_name','Subscribers','Views','Total_videos']])

left_column,middle_column,right_column = st.columns(3)
left_column.plotly_chart(fig_subs, use_container_width=True)
middle_column.plotly_chart(fig_vids, use_container_width=True)
right_column.plotly_chart(fig_views,use_container_width=True)

#..................Facebook Page Data Analysis and Data Visualization.................
st.markdown(
    "<div style='text-align:left'>"
    "<h1 style='color:#4267B2; font-weight:bold;'>Meta</h1>"
    "</div>",
    unsafe_allow_html=True
)

#KPIs visualization

followers = "2889"

st.markdown(f'<h1 style="font-size:30px; text-transform:uppercase; padding-bottom:20px">FACEBOOK PAGE FOLLOWERS <span style="color:blue;padding-left:10px;">{followers}</span></h1>',unsafe_allow_html=True)

df_fb_ue_summary = pd.read_json('https://raw.githubusercontent.com/GehanPasindhu/datas/main/DataSets/fbEngSummery.json')
df_fb_al_ue = pd.read_json('https://raw.githubusercontent.com/GehanPasindhu/datas/main/DataSets/likecomment.json')

#......................Facebook User Engagement........................

fb_al_likes_chart = df_fb_al_ue.groupby(by=["post_id"]).sum()[["likes"]]
fig_fb_al_likes= px.bar(
    fb_al_likes_chart,
    x=df_fb_al_ue.index,
    y="likes",
    title="<b>Likes recieved for each post</b>",
    color_discrete_sequence=["#0083B8"] * len(fb_al_likes_chart),
    template="plotly_dark",
    text_auto=True,
)

fb_al_shares_chart = df_fb_al_ue.groupby(by=["post_id"]).sum()[["shares"]]
fig_fb_al_shares= px.bar(
    fb_al_shares_chart,
    x=df_fb_al_ue.index,
    y="shares",
    title="<b>Shares recieved for each post</b>",
    color_discrete_sequence=["#0083B8"] * len(fb_al_shares_chart ),
    template="plotly_dark",
    text_auto=True
)

fb_al_comments_chart = df_fb_al_ue.groupby(by=["post_id"]).sum()[["comments"]]
fig_fb_al_comments= px.bar(
    fb_al_comments_chart,
    x=df_fb_al_ue.index,
    y="comments",
    title="<b>Comments recieved for each post</b>",
    color_discrete_sequence=["#0083B8"] * len(fb_al_comments_chart ),
    template="plotly_dark",
    text_auto=True
)


st.markdown('For user engagement analysis, only last 100 posts which posted on each page were considered')

st.plotly_chart(fig_fb_al_likes,use_container_width=True)
st.plotly_chart(fig_fb_al_shares,use_container_width=True)
st.plotly_chart(fig_fb_al_comments,use_container_width=True)


#...............................Facebook Competitor Analysis..................................

st.markdown("<h3 style='text-align: left;'>COMPETITOR ANALYSIS</h3>", unsafe_allow_html=True)

fb_summary_ue_lchart = df_fb_ue_summary.groupby(by=["Product"]).sum()[["Likes"]]
fig_fb_lsummary= px.bar(
    fb_summary_ue_lchart,
    x=fb_summary_ue_lchart.index,
    y="Likes",
    title="<b>Likes</b>",
    color_discrete_sequence=["#0083B8"] * len(fb_summary_ue_lchart),
    template="plotly_dark",
    text_auto=True
)

fb_summary_ue_schart = df_fb_ue_summary.groupby(by=["Product"]).sum()[["Shares"]]
fig_fb_ssummary= px.bar(
    fb_summary_ue_schart,
    x=fb_summary_ue_schart.index,
    y="Shares",
    title="<b>Shares</b>",
    color_discrete_sequence=["#0083B8"] * len(fb_summary_ue_schart),
    template="plotly_dark",
    text_auto=True
)

fb_summary_ue_cchart = df_fb_ue_summary.groupby(by=["Product"]).sum()[["Comments"]]
fig_fb_csummary= px.bar(
    fb_summary_ue_cchart,
    x=fb_summary_ue_cchart.index,
    y="Comments",
    title="<b>Comments</b>",
    color_discrete_sequence=["#0083B8"] * len(fb_summary_ue_cchart ),
    template="plotly_dark",
    text_auto=True
)

st.markdown('For competitor analysis, only last 18 posts which posted on each page were considered')

col9,col10,col11= st.columns(3)

col9.plotly_chart(fig_fb_lsummary,use_container_width=True)
col10.plotly_chart(fig_fb_ssummary,use_container_width=True)
col11.plotly_chart(fig_fb_csummary,use_container_width=True)

#......................Instagram User Engagement...................



st.markdown(
    "<div style='text-align:left'>"
    "<h1 style='color:#C13584; font-weight:bold;'>Instagram</h1>"
    "</div>",
    unsafe_allow_html=True
)

df_insta_ue_summary = pd.read_json('https://raw.githubusercontent.com/GehanPasindhu/datas/main/DataSets/ueig.json')
df_insta_al_ue = pd.read_json('https://raw.githubusercontent.com/GehanPasindhu/datas/main/DataSets/instalasteng.json')


# https://raw.githubusercontent.com/GehanPasindhu/datas/main/DataSets/ue_Ig.json
# KPIs Visualization

followers = df_insta_ue_summary['Followers'][0]
total_likes_insta = df_insta_ue_summary['Total Likes'][0]
total_comments_insta = df_insta_ue_summary['Total Comments'][0]

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.markdown(
    f'<h1 style="font-size:30px; text-transform:uppercase">Followers <span style="color:#C13584;padding-left:10px;">{followers}</span></h1>',
    unsafe_allow_html=True
    )
with middle_column:
    st.markdown(
    f'<h1 style="font-size:30px;text-transform:uppercase">Total Likes <span style="color:#C13584;padding-left:10px;">{total_likes_insta}</span></h1>',
    unsafe_allow_html=True
    )
with right_column:
    st.markdown(
    f'<h1 style="font-size:30px;text-transform:uppercase">Total Comments<span style="color:#C13584;padding-left:10px;">{total_comments_insta}</span></h1>',
    unsafe_allow_html=True
    )

#.............Instagram User engagement and Data Visualization..................

insta_like_ue_chart = df_insta_al_ue.groupby(by=["Post"]).sum()[["Likes"]]
fig_insta_likes= px.bar(
    insta_like_ue_chart,
    x=df_insta_al_ue["Post"],
    y="Likes",
    title="<b>Number of Likes received for last 20 posts</b>",
    color_discrete_sequence=["#C13584"] * len(insta_like_ue_chart ),
    template="plotly_dark",
    text_auto=True
)

insta_fol_sum_chart = df_insta_ue_summary.groupby(by=["Product"]).sum()[["Followers"]]
fig_insta_fol= px.bar(
    insta_fol_sum_chart,
    x=df_insta_ue_summary["Product"],
    y="Followers",
    title="<b>Instagram Followers</b>",
    color_discrete_sequence=["#C13584"] * len(insta_fol_sum_chart),
    template="plotly_dark",
    text_auto=True
)

insta_like_sum_chart = df_insta_ue_summary.groupby(by=["Product"]).sum()[["Total Likes"]]
fig_insta_sum_likes= px.bar(
    insta_like_sum_chart,
    x=df_insta_ue_summary["Product"],
    y="Total Likes",
    title="<b>Total Likes for Instagram Posts</b>",
    color_discrete_sequence=["#C13584"] * len(insta_like_sum_chart),
    template="plotly_dark",
    text_auto=True
)

insta_comments_sum_chart = df_insta_ue_summary.groupby(by=["Product"]).sum()[["Total Comments"]]
fig_insta_sum_comments= px.bar(
    insta_comments_sum_chart,
    x=df_insta_ue_summary["Product"],
    y="Total Comments",
    title="<b>Total Comments for Instagram Posts</b>",
    color_discrete_sequence=["#C13584"] * len(insta_comments_sum_chart),
    template="plotly_dark",
    text_auto=True
)

st.plotly_chart(fig_insta_likes,use_container_width=True,)

st.markdown("<h3 style='text-align: left;'>COMPETITOR ANALYSIS</h3>", unsafe_allow_html=True)

col16,col17,col18= st.columns(3)

col16.plotly_chart(fig_insta_fol,use_container_width=True)
col17.plotly_chart(fig_insta_sum_likes,use_container_width=True)
col18.plotly_chart(fig_insta_sum_comments,use_container_width=True)


st.markdown("<p style='text-align: right; font-style:italic'>Arogya page doesnt have an instagram page *</p>", unsafe_allow_html=True)

hide_stremlit_style = """
<style>
#MainMenu{visibility:hidden}
footer{visibility:hidden}
</style>

"""
st.markdown(hide_stremlit_style,unsafe_allow_html=True)