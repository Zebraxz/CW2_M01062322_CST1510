import streamlit as st
import pandas as pd
from app_model.db import get_connection
from app_model.cyber_incidents import get_all_cyber_incidents

st.set_page_config(
    page_title="Home",
    page_icon=" 👨‍💻",
    layout="wide"
)

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.warning("Please log in to access the cyber incident dashboard.")
    
    if st.button("Go to Login Page"):
        st.session_state['logged_in'] = False
        st.switch_page("Home.py")
    st.stop()

else:
    st.success("You're logged in!")



conn = get_connection
data = get_all_cyber_incidents()
data['timestamp'] = pd.to_datetime(data['timestamp'], errors='coerce')
st.title("Welcome To The Cyber Incidents Dashboard 👨‍💻")



with st.sidebar:
    st.header("Navigation")
    severity_ = st.selectbox('Severity Level', data['severity'].unique())



data['timestamp'] = pd.to_datetime(data['timestamp'])
filtered_data = data[data['severity'] == severity_]

col1, col2 = st.columns(2)

with col1:
    st.subheader(f"Cyber Incident with Severity: {severity_}")
    st.bar_chart(filtered_data['category'].value_counts())


with col2:
    st.subheader("Phishing Trend Over Time")

    phishing_only = filtered_data[filtered_data['category'] == 'Phishing']
    phishing_only = phishing_only.sort_values("timestamp")

    phishing_trend = phishing_only.groupby(
        phishing_only["timestamp"].dt.to_period("D")
    ).size()

    phishing_trend.index = phishing_trend.index.to_timestamp()
    st.line_chart(phishing_trend)


st.subheader("Incident Status Bottleneck")

bottleneck = filtered_data['status'].value_counts()
st.bar_chart(bottleneck)

worst_status = bottleneck.idxmax()
st.info(f"The biggest resolution bottleneck is currently: {worst_status}")

st.subheader("Full Incident Table")
st.dataframe(filtered_data, use_container_width=True)


