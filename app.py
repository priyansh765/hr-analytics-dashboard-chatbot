import streamlit as st
import pandas as pd

st.set_page_config(page_title="HR Analytics Dashboard", layout="wide")

st.title("HR Analytics Dashboard")

# Load data
df = pd.read_csv('data/processed/hr_cleaned.csv')

# Sidebar navigation
page = st.sidebar.radio("Navigate", ["Overview", "Attrition Analysis", "Department Insights", "Prediction", "Chatbot"])

if page == "Overview":
    st.header("Overview")
    st.write("Coming soon...")

elif page == "Attrition Analysis":
    st.header("Attrition Analysis")
    st.write("Coming soon...")

elif page == "Department Insights":
    st.header("Department Insights")
    st.write("Coming soon...")

elif page == "Prediction":
    st.header("Attrition Prediction")
    st.write("Coming soon...")

elif page == "Chatbot":
    st.header("HR Chatbot")
    st.write("Coming soon...")