import streamlit as st
import pandas as pd
from app_model.db import get_connection
from app_model.metadatas import get_all_datasets_metadata

st.set_page_config(
    page_title="Data Governance",
    page_icon="📊",
    layout="wide"
)

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.warning("Please log in to access the data governance dashboard.")

    if st.button("Go to Login Page"):
        st.session_state['logged_in'] = False
        st.switch_page("Home.py")
    st.stop()

else:
    st.success("You're logged in!")

conn = get_connection()
data = get_all_datasets_metadata(conn)

st.title("Data Governance Dashboard 📊")

with st.sidebar:
    st.header("Navigation")
    uploader_ = st.selectbox("Uploaded By", data['uploaded_by'].unique())

filtered_data = data[data['uploaded_by'] == uploader_]
filtered_data['upload_date'] = pd.to_datetime(filtered_data['upload_date'], errors='coerce')

col1, col2 = st.columns(2)

with col1:
    st.subheader("Largest Datasets (By Row Count)")
    st.bar_chart(filtered_data.sort_values("rows", ascending=False).set_index("name")["rows"])

with col2:
    st.subheader("Column Count Per Dataset")
    st.bar_chart(filtered_data.set_index("name")["columns"])

st.subheader("Old & Large Datasets (Archive Risk)")

old_data = filtered_data[
    (filtered_data['rows'] > 100000) &
    ((pd.Timestamp.now() - filtered_data['upload_date']).dt.days > 90)
]

st.dataframe(old_data, use_container_width=True)

if not old_data.empty:
    st.info("These datasets are large and haven’t been used in a long time. They should be reviewed or archived.")

st.subheader("All Department Datasets")
st.dataframe(filtered_data, use_container_width=True)
