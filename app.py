import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="HR Analytics Dashboard", layout="wide")

st.title("HR Analytics Dashboard")

# Load data
df = pd.read_csv('data/processed/hr_cleaned.csv')

st.sidebar.markdown("---")
st.sidebar.subheader("Filters")

dept_filter = st.sidebar.multiselect("Department", options=df['Department'].unique(), default=df['Department'].unique())
gender_filter = st.sidebar.multiselect("Gender", options=df['Gender'].unique(), default=df['Gender'].unique())

df = df[(df['Department'].isin(dept_filter)) & (df['Gender'].isin(gender_filter))]
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

    col1, col2 = st.columns(2)

    with col1:
        fig1 = px.histogram(df, x='Department', color='Attrition', barmode='group',
                             title='Attrition by Department')
        st.plotly_chart(fig1, use_container_width=True)

        fig3 = px.histogram(df, x='Gender', color='Attrition', barmode='group',
                             title='Attrition by Gender')
        st.plotly_chart(fig3, use_container_width=True)

        fig5 = px.histogram(df, x='SalaryBand', color='Attrition', barmode='group',
                             title='Attrition by Salary Band')
        st.plotly_chart(fig5, use_container_width=True)

    with col2:
        fig2 = px.histogram(df, x='AgeGroup', color='Attrition', barmode='group',
                             title='Attrition by Age Group')
        st.plotly_chart(fig2, use_container_width=True)

        fig4 = px.histogram(df, x='OverTime', color='Attrition', barmode='group',
                             title='Attrition by OverTime')
        st.plotly_chart(fig4, use_container_width=True)

        fig6 = px.histogram(df, x='TenureGroup', color='Attrition', barmode='group',
                             title='Attrition by Tenure Group')
        st.plotly_chart(fig6, use_container_width=True)

elif page == "Department Insights":
    st.header("Department Insights")

    col1, col2 = st.columns(2)

    with col1:
        dept_counts = df['Department'].value_counts().reset_index()
        dept_counts.columns = ['Department', 'Count']
        fig1 = px.bar(dept_counts, x='Department', y='Count', title='Headcount by Department')
        st.plotly_chart(fig1, use_container_width=True)

        fig3 = px.box(df, x='Department', y='JobSatisfaction', color='Department',
                       title='Job Satisfaction by Department')
        st.plotly_chart(fig3, use_container_width=True)

    with col2:
        income_by_role = df.groupby('JobRole')['MonthlyIncome'].mean().reset_index().sort_values('MonthlyIncome')
        fig2 = px.bar(income_by_role, x='MonthlyIncome', y='JobRole', orientation='h',
                       title='Average Income by Job Role')
        st.plotly_chart(fig2, use_container_width=True)

        fig4 = px.box(df, x='Department', y='WorkLifeBalance', color='Department',
                       title='Work Life Balance by Department')
        st.plotly_chart(fig4, use_container_width=True)

elif page == "Prediction":
    st.header("Attrition Prediction")
    st.write("Coming soon...")

elif page == "Chatbot":
    st.header("HR Chatbot")
    st.write("Coming soon...")