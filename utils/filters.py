# utils/filters.py
from __future__ import annotations

from datetime import date
from typing import Optional, List

import pandas as pd


def apply_date_filter(
    df: pd.DataFrame,
    start_date: Optional[date],
    end_date: Optional[date],
    ts_col: str = "timestamp",
) -> pd.DataFrame:
    """timestamp 컬럼 기준으로 날짜 필터를 적용"""
    if df.empty or ts_col not in df.columns:
        return df

    df = df.copy()
    df[ts_col] = pd.to_datetime(df[ts_col])

    if start_date:
        df = df[df[ts_col].dt.date >= start_date]
    if end_date:
        df = df[df[ts_col].dt.date <= end_date]

    return df


def apply_keyword_filter(
    df: pd.DataFrame,
    keyword: str,
    cols: Optional[List[str]] = None,
) -> pd.DataFrame:
    """여러 컬럼에 대해 OR 조건으로 키워드 필터 적용"""
    if not keyword or df.empty:
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
