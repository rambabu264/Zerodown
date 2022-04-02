import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go


st.set_page_config(layout="wide")
st.title("US Housing Market Dashboard")

@st.cache
def load_data():
    data = pd.read_csv('data_week_1.tsv',sep='\t')
    return data

df = load_data()


    # def line_chart(df,column_attr="total_homes_sold"):
    #     """
    #         function to plot line based on started
    #     """
    #     return fig

#st.write(df)

st.header("US MAP")
k = df[['state','total_new_listings']].groupby(['state'],as_index=False).sum()
k = k[:-1]
fig = px.choropleth(k,
                    locations='state', 
                    locationmode="USA-states", 
                    scope="usa",
                    
                    color='state',
                    color_continuous_scale="Viridis_r", 
                    )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, )
fig.update_layout(geo=dict(bgcolor= 'rgba(0,0,0,0)'))
st.plotly_chart(fig, use_container_width=True)


st.header("Pie Chart")
tmp = df[['region_type_id', 'total_homes_sold']]
fig = px.pie(tmp,names = 'region_type_id',color = 'region_type_id',color_discrete_sequence=px.colors.sequential.RdBu, title = 'Number of Counties and Metros')
fig.update_traces(textposition='inside', textinfo='percent+label')
st.plotly_chart( fig)
fig = px.pie(tmp, values = 'total_homes_sold', names = 'region_type_id',color = 'region_type_id' , color_discrete_sequence=px.colors.sequential.RdBu, title = 'Total no of Households sold in Counties and Metros')
fig.update_traces(textposition='inside', textinfo='percent+label')
st.plotly_chart(fig)
with st.expander('Inference'):
    st.write("""The chart above shows some numbers I picked for you.
        I rolled actual dice for these, so they're *guaranteed* to
        be random.""")

col1, col2 = st.columns(2)

with col1:

    st.header("Line Chart")
    states = df['state'].unique()

    option_state = st.selectbox(
        'What is your state?',
        states)
    
    data = df[df['state']==option_state]

    option_region = st.selectbox(
        'What is your region type you want to visualize?',
        ('County','Metro'))
    
    if option_region == "County":
        val = 0
    else:
        val = 1
    
    data = df[df['region_type_id']==val]
    
    option_city = st.selectbox(
        'What is your region city you want to visualize?',
        data['region_name'].unique())
    

    data = df[df['region_name']==option_city]
    column = list(data.columns)
    column = column[1:]
    column.remove('region_id')
    column.remove('region_type_id')
    column.remove('region_name')
    column.remove('period_begin')
    column.remove('period_end')
    column.remove('duration')
    column.remove('state')



    option_column = st.selectbox(
        'What is your column attribute you want to visualize?',
        column)

    data_2 = data[option_column].rolling(12).mean()
    data_2.fillna(0)
    
    

with col2:
    fig = go.Figure()
    fig.add_scatter(x=data['period_begin'],y=data[option_column],mode="lines",name='1 week avg')

                        
    fig.add_scatter(x=data['period_begin'],y=data_2,mode="lines",name='12 week avg')
    # fig.update_layout(
    #     showlegend=False
    # ) 
    fig.update_layout(title="Plot for the city "+option_city+" from 2018 to 2019",
                   xaxis_title='Staring Date 2018 - 2022',
                   yaxis_title=option_column
    )

    st.plotly_chart(fig, use_container_width= True)
         

