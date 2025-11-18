# backend.py

from __future__ import annotations

from datetime import datetime, timedelta, date
from typing import Dict, Any, List, Optional

import pandas as pd


# ------------------------
# 공통 유틸
# ------------------------
def _apply_date_filter(
    df: pd.DataFrame,
    start_date: Optional[date],
    end_date: Optional[date],
    ts_col: str = "timestamp",
) -> pd.DataFrame:
    """날짜 필터 공통 적용 (timestamp 컬럼 기준으로 날짜 비교)"""
    if df.empty:
        return df

    if ts_col not in df.columns:
        return df

    # timestamp 컬럼을 datetime 으로 보장
    df = df.copy()
    df[ts_col] = pd.to_datetime(df[ts_col])

    if start_date:
        df = df[df[ts_col].dt.date >= start_date]
    if end_date:
        df = df[df[ts_col].dt.date <= end_date]

    return df


def _apply_keyword_filter(
    df: pd.DataFrame,
    keyword: str,
    cols: Optional[List[str]] = None,
) -> pd.DataFrame:
    """키워드가 들어간 행만 남기기 (여러 컬럼 OR 검색)"""
    if not keyword:
        return df
    if df.empty:
        return df

    df = df.copy()
    keyword = str(keyword).lower()

    if cols is None:
        cols = [c for c in df.columns if df[c].dtype == "object"]

    if not cols:
        return df

    mask = False
    for col in cols:
        mask = mask | df[col].astype(str).str.lower().str.contains(keyword)

    return df[mask]


# ------------------------
# 1. Lambda 로그 (목업)
# ------------------------
def get_lambda_logs(filters: Dict[str, Any]) -> pd.DataFrame:
    """
    Lambda 로그를 가져오는 목업 함수.
    실제 환경에서는 이 부분에서 CloudWatch Logs / Insights 를 조회하면 됩니다.
    """
    now = datetime.now()

    data = [
        {
            "timestamp": now - timedelta(minutes=5),
            "function_name": "process-orders",
            "level": "INFO",
            "message": "Order processing completed successfully.",
            "request_id": "req-12345",
        },
        {
            "timestamp": now - timedelta(minutes=15),
            "function_name": "send-report-email",
            "level": "ERROR",
            "message": "Failed to send email: SES ThrottlingException",
            "request_id": "req-23456",
        },
        {
            "timestamp": now - timedelta(hours=1),
            "function_name": "sync-users",
            "level": "WARN",
            "message": "User sync delayed due to API rate limiting.",
            "request_id": "req-34567",
        },
        {
            "timestamp": now - timedelta(hours=2),
            "function_name": "sync-users",
            "level": "DEBUG",
            "message": "Sync started with batch_size=100",
            "request_id": "req-45678",
        },
    ]

    df = pd.DataFrame(data)

    # ---- 필터 적용 ----
    start_date: Optional[date] = filters.get("start_date")
    end_date: Optional[date] = filters.get("end_date")
    levels: Optional[List[str]] = filters.get("levels")
    keyword: str = filters.get("keyword", "")

    # 날짜 필터
    df = _apply_date_filter(df, start_date, end_date, ts_col="timestamp")

    # 로그 레벨 필터
    if levels:
        df = df[df["level"].isin(levels)]

    # 키워드 필터 (함수명, 메시지, request_id)
    df = _apply_keyword_filter(
        df,
        keyword,
        cols=["function_name", "message", "request_id"],
    )

    # 최신순 정렬
    df = df.sort_values("timestamp", ascending=False)

    return df.reset_index(drop=True)


# ------------------------
# 2. SES 로그 (목업)
# ------------------------
def get_ses_logs(filters: Dict[str, Any]) -> pd.DataFrame:
    """
    SES 메일 로그 목업 함수.
    실제 환경에서는 SES 이벤트(CloudWatch / EventBridge / S3)에 저장된 로그를 조회하면 됩니다.
    """
    now = datetime.now()

    data = [
        {
            "timestamp": now - timedelta(minutes=3),
            "mail_to": "user1@example.com",
            "subject": "Daily Report",
            "status": "DELIVERED",
            "event_type": "Send",
            "message_id": "msg-111",
        },
        {
            "timestamp": now - timedelta(minutes=20),
            "mail_to": "user2@example.com",
            "subject": "Password Reset",
            "status": "BOUNCE",
            "event_type": "Bounce",
            "message_id": "msg-222",
        },
        {
            "timestamp": now - timedelta(hours=2),
            "mail_to": "admin@example.com",
            "subject": "Error Notification",
            "status": "DELIVERED",
            "event_type": "Send",
            "message_id": "msg-333",
        },
        {
            "timestamp": now - timedelta(days=1),
            "mail_to": "user3@example.com",
            "subject": "Weekly Summary",
            "status": "COMPLAINT",
            "event_type": "Complaint",
            "message_id": "msg-444",
        },
    ]

    df = pd.DataFrame(data)

    # ---- 필터 적용 ----
    start_date: Optional[date] = filters.get("start_date")
    end_date: Optional[date] = filters.get("end_date")
    levels: Optional[List[str]] = filters.get("levels")  # 로그 레벨과 직접 매핑은 없지만, 예시는 남겨둠
    keyword: str = filters.get("keyword", "")

    # 날짜 필터
    df = _apply_date_filter(df, start_date, end_date, ts_col="timestamp")

    # 로그 레벨을 SES status 에 대충 매핑해보는 예시 (원하는 대로 바꾸면 됨)
    # ERROR -> BOUNCE/COMPLAINT, WARN/INFO/DEBUG -> 나머지 등등
    if levels:
        if "ERROR" in levels and not any(l in ["WARN", "INFO", "DEBUG"] for l in levels):
            df = df[df["status"].isin(["BOUNCE", "COMPLAINT"])]

    # 키워드 필터 (메일 주소, 제목, message_id)
    df = _apply_keyword_filter(
        df,
        keyword,
        cols=["mail_to", "subject", "message_id"],
    )

    df = df.sort_values("timestamp", ascending=False)

    return df.reset_index(drop=True)


# ------------------------
# 3. 리포트 목록 (목업)
# ------------------------
def get_reports(filters: Dict[str, Any]) -> pd.DataFrame:
    """
    리포트 목록 목업 함수.
    실제 환경에서는 DB / S3 등에 저장된 메타데이터를 조회하면 됩니다.
    """
    now = datetime.now()

    data = [
        {
            "report_name": "Lambda Error Summary (오늘)",
            "created_at": now - timedelta(minutes=10),
            "description": "오늘 발생한 Lambda ERROR 로그를 요약한 리포트입니다.",
            "file_url": "https://example.com/reports/lambda-error-today.pdf",
        },
        {
            "report_name": "SES Bounce Report (이번 주)",
            "created_at": now - timedelta(hours=3),
            "description": "이번 주동안 BOUNCE 된 메일을 정리한 리포트입니다.",
            "file_url": "https://example.com/reports/ses-bounce-week.xlsx",
        },
        {
            "report_name": "주간 시스템 리포트",
            "created_at": now - timedelta(days=2),
            "description": "주요 Lambda/SES 활동을 종합한 주간 리포트입니다.",
            "file_url": "https://example.com/reports/system-weekly.html",
        },
    ]

    df = pd.DataFrame(data)

    keyword: str = filters.get("keyword", "")
    selected_date: Optional[date] = filters.get("date")

    # 키워드 필터 (리포트 이름, 설명)
    df = _apply_keyword_filter(
        df,
        keyword,
        cols=["report_name", "description"],
    )

    # 생성일 기준 날짜 필터 (date input 을 사용하므로 '같은 날짜' 기준)
    if selected_date:
        df = df[pd.to_datetime(df["created_at"]).dt.date == selected_date]

    df = df.sort_values("created_at", ascending=False)

    return df.reset_index(drop=True)
