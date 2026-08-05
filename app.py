import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="HR Analytics Dashboard", layout="wide")

st.title("HR Analytics Dashboard")

# Load data
df = pd.read_csv('data/processed/hr_cleaned.csv')

# Sidebar navigation
page = st.sidebar.radio("Navigate", ["Overview", "Attrition Analysis", "Department Insights", "Prediction", "Chatbot"])

if page == "Overview":
    st.header("Overview")

    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)

    total_employees = df.shape[0]
    attrition_rate = round((df['AttritionFlag'].sum() / total_employees) * 100, 2)
    avg_income = round(df['MonthlyIncome'].mean(), 0)
    avg_age = round(df['Age'].mean(), 1)

    col1.metric("Total Employees", total_employees)
    col2.metric("Attrition Rate", f"{attrition_rate}%")
    col3.metric("Avg Monthly Income", f"₹{avg_income}")
    col4.metric("Avg Age", avg_age)

    st.markdown("---")

    # Attrition Pie Chart
    attrition_counts = df['Attrition'].value_counts().reset_index()
    attrition_counts.columns = ['Attrition', 'Count']

    fig = px.pie(attrition_counts, names='Attrition', values='Count',
                 title='Attrition Distribution', hole=0.4)
    st.plotly_chart(fig, use_container_width=True)

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