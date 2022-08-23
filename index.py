# ...............Import Libraries..................
import streamlit as st  # for User Interface (UI) design

st.set_page_config(
    page_title="Rukshan Yoga Studio",
    page_icon="🕉️",
    layout="wide"
)

st.markdown(
    "<div style='text-align:center;margin-bottom:20px'>"
    "<h1>Social Media Analytics Dashboard</h1>"
    "<h2>Rukshan Yoga Studio - Mirissa</h2>"
    "<img src='https://rukshanyoga.lk/wp-content/uploads/2021/01/Logo.svg' style='width:300px; margin-top:5px;'>"
    "</div>",
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4, gap="small")
with col1:
    st.markdown(
        "<div style='text-align:center; border:1px solid; padding:20px; border-radius:10px'>"
        "<a href='/User_Engagement' target='_self' style='color:#f1f1f1; text-decoration:none'>User Engagment Analysis</a>"
        "</div>",
        unsafe_allow_html=True
    )
with col2:
    st.markdown(
        "<div style='text-align:center; border:1px solid; padding:20px; border-radius:10px'>"
        "<a href='/User_Engagement' target='_self' style='color:#f1f1f1; text-decoration:none'>Information Diffusion Analysis</a>"
        "</div>",
        unsafe_allow_html=True
    )
with col3:
    st.markdown(
        "<div style='text-align:center; border:1px solid; padding:20px; border-radius:10px'>"
        "<a href='/User_Engagement' target='_self' style='color:#f1f1f1; text-decoration:none'>Keyword Analysis</a>"
        "</div>",
        unsafe_allow_html=True
    )
with col4:
    st.markdown(
        "<div style='text-align:center; border:1px solid; padding:20px; border-radius:10px'>"
        "<a href='/User_Engagement' target='_self' style='color:#f1f1f1; text-decoration:none'>Polarity Analysis</a>"
        "</div>",
        unsafe_allow_html=True
    )

st.markdown(
    "<div style='text-align:center; margin-top:80px;'>"
    "<h3>Designed By : Gehan Pasindhu(20235926)</h3>"
    "</div>", unsafe_allow_html=True
)

st.markdown(
 "<div style='text-align:right; margin-top:20px;'>"
    "<p style='font-style:italic'>Note *<br>Social Media Analytics Dashboard for Rukshan Yoga Studios Application is designed only for educational purpose.<br> And any of the data used here will not be used for any other purposes.</p>"
    "</div>", unsafe_allow_html=True
)

hide_stremlit_style = """
<style>
#MainMenu{visibility:hidden}
footer{visibility:hidden}
</style>

"""
st.markdown(hide_stremlit_style, unsafe_allow_html=True)
