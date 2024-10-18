import streamlit as st
from streamlit_date_picker import date_range_picker, PickerType
import plotly.express as px
import pandas as pd
import pandas
import psycopg2
from psycopg2 import DatabaseError
from Query_file import *

error_message = "An error occurred. Kindly connect to the internet and refresh this page"
error_100 = "An error 100 occurred. Kindly connect to the internet and refresh this page"

try:
    dets_query_object = Connect_query()
except (psycopg2.Error, pandas.errors.DatabaseError, DatabaseError, psycopg2.DatabaseError):
    st.error(error_message)
    print("An error occured in Liberty Life project while creating dets_query_object obj")



st.set_page_config(page_title="Liberty Life", page_icon="stethoscope", layout="wide",initial_sidebar_state = "expanded")



####::::::::::::::::::::::::: MAIN APP :::::::::::::::::::::::::::######

st.title(" LibertyLife Dashboard")
####This help to create the dropdown for date selection

date_range_string = date_range_picker(picker_type=PickerType.date,
                                      key='range_picker')


###### GROUPING THE SUBBSCRIBERS BY SUBSCRIPTION TYPE ::::::::::::::::::::::::::#################
all_subscribers = dets_query_object.subcription_plan()
# individual_sub = all_subscribers.query("plan_type == 'INDIVIDUAL'")
# corporate_sub = all_subscribers.query("plan_type == 'CORPORATE'")
# family_sub = all_subscribers.query("plan_type == 'FAMILY'")
# print(all_subscribers)
###################::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

####::::::::::::::::::::::::::::::: GROUPING SUBSCRIBERS BY CHANNEL :::::::::::::::::::::::::::::::::::::::::::#########################################################
all_channels = all_subscribers
ussd_subs  = all_subscribers.query("channel == 'USSD'")
web_subs = all_subscribers.query("channel == 'WEB'")
agent_subs = all_subscribers.query("channel == 'AGENT'")
seeds_subs = all_subscribers.query("channel == 'SEEDS_BORROWER_CHANNEL'")
sales_agent_subs = all_subscribers.query("channel == 'SALES_AGENT'")
print(ussd_subs)
#############::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
####This if statement helps to check if any date range was selected 
# in the dropdown above and filters the data according, if not it shows all time data
if date_range_string is not None:
     start_datetime = pd.Timestamp(date_range_string[0])
     end_datetime = pd.Timestamp(date_range_string[1])
     end_datetime = end_datetime.replace(hour=23, minute=59, second=59, microsecond=0)

########:::::::::::::::: Converting The Date Column To Datetime  ::::::::::::::::::::::::::::::::::::::::::::::::::########################### 
#      all_subscribers['date'] = pd.to_datetime(all_subscribers['date'])
#      individual_sub['date'] = pd.to_datetime(individual_sub['date'])
#      corporate_sub['date']  = pd.to_datetime(corporate_sub['date'])
#      family_sub['date'] = pd.to_datetime(family_sub['date'])
# #############:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::########################
     all_channels['date'] = pd.to_datetime(all_channels['date'])
     ussd_subs['date'] = pd.to_datetime(ussd_subs['date'])
     web_subs['date'] = pd.to_datetime(web_subs['date'])
     agent_subs['date'] = pd.to_datetime(agent_subs['date'])
     seeds_subs['date'] = pd.to_datetime(seeds_subs['date'])
     sales_agent_subs['date'] = pd.to_datetime(sales_agent_subs['date'])
#######################::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::#########################################################

################## Filter DATE RANGE FOR SELECTION #############
     all_subscribers_filtered = all_subscribers[(all_subscribers['date'] >= start_datetime) 
                                         & (all_subscribers['date'] <= end_datetime)]

    #  individual_filtered = [(individual_sub['date'] >= start_datetime) 
    #                                      & (individual_sub['date'] <= end_datetime)]
    #  corporate_filtered = [(corporate_sub['date'] >= start_datetime) 
    #                                      & (corporate_sub['date'] <= end_datetime)]
    #  family_filtered = [(family_sub['date'] >= start_datetime) 
    #                                      & (family_sub['date'] <= end_datetime)]
############################:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::######################
     all_channels_filtered = all_channels[(all_channels['date'] >= start_datetime) 
                                        & (all_channels['date'] <= end_datetime)]
     ussd_subs_filtered = ussd_subs[(ussd_subs['date'] >= start_datetime) 
                                        & (ussd_subs['date'] <= end_datetime)]
     web_subs_filtered = web_subs[(web_subs['date'] >= start_datetime) 
                                        & (web_subs['date'] <= end_datetime)]
     agent_subs_filtered = agent_subs[(agent_subs['date'] >= start_datetime) 
                                        & (agent_subs['date'] <= end_datetime)]
     seeds_subs_filtered = seeds_subs[(seeds_subs['date'] >= start_datetime) 
                                        & (seeds_subs['date'] <= end_datetime)]
     sales_agent_subs_filtered = sales_agent_subs[(sales_agent_subs['date'] >= start_datetime) 
                                        & (sales_agent_subs['date'] <= end_datetime)]

#### This if statement filters using the All time button,
#  if all time, only the dta within the if block will be affected,
#  if not then it wnt affect others that why the variables are outside the if block.

     if st.sidebar.button('All Time'):
       all_subscribers_data = all_subscribers
       all_channels_data = all_channels
     else:
       all_channels_data = all_channels_filtered
     ussd_subs_data = ussd_subs_filtered
     web_subs_data = web_subs_filtered
     agent_subs_data = agent_subs_filtered
     seeds_subs_data = seeds_subs_filtered
     sales_agent_subs_data  = sales_agent_subs_filtered

##########::::::::::::::::::::::::::::::::: GRAPHICAL REPRESENTATION USING THE CHANNELS:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::###########################
web_col1, web_col2 = st.columns(2)
with  web_col1:
  web_daily_fig1 = px.line(
                    web_subs_data,
                    x="date",
                    y="channel_daily_count",
                    # symbol= 'date',
                    title="<b>WEB COUNT</b>",
                    # color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
                    template="plotly_white",
                    height=300,
                    line_shape='linear'  # Ensures that the points connect as a proper line chart
                    )
  web_daily_fig1.update_layout(
                    xaxis=dict(tickmode="linear", showgrid=False),
                    yaxis=(dict(showgrid=False)),
                    plot_bgcolor="rgba(0,0,0,0)",
                    showlegend=False,  # Hide the legend
                    # traceorder="normal",  # Set the order in which the legend items appear
                    font=dict(
                        family="sans-serif",
                        size=12,
                        color="white"
                    ),
                    # bgcolor="rgba(0,0,0,0)",  # Set the background color of the legend to transparent
                    )
  st.plotly_chart(web_daily_fig1, use_container_width=True)

  with  web_col2:
    web_daily_fig2 = px.line(
                    web_subs_data,
                    x="date",
                    y="channel_daily_sum",
                    # symbol= 'date',
                    title="<b>WEB REVENUE</b>",
                    # color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
                    template="plotly_white",
                    height=300,
                    line_shape='linear'  # Ensures that the points connect as a proper line chart
                    )
    web_daily_fig2.update_layout(
                    xaxis=dict(tickmode="linear", showgrid=False),
                    yaxis=(dict(showgrid=False)),
                    plot_bgcolor="rgba(0,0,0,0)",
                    showlegend=False,  # Hide the legend
                    # traceorder="normal",  # Set the order in which the legend items appear
                    font=dict(
                        family="sans-serif",
                        size=12,
                        color="white"
                    ),
                    # bgcolor="rgba(0,0,0,0)",  # Set the background color of the legend to transparent
                    )
    st.plotly_chart(web_daily_fig2, use_container_width=True)


ussd_col1,ussd_col2 = st.columns(2)

with  ussd_col1:
  ussd_daily_fig1 = px.line(
                    ussd_subs_data,
                    x="date",
                    y="channel_daily_count",
                    # symbol= 'date',
                    title="<b>USSD COUNT</b>",
                    # color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
                    template="plotly_white",
                    height=300,
                    line_shape='linear'  # Ensures that the points connect as a proper line chart
                    )
  ussd_daily_fig1.update_layout(
                    xaxis=dict(tickmode="linear", showgrid=False),
                    yaxis=(dict(showgrid=False)),
                    plot_bgcolor="rgba(0,0,0,0)",
                    showlegend=False,  # Hide the legend
                    # traceorder="normal",  # Set the order in which the legend items appear
                    font=dict(
                        family="sans-serif",
                        size=12,
                        color="white"
                    ),
                    # bgcolor="rgba(0,0,0,0)",  # Set the background color of the legend to transparent
                    )
  st.plotly_chart(ussd_daily_fig1, use_container_width=True)
 
  with  ussd_col2:
    ussd_daily_fig2 = px.line(
                    ussd_subs_data,
                    x="date",
                    y="channel_daily_sum",
                    # symbol= 'date',
                    title="<b>USSD REVENUE</b>",
                    # color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
                    template="plotly_white",
                    height=300,
                    line_shape='linear'  # Ensures that the points connect as a proper line chart
                    )
    ussd_daily_fig2.update_layout(
                    xaxis=dict(tickmode="linear", showgrid=False),
                    yaxis=(dict(showgrid=False)),
                    plot_bgcolor="rgba(0,0,0,0)",
                    showlegend=False,  # Hide the legend
                    # traceorder="normal",  # Set the order in which the legend items appear
                    font=dict(
                        family="sans-serif",
                        size=12,
                        color="white"
                    ),
                    # bgcolor="rgba(0,0,0,0)",  # Set the background color of the legend to transparent
                    )
    st.plotly_chart(ussd_daily_fig2, use_container_width=True)


seeds_col1,seeds_col2 = st.columns(2)
with seeds_col1:
  seeds_fig1 = px.line(
                    seeds_subs_data,
                    x="date",
                    y="channel_daily_count",
                    # symbol= 'date',
                    title="<b>SEEDS COUNT</b>",
                    # color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
                    template="plotly_white",
                    height=300,
                    line_shape='linear'  # Ensures that the points connect as a proper line chart
                    )
  seeds_fig1.update_layout(
                    xaxis=dict(tickmode="linear", showgrid=False),
                    yaxis=(dict(showgrid=False)),
                    plot_bgcolor="rgba(0,0,0,0)",
                    showlegend=False,  # Hide the legend
                    # traceorder="normal",  # Set the order in which the legend items appear
                    font=dict(
                        family="sans-serif",
                        size=12,
                        color="white"
                    ),
                    # bgcolor="rgba(0,0,0,0)",  # Set the background color of the legend to transparent
                    )
  st.plotly_chart(seeds_fig1, use_container_width=True)

with seeds_col2:
  seeds_fig2 = px.line(
                    seeds_subs_data,
                    x="date",
                    y="channel_daily_sum",
                    # symbol= 'date',
                    title="<b>SEEDS REVENUE</b>",
                    # color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
                    template="plotly_white",
                    height=300,
                    line_shape='linear'  # Ensures that the points connect as a proper line chart
                    )
  seeds_fig2.update_layout(
                    xaxis=dict(tickmode="linear", showgrid=False),
                    yaxis=(dict(showgrid=False)),
                    plot_bgcolor="rgba(0,0,0,0)",
                    showlegend=False,  # Hide the legend
                    # traceorder="normal",  # Set the order in which the legend items appear
                    font=dict(
                        family="sans-serif",
                        size=12,
                        color="white"
                    ),
                    # bgcolor="rgba(0,0,0,0)",  # Set the background color of the legend to transparent
                    )
  st.plotly_chart(seeds_fig2, use_container_width=True)



agent_col1,agent_col2 = st.columns(2)
with agent_col1:
  agent_fig1 = px.line(
                    agent_subs_data,
                    x="date",
                    y="channel_daily_count",
#                     # symbol= 'date',
                    title="<b>AGENT COUNT</b>",
#                     # color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
                    template="plotly_white",
                    height=300,
                    line_shape='linear'  # Ensures that the points connect as a proper line chart
                    )
  agent_fig1.update_layout(
                    xaxis=dict(tickmode="linear", showgrid=False),
                    yaxis=(dict(showgrid=False)),
                    plot_bgcolor="rgba(0,0,0,0)",
                    showlegend=False,  # Hide the legend
#                     # traceorder="normal",  # Set the order in which the legend items appear
                    font=dict(
                        family="sans-serif",
                        size=12,
                        color="white"
                    ),
#                     # bgcolor="rgba(0,0,0,0)",  # Set the background color of the legend to transparent
                    )
  st.plotly_chart(agent_fig1, use_container_width=True)


with agent_col2:
  agent_fig2 = px.line(
                    agent_subs_data,
                    x="date",
                    y="channel_daily_sum",
#                     # symbol= 'date',
                    title="<b>AGENT REVENUE</b>",
#                     # color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
                    template="plotly_white",
                    height=300,
                    line_shape='linear'  # Ensures that the points connect as a proper line chart
                    )
  agent_fig2.update_layout(
                    xaxis=dict(tickmode="linear", showgrid=False),
                    yaxis=(dict(showgrid=False)),
                    plot_bgcolor="rgba(0,0,0,0)",
                    showlegend=False,  # Hide the legend
#                     # traceorder="normal",  # Set the order in which the legend items appear
                    font=dict(
                        family="sans-serif",
                        size=12,
                        color="white"
                    ),
#                     # bgcolor="rgba(0,0,0,0)",  # Set the background color of the legend to transparent
                    )
  st.plotly_chart(agent_fig2, use_container_width=True)



sales_agent_col1,sales_agent_col2 = st.columns(2)
with  sales_agent_col1:
  sales_fig1 = px.line(
                    sales_agent_subs,
                    x="date",
                    y="channel_daily_count",
                    # symbol= 'date',
                    title="<b>SALES_AGENT COUNT</b>",
                    # color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
                    template="plotly_white",
                    height=300,
                    line_shape='linear'  # Ensures that the points connect as a proper line chart
                    )
  sales_fig1.update_layout(
                    xaxis=dict(tickmode="linear", showgrid=False),
                    yaxis=(dict(showgrid=False)),
                    plot_bgcolor="rgba(0,0,0,0)",
                    showlegend=False,  # Hide the legend
                    # traceorder="normal",  # Set the order in which the legend items appear
                    font=dict(
                        family="sans-serif",
                        size=12,
                        color="white"
                    ),
                    # bgcolor="rgba(0,0,0,0)",  # Set the background color of the legend to transparent
                    )
  st.plotly_chart(sales_fig1, use_container_width=True)
  

with  sales_agent_col2:
    sales_fig2 = px.line(
                    sales_agent_subs,
                    x="date",
                    y="channel_daily_sum",
                    # symbol= 'date',
                    title="<b>SALES_AGENT REVENUE</b>",
                    # color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
                    template="plotly_white",
                    height=300,
                    line_shape='linear'  # Ensures that the points connect as a proper line chart
                    )
    sales_fig2.update_layout(
                    xaxis=dict(tickmode="linear", showgrid=False),
                    yaxis=(dict(showgrid=False)),
                    plot_bgcolor="rgba(0,0,0,0)",
                    showlegend=False,  # Hide the legend
                    # traceorder="normal",  # Set the order in which the legend items appear
                    font=dict(
                        family="sans-serif",
                        size=12,
                        color="white"
                    ),
                    # bgcolor="rgba(0,0,0,0)",  # Set the background color of the legend to transparent
                    )
    st.plotly_chart(sales_fig2, use_container_width=True)


# Create one column using st.columns
all_time_col1,all_time_col2 = st.columns(2)

with all_time_col1:
    all_fig1 = px.bar(
        all_channels_data,
        x='month_name',
        y='channel_monthly_count',
        color='channel',
        barmode='group',
        height=300,
        title="<b>ALL_TIME COUNT</b>",

    )
    st.plotly_chart(all_fig1, use_container_width=True)

with all_time_col2:
    all_fig2 = px.bar(
        all_channels_data,
        x='month_name',
        y='channel_monthly_sum',
        color='channel',
        barmode='group',
        height=300,
        title="<b>ALL_TIME REVENUE</b>",

    )
    st.plotly_chart(all_fig2, use_container_width=True)




