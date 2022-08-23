#..............................UI design of Information Diffusion Page.....................................

# Importing necessary libraries

import streamlit as st # for User Interface design and visualization
import networkx as nx # for networkx graphs visualization
import matplotlib.pyplot as plt #for data manipulation and visualization of social media networks
import pandas as pd # for data frames manipulation

import warnings
warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="Rukshan Yoga Studio | Information Diffusion",
    page_icon="🕉️",
    layout="wide"
)

st.markdown(
    "<div style='text-align:left;margin-bottom:2px'>"
    "<h1>Information Diffusion | Rukshan Yoga Studio</h1>"
    "</div>",
    unsafe_allow_html=True
)

#.....................Polarity analysis of Youtube channel comments...................
st.markdown(
    "<div style='text-align:left'>"
    "<h1 style='color:red; font-weight:bold;'>YouTube</h1>"
    "</div>",
    unsafe_allow_html=True
)

#Data extraction 

df_full = pd.read_json("https://raw.githubusercontent.com/GehanPasindhu/datas/main/DataSets/infoDfuYT.json")

df = df_full[['Commented by','Replied by']]

df = df.replace(to_replace="",
           value="Rukshan Yoga Sri Lanka")

# Visualization of Networkx Graphs

G = nx.from_pandas_edgelist(df,source='Commented by',target="Replied by",create_using = nx.Graph())
fig_nx=nx.draw(G,with_labels=True,font_weight='normal',font_size=6)
pos = nx.spring_layout(G)
betCent = nx.betweenness_centrality(G, normalized=True, endpoints=True)
node_color = [20000.0 * G.degree(v) for v in G]
node_size = [v * 10000 for v in betCent.values()]
plt.figure(figsize=(20,20))
fig_bet= nx.draw_networkx(G, pos=pos, with_labels=True,
node_color=node_color,
node_size=node_size )
x = sorted(betCent, key=betCent.get, reverse=True)[:8]


pos2 = nx.spring_layout(G)
betCent2 = nx.degree_centrality(G)
node_color2 = [20000.0 * G.degree(v) for v in G]
node_size2 = [v * 10000 for v in betCent2.values()]
plt.figure(figsize=(20,20))
fig_deg = nx.draw_networkx(G, pos=pos2, with_labels=True,
node_color=node_color2,
node_size=node_size2 )

y = sorted(betCent2, key=betCent2.get, reverse=True)[:8]
degree = pd.DataFrame({"Identified list of Influencers":y})

pos3 = nx.spring_layout(G)
betCent3 = nx.degree_centrality(G)
node_color3 = [20000.0 * G.degree(v) for v in G]
node_size3 = [v * 10000 for v in betCent3.values()]
plt.figure(figsize=(20,20))
nx.draw_networkx(G, pos=pos3, with_labels=True,
node_color=node_color3,
node_size=node_size3)
z = sorted(betCent, key=betCent.get, reverse=True)[:8]


pos4 = nx.spring_layout(G)
betCent4 = nx.eigenvector_centrality(G)
node_color4 = [20000.0 * G.degree(v) for v in G]
node_size4 = [v * 10000 for v in betCent4.values()]
plt.figure(figsize=(20,20))
fig_ec = nx.draw_networkx(G, pos=pos4, with_labels=True,
node_color=node_color4,
node_size=node_size4 )
sorted(betCent, key=betCent.get, reverse=True)[:8]

col3,col4 =st.columns(2)
with col3:
    st.subheader("INFLUENCERS")
    st.table(degree)
with col4:
    st.subheader("EIGENVECTOR CENTRALITY")
    st.pyplot(fig_ec, use_container_width=True)


col1,col2 =st.columns(2)
with col1:
    st.subheader("DEGREE CENTRALITY")
    st.image('degreeCentality.png')
with col2:
    st.subheader("BETWEENESS CENTRALITY")
    st.image('betweenessCentrality.png')


st.set_option('deprecation.showPyplotGlobalUse', False)

hide_stremlit_style = """
<style>
#MainMenu{visibility:hidden}
footer{visibility:hidden}
</style>

"""
st.markdown(hide_stremlit_style,unsafe_allow_html=True)
