# services/logs_service.py
import pandas as pd
# from infra.aws_cloudwatch import fetch_lambda_logs, fetch_ses_logs
from utils.filters import apply_date_filter, apply_keyword_filter

def get_lambda_logs_df(start_date, end_date, levels, keyword) -> pd.DataFrame:
    # raw_df = fetch_lambda_logs(start_date, end_date)
    # df = raw_df.copy()

    # if levels:
    #     df = df[df["level"].isin(levels)]

    # df = apply_keyword_filter(df, keyword, cols=["function_name", "message"])
    # df = df.sort_values("timestamp", ascending=False)
    # return df.reset_index(drop=True)
    return


def get_ses_logs_df(start_date, end_date, levels, keyword) -> pd.DataFrame:
    # raw_df = fetch_ses_logs(start_date, end_date)
    # df = raw_df.copy()

    # # 필요하면 levels로 SES status 매핑
    # df = apply_keyword_filter(df, keyword, cols=["mail_to", "subject"])
    # df = df.sort_values("timestamp", ascending=False)
    # return df.reset_index(drop=True)
    return 
