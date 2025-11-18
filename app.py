# app.py

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# backend.py 에서 아래 함수들이 제공된다고 가정합니다.
# 실제 구현은 나중에 backend.py 에서 하면 됩니다.
from backend import (
    get_lambda_logs,   # def get_lambda_logs(filters: dict) -> pd.DataFrame
    get_ses_logs,      # def get_ses_logs(filters: dict) -> pd.DataFrame
    get_reports,       # def get_reports(filters: dict) -> pd.DataFrame
)

@st.dialog("리포트 재발송 확인")
def show_resend_modal(selected_reports: pd.DataFrame):
    st.markdown("다음 리포트를 재발송합니다:")
    st.table(
        selected_reports[["report_name", "created_at", "description"]]
        if all(c in selected_reports.columns for c in ["report_name", "created_at", "description"])
        else selected_reports
    )

    st.markdown("---")
    st.markdown("### 📧 수신할 이메일 목록")

    # 필요하다면, 나중에 report DataFrame 안의 컬럼들에서 기본 이메일을 뽑아서 미리 채워넣어도 됨
    default_emails = st.session_state.get("last_resend_emails", "")
    emails = st.text_area(
        "이메일 주소들을 ,(콤마)로 구분해서 입력하세요",
        value=default_emails,
        key="resend_email_text",
        height=100,
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ 보내기"):
            # TODO: 실제 재발송 로직을 여기에 연결 (예: backend.resend_reports(selected_reports, emails))
            st.success("리포트 재발송 요청을 완료했습니다.")
            st.session_state["last_resend_emails"] = emails
            st.session_state["report_resend_mode"] = False
            st.rerun()  # 모달 닫기

    with col2:
        if st.button("❌ 취소"):
            st.info("재발송을 취소했습니다.")
            st.rerun()  # 모달 닫기



# ----------------------------
# 공통 설정
# ----------------------------
st.set_page_config(
    page_title="AWS CloudWatch Log Manager",
    layout="wide",
)

st.title("📊 AWS CloudWatch Log Manager")

st.caption(
    "Lambda / SES 로그를 한 곳에서 조회하고, 생성된 리포트를 관리하는 대시보드입니다."
)

# ----------------------------
# 상단 탭 (네비게이션)
# ----------------------------
log_tab, report_tab = st.tabs(["🧾 로그", "📂 리포트"])


# ----------------------------
# 1. 로그 탭
# ----------------------------
with log_tab:
    st.subheader("🧾 Lambda / SES 로그 조회")

    # 공통 필터 영역
    with st.sidebar:
        st.markdown("### 🔍 로그 필터")
        log_date_range = st.date_input(
            "조회 기간",
            value=(
                datetime.today().date() - timedelta(days=1),
                datetime.today().date(),
            ),
        )
        if isinstance(log_date_range, tuple) and len(log_date_range) == 2:
            start_date, end_date = log_date_range
        else:
            # 단일 날짜 선택 시 대비
            start_date = log_date_range
            end_date = log_date_range

        log_level = st.multiselect(
            "Log Level",
            options=["ERROR", "WARN", "INFO", "DEBUG"],
            default=["ERROR", "WARN", "INFO"],
        )
        keyword = st.text_input("검색 키워드 (함수명, 메시지 등)", value="")

        st.markdown("---")
        st.markdown("**필터 요약**")
        st.write(f"기간: {start_date} ~ {end_date}")
        st.write(f"레벨: {', '.join(log_level) if log_level else '전체'}")
        st.write(f"키워드: `{keyword}`" if keyword else "키워드: 전체")

    # Lambda / SES 별 서브 탭
    lambda_tab, ses_tab = st.tabs(["🐑 Lambda 로그", "✉️ SES 메일 로그"])

    # ------------------------
    # Lambda 로그 탭
    # ------------------------
    with lambda_tab:
        st.markdown("#### 🐑 Lambda 로그")

        lambda_filters = {
            "start_date": start_date,
            "end_date": end_date,
            "levels": log_level,
            "keyword": keyword,
        }

        try:
            lambda_logs: pd.DataFrame = get_lambda_logs(lambda_filters)
        except Exception as e:
            st.error(f"Lambda 로그를 불러오는 중 오류가 발생했습니다: {e}")
            lambda_logs = pd.DataFrame()

        if lambda_logs is None or lambda_logs.empty:
            st.info("조건에 해당하는 Lambda 로그가 없습니다.")
        else:
            # 중요한 컬럼 순서 예시 (backend 에서 컬럼명 맞춰주면 좋음)
            preferred_cols = [
                "timestamp",
                "function_name",
                "level",
                "message",
                "request_id",
            ]
            display_cols = [c for c in preferred_cols if c in lambda_logs.columns] or lambda_logs.columns
            st.dataframe(
                lambda_logs[display_cols],
                use_container_width=True,
                hide_index=True,
            )

            with st.expander("📌 선택한 로그 상세 보기 (행 클릭 후 인덱스 입력)", expanded=False):
                selected_index = st.number_input(
                    "상세 로그를 확인할 행 번호 (0부터 시작)",
                    min_value=0,
                    max_value=len(lambda_logs) - 1,
                    value=0,
                    step=1,
                )
                row = lambda_logs.iloc[int(selected_index)]
                st.json(row.to_dict())

    # ------------------------
    # SES 로그 탭
    # ------------------------
    with ses_tab:
        st.markdown("#### ✉️ SES 메일 로그")

        ses_filters = {
            "start_date": start_date,
            "end_date": end_date,
            "levels": log_level,
            "keyword": keyword,
        }

        try:
            ses_logs: pd.DataFrame = get_ses_logs(ses_filters)
        except Exception as e:
            st.error(f"SES 로그를 불러오는 중 오류가 발생했습니다: {e}")
            ses_logs = pd.DataFrame()

        if ses_logs is None or ses_logs.empty:
            st.info("조건에 해당하는 SES 로그가 없습니다.")
        else:
            preferred_cols = [
                "timestamp",
                "mail_to",
                "subject",
                "status",
                "event_type",
                "message_id",
            ]
            display_cols = [c for c in preferred_cols if c in ses_logs.columns] or ses_logs.columns
            st.dataframe(
                ses_logs[display_cols],
                use_container_width=True,
                hide_index=True,
            )

            with st.expander("📌 선택한 메일 로그 상세 보기 (행 클릭 후 인덱스 입력)", expanded=False):
                selected_index = st.number_input(
                    "상세 메일 로그를 확인할 행 번호 (0부터 시작)",
                    min_value=0,
                    max_value=len(ses_logs) - 1,
                    value=0,
                    step=1,
                    key="ses_detail_index",
                )
                row = ses_logs.iloc[int(selected_index)]
                st.json(row.to_dict())


# ----------------------------
# 2. 리포트 탭
# ----------------------------
with report_tab:
    st.subheader("📂 생성된 리포트 관리")

    # 리포트 필터
    col1, col2 = st.columns([2, 1])
    with col1:
        report_keyword = st.text_input("리포트 검색 (이름, 설명 등)", value="")
    with col2:
        report_date = st.date_input(
            "생성일 기준 (선택 사항)",
            value=None,
        )

    report_filters = {
        "keyword": report_keyword,
        "date": report_date,
    }

    try:
        reports: pd.DataFrame = get_reports(report_filters)
    except Exception as e:
        st.error(f"리포트를 불러오는 중 오류가 발생했습니다: {e}")
        reports = pd.DataFrame()
        
    # --- 재발송 모드 상태 초기화 ---
    if "report_resend_mode" not in st.session_state:
        st.session_state["report_resend_mode"] = False
        
    if reports is None or reports.empty:
        st.info("현재 조건에 해당하는 리포트가 없습니다.")
    else:
        st.markdown("#### 📑 리포트 목록")

        # 보여줄 대표 컬럼 (backend에서 이 컬럼들 맞춰주면 좋음)
        preferred_cols = [
            "report_name",
            "created_at",
            "description",
            "file_url",
        ]
        display_cols = [c for c in preferred_cols if c in reports.columns] or reports.columns

        # 테이블 형태로 확인 (file_url은 숨기고, 아래에서 버튼으로 제공)
        table_cols = [c for c in display_cols if c != "file_url"]

        # st.dataframe(
        #     reports[table_cols],
        #     use_container_width=True,
        #     hide_index=True,
        # )

          # 상단에 재발송 모드 토글 버튼
        col_btn1, col_btn2 = st.columns([1, 1])
        with col_btn1:
            toggle_label = (
                "🔁 재발송 모드 활성화"
                if not st.session_state["report_resend_mode"]
                else "❌ 재발송 모드 종료"
            )
            if st.button(toggle_label, key="toggle_resend_mode"):
                st.session_state["report_resend_mode"] = not st.session_state["report_resend_mode"]
                st.rerun()

        # --- 재발송 모드가 아닐 때: 그냥 테이블만 보여주기 ---
        if not st.session_state["report_resend_mode"]:
            st.dataframe(
                reports[table_cols],
                use_container_width=True,
                hide_index=True,
            )

        # --- 재발송 모드일 때: 체크박스 + 발송하기 버튼 ---
        else:
            st.info("재발송할 리포트를 선택한 후, 아래의 **발송하기** 버튼을 눌러주세요.")

            selected_indices = []

            # 각 행 옆에 체크박스 + 간단 정보
            for idx, row in reports.iterrows():
                row_cols = st.columns([0.08, 0.92])
                with row_cols[0]:
                    checked = st.checkbox(
                        "",
                        key=f"report_select_{idx}",
                    )
                with row_cols[1]:
                    # 리포트 요약 정보
                    name = row.get("report_name", "이름 없음")
                    created_at = row.get("created_at", "")
                    desc = row.get("description", "")

                    st.markdown(f"**{name}**")
                    if created_at is not None:
                        st.caption(str(created_at))
                    if isinstance(desc, str) and desc:
                        st.write(desc)

                st.markdown("---")

                if checked:
                    selected_indices.append(idx)

            # 발송하기 버튼
            if st.button("📨 발송하기", key="send_resend"):
                if not selected_indices:
                    st.warning("재발송할 리포트를 하나 이상 선택해주세요.")
                else:
                    selected_reports = reports.loc[selected_indices]
                    # 모달 열기
                    show_resend_modal(selected_reports)
                    
        st.markdown("---")
        st.markdown("#### 📎 리포트 열기")

        for idx, row in reports.iterrows():
            cols = st.columns([3, 2, 2])
            with cols[0]:
                st.markdown(f"**{row.get('report_name', '이름 없음')}**")
                if "description" in row and isinstance(row["description"], str):
                    st.caption(row["description"])
            with cols[1]:
                created_at = row.get("created_at")
                if isinstance(created_at, (datetime, pd.Timestamp)):
                    st.write(created_at.strftime("%Y-%m-%d %H:%M"))
                else:
                    st.write(created_at or "-")
            with cols[2]:
                file_url = row.get("file_url")
                if file_url:
                    st.link_button("열기 🔗", file_url)
                else:
                    st.write("URL 없음")

            st.markdown("---")
