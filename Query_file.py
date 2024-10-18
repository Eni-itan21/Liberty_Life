import psycopg2
import pandas as pd
import numpy as np
import streamlit as st
import warnings
import datetime
from datetime import timedelta, datetime, timezone
from dataclasses import dataclass
warnings.filterwarnings('ignore')
pd.set_option('display.max_columns', 100)


@dataclass
class Connect_query:
    error = 'Ooops! Connection(DB) Failed. Kindly Refresh page'

    @st.cache_resource(show_spinner=False) # To chache the connection (caching resource)
    def life_connection(self, script):
        conn = psycopg2.connect(host = st.secrets.Life.host,
                            database = st.secrets.Life.database,
                            user = st.secrets.Life.user,
                            password = st.secrets.Life.password,
                            port = st.secrets.Life.port
                            )
        cur = conn.cursor()
        received_script = script
        query = pd.read_sql_query(received_script, conn) 
        return query

    #### All Subscription details
    @st.cache_resource(show_spinner=False)
    def subcription_plan(self):
        """
            Get data for all the various subscription plans
        """
        query = '''WITH DailyChannelSum AS (
                   SELECT
                      DATE(created_at) AS date,
                      TO_CHAR(created_at::timestamp with time zone, 'IW') AS week_number,
                      TO_CHAR(created_at::timestamp with time zone, 'Month') AS month_name,
                      EXTRACT(YEAR FROM created_at) AS year,
                      channel,
                      SUM(amount) AS channel_daily_sum,
                      COUNT(*) AS channel_daily_count
                   FROM
                       life_insurance_healthplan
                   WHERE
                       status = 'SUCCESS'
                   GROUP BY
                       date,
                       week_number,
                       month_name,
                       year,
                       channel
               ),
                   DailyTotals AS (
                   SELECT
                       DATE(created_at) AS date,
                       TO_CHAR(created_at::timestamp with time zone, 'IW') AS week_number,
                       TO_CHAR(created_at::timestamp with time zone, 'Month') AS month_name,
                       SUM(amount) AS daily_total_sum,
                       EXTRACT(YEAR FROM created_at) AS year
                   FROM
                       life_insurance_healthplan
                   WHERE
                       status = 'SUCCESS'
                   GROUP BY
                       date,
                       week_number,
                       month_name,
                       year
                  ),
                   MonthlyChannelSum AS (
                   SELECT
                       TO_CHAR(created_at::timestamp with time zone, 'Month') AS month_name,
                       EXTRACT(YEAR FROM created_at) AS year,
                       channel,
                       SUM(amount) AS channel_monthly_sum,
                       COUNT(*) AS channel_monthly_count
                   FROM
                       life_insurance_healthplan
                   WHERE
                       status = 'SUCCESS'
                   GROUP BY
                       month_name,
                       year,
                       channel
                  )
                   SELECT
                       dcs.date,
                       dcs.week_number,
                       dcs.month_name,
                       dcs.year,
                       dcs.channel,
                       dcs.channel_daily_sum,
                       dcs.channel_daily_count,
                       dt.daily_total_sum,
                       mcs.channel_monthly_sum,
                       mcs.channel_monthly_count
                   FROM
                       DailyChannelSum AS dcs
                   JOIN
                       DailyTotals AS dt ON dcs.date = dt.date
                   JOIN
                       MonthlyChannelSum AS mcs ON dcs.month_name = mcs.month_name
                           AND dcs.year = mcs.year
                   AND dcs.channel = mcs.channel
                   ORDER BY
                       dcs.date,
                       dcs.year,
                       dcs.month_name,
                       dcs.week_number,
                       dcs.channel_daily_sum,
                       dcs.channel_daily_count,
                       dcs.channel;
         '''

        try:
            data = self.life_connection(query)
        except(Exception,psycopg2.OperationalError) as e:
            st.error(f'Unable to connect to DB for Individual_plan, got an {e} error')
            print("Exception:",e)
            return st.stop()
        if data.empty:
            return None
        else:
            return data
    
    #  WITH DailyChannelSum AS (
        #            SELECT
        # #                DATE(created_at) AS date,
        #                TO_CHAR(created_at::timestamp with time zone, 'IW') AS week_number,
        #                TO_CHAR(created_at::timestamp with time zone, 'Month') AS month_name,
        #                EXTRACT(YEAR FROM created_at) AS year,
        #                channel,
        #                SUM(amount) AS channel_daily_sum,
        #                COUNT(*) AS channel_daily_count
        #            FROM
        #                life_insurance_healthplan
        #            WHERE
        #                status = 'SUCCESS'
        #            GROUP BY
        #                date,
        #                week_number,
        #                month_name,
        #                year,
        #                channel
        #             ),
        #             DailyTotals AS (
        #                 SELECT
        #                     DATE(created_at) AS date,
        #                     TO_CHAR(created_at::timestamp with time zone, 'IW') AS week_number,
        #                     TO_CHAR(created_at::timestamp with time zone, 'Month') AS month_name,
        #                     EXTRACT(YEAR FROM created_at) AS year,
        #                     SUM(amount) AS daily_total_sum
        #                 FROM
        #                     life_insurance_healthplan
        #             WHERE
        #                 status = 'SUCCESS'
        #             GROUP BY
        #                 date,
        #                 week_number,
        #                 month_name,
        #                 year
        #         )
        #             SELECT
        #                 dcs.date,
        #                 dcs.week_number,
        #                 dcs.month_name,
        #                 dcs.year,
        #                 dcs.channel,
        #                 dcs.channel_daily_sum,
        #                 dcs.channel_daily_count,
        #                 dt.daily_total_sum
        #             FROM
        #                 DailyChannelSum AS dcs
        #             JOIN
        #                 DailyTotals AS dt ON dcs.date = dt.date
        #             ORDER BY
        #                 dcs.date,
        #                 dcs.year,
        #                 dcs.month_name,
        #                 dcs.week_number,
        #                 dcs.channel_daily_sum,
        #                 dcs.channel_daily_count,
        #                 dcs.channel;

    # @st.cache_resource(show_spinner=False)
    # def subcription_plan(self):
    #     """
    #         Get data for all the various subscription plans
    #     """
    #     query = '''SELECT 
    #                 DATE(created_at) as date,
    #                 TO_CHAR(created_at::timestamp with time zone, 'IW') AS week_number,
    #                 TO_CHAR(created_at::timestamp with time zone, 'Month') AS month_name,
    #                 TO_CHAR(created_at::timestamp with time zone, 'YYYY') AS year,
    #                 plan_type,
    #                 insurance_duration,
    #                 sum(amount),
    #                 channel
    #             FROM 
    #                 life_insurance_healthplan
    #             WHERE 
    #                 status = 'SUCCESS'
    #             GROUP BY 
    #                 date,
    #                 week_number,
    #                 month_name,
    #                 channel,
    #                 plan_type,
    #                 insurance_duration,
    #                 year;
    #             '''
    #     try:
    #         data = self.life_connection(query)
    #     except(Exception,psycopg2.OperationalError) as e:
    #         st.error(f'Unable to connect to DB for Individual_plan, got an {e} error')
    #         print("Exception:",e)
    #         return st.stop()
    #     if data.empty:
    #         return None
    #     else:
    #         return data


# @st.cache_resource(show_spinner=False)
# def individual_plan():
    
#     """
#     Get data for when subscription_plan is 'Individual'
#     """
#     query = '''SELECT 
#                 created_at,
#                 TO_CHAR(date_created::timestamp with time zone, 'Month') AS month_name,
#                 TO_CHAR(date_created::timestamp with time zone, 'IW') AS week_number,
#                 plan_type,
#                 insurance_duration,
#                 amount,
#                 status,
#                 channel
#                FROM 
#                  life_insurance_healthplan
#                WHERE 
#                  plan_type = 'INDIVIDUAL'
#                AND  
#                  status = 'SUCCESS'
#             '''
#     try:
#         data = life_connection(query)
#     except(Exception,psycopg2.OperationalError) as e:
#         st.error(f'Unable to connect to DB for Individual_plan, got an {e} error')
#         print("Exception:",e)
#         return st.stop()
#     if data.empty:
#         return None
#     else:
#         return data
    
# individual_data = individual_plan()


# @st.cache_resource(show_spinner=False)
# def corporate_plan():
#     """
#         Get data for when subscription_plan is 'Corporate'
#     """
#     query = '''SELECT 
#                 created_at,
#                 TO_CHAR(date_created::timestamp with time zone, 'Month') AS month_name,
#                 TO_CHAR(date_created::timestamp with time zone, 'IW') AS week_number,
#                 plan_type,
#                 insurance_duration,
#                 amount,
#                 status,
#                 channel
#                FROM 
#                  life_insurance_healthplan
#                WHERE 
#                  plan_type = 'CORPORATE'
#                AND  
#                  status = 'SUCCESS'
#             '''
#     try:
#         data = life_connection(query)
#     except(Exception,psycopg2.OperationalError) as e:
#         st.error(f'Unable to connect to DB for Individual_plan, got an {e} error')
#         print("Exception:",e)
#         return st.stop()
#     if data.empty:
#         return None
#     else:
#         return data
    
# corporate_data = corporate_plan()
# ### print(corporate_data)


# @st.cache_resource(show_spinner=False)
# def family_plan():
#     """
#         Get data for when subscription_plan is 'Family'
#     """
#     query = '''SELECT 
#                 created_at,
#                 TO_CHAR(date_created::timestamp with time zone, 'Month') AS month_name,
#                 TO_CHAR(date_created::timestamp with time zone, 'IW') AS week_number,
#                 plan_type,
#                 insurance_duration,
#                 amount,
#                 status,
#                 channel
#                FROM 
#                  life_insurance_healthplan
#                WHERE 
#                  plan_type = 'FAMILY'
#                AND  
#                  status = 'SUCCESS'
#             '''
#     try:
#         data = life_connection(query)
#     except(Exception,psycopg2.OperationalError) as e:
#         st.error(f'Unable to connect to DB for Individual_plan, got an {e} error')
#         print("Exception:",e)
#         return st.stop()
#     if data.empty:
#         return None
#     else:
#         return data

# family_data = family_plan()
# #print(family_data)


