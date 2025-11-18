# ui/logs_tab.py
import streamlit as st
from datetime import datetime, timedelta
from services.logs_service import get_lambda_logs_df, get_ses_logs_df

def render_logs_tab():
    st.subheader("🧾 Lambda / SES 로그 조회")

    # sidebar 필터
    with st.sidebar:
        st.markdown("### 🔍 로그 필터")
        start, end = st.date_input(
            "조회 기간",
            value=(
                datetime.today().date() - timedelta(days=1),
                datetime.today().date(),
            ),
        )
        log_levels = st.multiselect(
            "Log Level",
            ["ERROR", "WARN", "INFO", "DEBUG"],
            default=["ERROR", "WARN", "INFO"],
        )
        keyword = st.text_input("검색 키워드", "")

    lambda_tab, ses_tab = st.tabs(["🐑 Lambda 로그", "✉️ SES 로그"])

    with lambda_tab:
        df = get_lambda_logs_df(start, end, log_levels, keyword)
        _render_log_table(df)

    with ses_tab:
        df = get_ses_logs_df(start, end, log_levels, keyword)
        _render_log_table(df)


def _render_log_table(df):
    if df is None or df.empty:
        st.info("조건에 해당하는 로그가 없습니다.")
        return

    st.dataframe(df, use_container_width=True, hide_index=True)
