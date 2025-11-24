# app.py
import streamlit as st
from pages.main import render_main_page
from pages.report import render_report_by_id

# 페이지 설정 (한 번만!)
st.set_page_config(
    page_title="법령 분석 리포트",
    page_icon="📄",
    layout="wide",
)

# 1) 쿼리 읽기 (QueryParamsProxy 객체)
qp = st.query_params  # ✅ 괄호 없이 사용

report_id = None
page_mode = "main"  # 기본은 메인 페이지

if "id" in qp:                      # ✅ 키가 있는지 먼저 확인
    report_id = qp["id"]            # 값은 문자열 (예: "1")
    page_mode = "report_by_id"

# 2) 모드에 따라 라우팅
if page_mode == "main":
    render_main_page()

elif page_mode == "report_by_id":
    if not report_id:
        st.error("리포트 ID가 비어 있습니다. 예) /?id=1")
    else:
        # report_id는 문자열이므로 그대로 넘기면 됩니다.
        render_report_by_id(report_id)
