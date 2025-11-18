# # infra/aws_cloudwatch.py
# from datetime import date
# import pandas as pd
# import boto3
# import streamlit as st

# from config.settings import AWS_REGION, LAMBDA_LOG_GROUPS, SES_LOG_GROUP

# @st.cache_data(ttl=60)
# def fetch_lambda_logs(start_date: date, end_date: date) -> pd.DataFrame:
#     """CloudWatch Logs에서 Lambda 로그를 조회 (예시)"""
#     # 여기서 boto3로 CloudWatch Logs Insights 호출 (이 코드는 구조 예시)
#     # client = boto3.client("logs", region_name=AWS_REGION)
#     # ...
#     # return pd.DataFrame(result)
#     # 일단 목업
#     return pd.DataFrame([])


# @st.cache_data(ttl=60)
# def fetch_ses_logs(start_date: date, end_date: date) -> pd.DataFrame:
#     """SES 관련 로그 조회 (예시)"""
#     return pd.DataFrame([])
