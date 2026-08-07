import streamlit as st
import pandas as pd
import plotly.express as px
import joblib
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.chatbot.rule_based_bot import HRChatbot

st.set_page_config(page_title="HR Analytics Dashboard", layout="wide")

st.title("HR Analytics Dashboard")

# Load data
df = pd.read_csv('data/processed/hr_cleaned.csv')
# Load trained model
model = joblib.load('src/models/attrition_model.pkl')
label_encoders = joblib.load('src/models/label_encoders.pkl')
feature_columns = joblib.load('src/models/feature_columns.pkl')

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
    st.write("Enter employee details to predict attrition risk")

    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.slider("Age", 18, 60, 30)
        monthly_income = st.number_input("Monthly Income", 1000, 20000, 5000)
        overtime = st.selectbox("OverTime", ["Yes", "No"])
        job_satisfaction = st.slider("Job Satisfaction (1-4)", 1, 4, 3)

    with col2:
        department = st.selectbox("Department", df['Department'].unique())
        job_role = st.selectbox("Job Role", df['JobRole'].unique())
        years_at_company = st.slider("Years at Company", 0, 40, 5)
        work_life_balance = st.slider("Work Life Balance (1-4)", 1, 4, 3)

    with col3:
        distance_from_home = st.slider("Distance From Home", 1, 30, 5)
        total_working_years = st.slider("Total Working Years", 0, 40, 8)
        gender = st.selectbox("Gender", df['Gender'].unique())
        marital_status = st.selectbox("Marital Status", df['MaritalStatus'].unique())

    if st.button("Predict Attrition Risk"):
        # Build input row using dataset defaults, then override with user inputs
        input_data = df.drop(columns=['Attrition', 'AttritionFlag', 'AgeGroup', 'SalaryBand', 'TenureGroup'], errors='ignore').iloc[0:1].copy()

        input_data['Age'] = age
        input_data['MonthlyIncome'] = monthly_income
        input_data['OverTime'] = overtime
        input_data['JobSatisfaction'] = job_satisfaction
        input_data['Department'] = department
        input_data['JobRole'] = job_role
        input_data['YearsAtCompany'] = years_at_company
        input_data['WorkLifeBalance'] = work_life_balance
        input_data['DistanceFromHome'] = distance_from_home
        input_data['TotalWorkingYears'] = total_working_years
        input_data['Gender'] = gender
        input_data['MaritalStatus'] = marital_status

        # Encode categorical columns
        for col, le in label_encoders.items():
            if col in input_data.columns:
                input_data[col] = le.transform(input_data[col].astype(str))

        input_data = input_data[feature_columns]

        prediction = model.predict(input_data)[0]
        probability = model.predict_proba(input_data)[0][1]

        st.markdown("---")
        if prediction == 1:
            st.error(f"⚠️ High Attrition Risk — Probability: {probability*100:.1f}%")
        else:
            st.success(f"✅ Low Attrition Risk — Probability: {probability*100:.1f}%")

elif page == "Chatbot":
    st.title("🤖 HR Analytics Chatbot")
    st.write("Company ke HR data ke baare me kuch bhi poocho!")

    # Chatbot instance ko session state me cache karo (baar baar reload na ho)
    if "chatbot" not in st.session_state:
        st.session_state.chatbot = HRChatbot()

    # Chat history session state me store karo
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Sample questions dikhado help ke liye
    with st.expander("💡 Example questions"):
        st.markdown("""
        - What is the attrition rate?
        - Average salary in Sales department?
        - How many employees in Research & Development?
        - What is the average age?
        - How much overtime is there?
        """)

    # Purani chat history dikhao
    for role, message in st.session_state.chat_history:
        with st.chat_message(role):
            st.write(message)

    # User input box (bottom me fixed rehta hai Streamlit me)
    user_input = st.chat_input("Apna sawal yahan likho...")

    if user_input:
        # User ka message history me add karo aur dikhao
        st.session_state.chat_history.append(("user", user_input))
        with st.chat_message("user"):
            st.write(user_input)

        # Bot ka response nikalo
        response = st.session_state.chatbot.get_response(user_input)

        # Bot ka message history me add karo aur dikhao
        st.session_state.chat_history.append(("assistant", response))
        with st.chat_message("assistant"):
            st.write(response)

    # Clear chat button
    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()