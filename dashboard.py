import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine
from PIL import Image
import datetime

# engine = create_engine("mysql+mysqlconnector://root:1234@localhost/superstore") 
# #Should hash out the password and don't upload on Github

# df = pd.read_sql_table('superstore', con=engine)
# #print(df.head())

df = pd.read_csv('SampleSuperstore.csv')

st.set_page_config(layout='wide')
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)
image = Image.open('logo.jpg')

col1, col2 = st.columns([0.1,0.9])
with col1:
    st.image(image,width=450)
with col2:
    st.markdown("<h1 style='text-align: center;'>We Gat U Interactive Sales Dashboard</h1>", unsafe_allow_html=True)

col3, col4, col5 = st.columns([0.10, 0.45, 0.45])
with col3:
    update_date = str(datetime.datetime.now().strftime('%d %B %Y'))
    st.write(f'Last updated:  \n{update_date}')

with col4:
    fig = px.bar(
        df.groupby('Segment', as_index=False)['Profit'].sum(),
        x='Segment', y='Profit', template='plotly_white', hover_data='Profit', height=500,
        title='Total Profit by Segment'
    )
    st.plotly_chart(fig, use_container_width=True)

__, view1, dwn1, view2, dwn2 = st.columns([0.15,0.20,0.20,0.20,0.20])
with view1:
    expander = st.expander('Segment Profit')
    data = df[['Segment', 'Profit']].groupby(by='Segment')['Profit'].sum()
    expander.write(data)

with dwn1:
    st.download_button('Get Data', data.to_csv().encode('utf-8'),
                       file_name='SegmentData.csv', mime='text/csv')
    
with col5:
    region_sales = df[['Region','Profit']].groupby('Region')['Profit'].sum().reset_index()
    fig = px.pie(region_sales,values='Profit', names='Region', title='Profit by Region', hover_data='Profit', template='plotly_white', width=100)
    
    st.plotly_chart(fig, use_container_width=True)

with view2:
    expander = st.expander('Region Profit')
    data = df[['Region', 'Profit']].groupby(by='Region')['Profit'].sum()
    expander.write(data)

with dwn2:
    st.download_button('Get Data', data.to_csv().encode('utf-8'),
                       file_name='RegionData.csv', mime='text/csv')

st.divider()

_, col6, col7 = st.columns([0.10,0.45,0.45])
with col6:
    fig = px.bar(df,x='Region',y='Sales',color='Category',barmode='group',
                color_discrete_sequence=px.colors.qualitative.Plotly,# use Plotly's default palette   
                title='Total Sales by Category in each Region')
    
    st.plotly_chart(fig,use_container_width=True)



with col7:
    fig = px.bar(df, x='Ship Mode', y='Discount', title='Total Discount by Ship Mode')


    st.plotly_chart(fig, use_container_width=True)


st.divider()

_, col8 = st.columns([0.1,1])
with col8:
    sales_units = df.groupby('State')[['Sales', 'Quantity']].sum().reset_index()
    fig = go.Figure()
    fig.add_trace(go.Bar(x=sales_units['State'], y=sales_units['Sales'], name='Total Sales'))
    fig.add_trace(go.Scatter(x=sales_units['State'], y=sales_units['Quantity'], mode='lines', yaxis='y2', name='Total Units Sold'))

    fig.update_layout(
    title = 'Total Units and Total Sales by State',
    xaxis = dict(title='State'),
    yaxis = dict(title='Total Sales', showgrid=False),
    yaxis2 = dict(title='Total Units Sold', overlaying='y', side='right'),
    legend = dict(x=1,y=1),
    template = 'plotly_white')

    st.plotly_chart(fig,use_container_width=True)

st.divider()



col9, col10, col11 = st.columns([0.1,0.45,0.45])
with col9:
    st.markdown("<h5 style='text-align: center;'> State Sales per Category </h2>",unsafe_allow_html=True)
    #Dropdown to select a state
    state = st.selectbox("Select a State", sorted(df["State"].unique()))

with col10:
    # Filter dataset by selected state
    dff = df[df["State"] == state]

    # Aggregate profit by Category + Sub-Category
    agg = dff.groupby(["Category"], as_index=False)["Profit"].sum()

    # Build funnel chart
    fig = px.funnel(agg,x="Profit",y="Category",title=f"Profit Funnel for {state}",)

    # Show chart
    st.plotly_chart(fig, use_container_width=True)

with col11:
     #Aggregate profit by Segment
    sagg = dff.groupby(["Segment"], as_index=False)["Profit"].sum()

    # Build funnel chart
    fig = px.bar(sagg,x="Profit",y="Segment",title=f"Profit bar for {state}",)

    # Show chart
    st.plotly_chart(fig, use_container_width=True)






st.divider()

_, col12 = st.columns([0.1,1])
with col12:
    # Option 1: Use only positive profits
    df_positive = df[df['Profit'] > 0]

    fig = px.icicle(
    df_positive,
    path=[px.Constant("Profit"), 'Category', 'Sub-Category'],
    values='Profit',
    color='Profit',
    height = 700,
    width = 600,
    color_continuous_scale='viridis')

    fig.update_traces(root_color="lightblue")
    fig.update_layout(
        title = 'Profit Analysis by Category and Sub-Category',
        margin=dict(t=50, l=25, r=25, b=25))

    st.plotly_chart(fig, use_container_width=True)