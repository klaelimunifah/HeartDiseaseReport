import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set_style("whitegrid")
import plotly.express as px
import plotly.graph_objects as go

def total_respondents(df):
    total = len(df)
    return total

def heart_patients(df):
    heart_patiens = df.loc[df['HadHeartAttack'] == "Yes"].reset_index()
    return heart_patiens

def total_patients(df):
    total = len(df)
    return total

def patients_percentage(df):
    had_heart_attack= df.groupby(['HadHeartAttack']).agg({'heartattack' :'count'}).reset_index()
    had_heart_attack= had_heart_attack.rename(columns = { 'heartattack': 'Total'})
    fig = px.pie(had_heart_attack, values='Total',
                 names='HadHeartAttack',
                 title='Heart Disease Patients in USA',
                 hole = 0.5,
                 color_discrete_sequence=px.colors.sequential.Aggrnyl)
    fig.update_layout(margin={"r":0,"t":25,"l":0,"b":0})
    return fig

def gender_distribution(df):
    gender_distribution = heart_patients(df)
    gender_distribution = gender_distribution.groupby(['Sex']).agg({'HadHeartAttack' : "count"})
    gender_distribution = gender_distribution.rename(columns ={'HadHeartAttack' : 'Total'})
    gender_distribution = gender_distribution.reset_index()

    total_female = gender_distribution.loc[gender_distribution['Sex'] == 'Female']
    total_female = total_female['Total']

    total_male = gender_distribution.loc[gender_distribution['Sex'] == 'Male']
    total_male = total_male['Total']
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=total_female,
        name='Female',
        orientation='h',
        marker=dict(
        color='rgba(139, 209, 110, 0.6)',
        line=dict(color='rgba(57, 171, 126, 1.0)', width=3))))

    fig.add_trace(go.Bar(
        x= total_male,
        name='Male',
        orientation='h',
        marker=dict(
        color='rgba(14, 129, 125, 0.6)',
        line=dict(color='rgba(36, 86, 104, 1.0)', width=3))))

    fig.update_layout(barmode='stack',
                      title='Gender Distribution of Heart Disease Patients',
                      xaxis = go.XAxis(showticklabels=False),
                      yaxis = go.YAxis(showticklabels= False),
                      height=300,
                      margin={"r":0,"t":25,"l":0,"b":0})

    return fig

def need_attention(df):
    by_generalhealth = heart_patients(df)
    by_generalhealth['generalhealthrate'] = by_generalhealth.GeneralHealth.replace({"Poor": 1,  "Fair" : 2, "Good" : 3, "Very good": 4, "Excellent":5})
    by_generalhealth = by_generalhealth.groupby(['generalhealthrate','GeneralHealth']).agg({'HadHeartAttack' : "count"})
    by_generalhealth = by_generalhealth.reset_index()
    by_generalhealth = by_generalhealth.rename(columns = { 'HadHeartAttack': 'Total'}).set_index('generalhealthrate')

    fig = go.Figure(go.Bar(
            x= by_generalhealth.Total,
            y= by_generalhealth.GeneralHealth,
            orientation='h', marker={'color': by_generalhealth.index ,
                                               'colorscale': 'Aggrnyl'}))
    fig.update_layout(title='Patients General Health',
                      margin={"r":0,"t":25,"l":0,"b":0})
    return fig

def state_distribution(df):
    state_distribution = heart_patients(df)
    state_distribution = state_distribution.groupby(['State']).agg({'HadHeartAttack' : 'count', 'usa_state_code' : 'first'}).reset_index()
    state_distribution= state_distribution.rename(columns = { 'HadHeartAttack': 'Total'})

    fig = px.choropleth(state_distribution, locations='usa_state_code', color="Total",
                           range_color=(0, 1200),
                           color_continuous_scale="Aggrnyl",
                           locationmode = 'USA-states',
                           scope="usa",
                           title='USA Heart Disease Patients Distribution'
                          )
    fig.update_layout(margin={"r":0,"t":25,"l":0,"b":0})
    return fig

def physical_activities_corr(df):
    physical_activities = df.groupby(['HadHeartAttack', 'PhysicalActivities']).agg({'PhysicalActivities' : "count"}).rename(columns = { 'PhysicalActivities': 'Total'})
    physical_activities = physical_activities.reset_index()
    fig = px.histogram(physical_activities, x="HadHeartAttack", y="Total",
             color='PhysicalActivities', barmode='group',
             height=400, color_discrete_sequence=px.colors.sequential.Aggrnyl )
    fig.update_layout(title='Physical Activities of Respondents', margin={"r":0,"t":25,"l":0,"b":0})
    return fig

def sleep_hours_distribution(df):
    fig = px.violin(df, y="SleepHours", color="HadHeartAttack",
                violinmode='overlay',
                hover_data=df.columns, color_discrete_sequence=['#EDEF5D', '#0E817D'])
    fig.update_layout( title='Sleep Hours Distribution of Respondents', margin={"r":0,"t":25,"l":0,"b":0})

    return fig

#Import data
all_data = pd.read_csv('all_data.csv')

#MAIN
st.title("CDC's 2022 Heart Disease Patient Dashboard")

with st.container( ):
    col1, col2 = st.columns([2,3])
    with col1:
        with st.container():
            col3,col4 = st.columns([1,1])
            with col3:
                st.metric(label= "Total Respondents", value = total_respondents(all_data))
            with col4:
                st.metric(label= "Total Patients", value = total_patients(heart_patients(all_data)))
        with st.container():
            fig3 = need_attention(all_data)
            st.plotly_chart(fig3, use_container_width=True)

    with col2:
        with st.container( ):
            fig1= patients_percentage(all_data)
            st.plotly_chart(fig1, use_container_width=True)
        with st.container():
            fig2 = gender_distribution(all_data)
            st.plotly_chart(fig2, use_container_width=True)



with st.container():
    fig4 = state_distribution(all_data)
    st.plotly_chart(fig4, use_container_width=True)

with st.container():
    col1, col2 = st.columns([1,1])
    with col1:
        fig5 = physical_activities_corr(all_data)
        st.plotly_chart(fig5, use_container_width=True)
    with col2:
        fig6 = sleep_hours_distribution(all_data)
        st.plotly_chart(fig6, use_container_width=True)

