import streamlit as st
from datetime import date, datetime

REPORTS = [
    {
        "id": 1,
        "title": "산업안전보건법 시행령 개정",
        "summary": "유해위험방지계획서 제출 대상 확대 및 관리 기준 강화.",
        "date": "2025-11-24",
        "link": "https://example.com/report/1",
    },
    {
        "id": 2,
        "title": "화학물질관리법 시행규칙 개정",
        "summary": "특정 유해 화학물질 취급시설의 정기 점검 주기 변경.",
        "date": "2025-11-24",
        "link": "https://example.com/report/2",
    },
    {
        "id": 3,
        "title": "고압가스안전관리법 일부 개정",
        "summary": "저장탱크 설치 기준 및 점검 항목이 구체화되었습니다.",
        "date": "2025-11-20",
        "link": "https://example.com/report/3",
    },
]

def get_today_reports():
    today_str = date.today().isoformat()
    return [r for r in REPORTS if r["date"] == today_str]

def get_report_dates():
    return sorted(set(r["date"] for r in REPORTS))

def get_reports_by_date(d: date):
    date_str = d.isoformat()
    return [r for r in REPORTS if r["date"] == date_str]

def render_main_page():

    # ======= 공통 스타일 (Tailwind 느낌으로 커스텀 CSS) =======
    st.markdown(
        """
        <style>
        /* 전체 배경색 */
        body {
            background-color: #f9fafb;
        }
        .main .block-container {
            padding-top: 0rem;
            padding-bottom: 3rem;
        }
        /* 헤더 */
        .header {
            background-color: #ffffff;
            border-bottom: 1px solid #e5e7eb;
            padding: 1.5rem 2rem;
            margin: 0 -4rem 1.5rem -4rem;
        }
        .header-inner {
            max-width: 72rem;
            margin: 0 auto;
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }
        .header-title {
            font-size: 1.25rem;
            font-weight: 600;
            color: #000000;
        }
        .header-icon {
            width: 2rem;
            height: 2rem;
            border-radius: 0.5rem;
            display: flex;
            align-items: center;
            justify-content: center;
            background-color: #eff6ff;
            color: #2563eb;
            font-size: 1.2rem;
        }


        /* 섹션 제목 */
        .section-title {
            font-size: 1.1rem;
            font-weight: 600;
            color: #111827;
            margin-bottom: 0.25rem;
        }
        .section-desc {
            font-size: 0.9rem;
            color: #4b5563;
            margin-bottom: 1.5rem;
        }

        /* 카드 공통 */
        .card {
            background-color: #ffffff;
            border-radius: 0.75rem;
            border: 1px solid #e5e7eb;
            padding: 1rem 1.25rem;
            box-shadow: 0 1px 2px rgba(0,0,0,0.02);
        }
        .card-title {
            font-size: 1rem;
            font-weight: 600;
            color: #111827;
            margin-bottom: 0.5rem;
        }
        .card-date {
            font-size: 0.8rem;
            color: #6b7280;
            margin-bottom: 0.5rem;
        }
        .card-summary {
            font-size: 0.9rem;
            color: #4b5563;
            margin-bottom: 0.75rem;
        }
        .card-link {
            font-size: 0.85rem;
            color: #2563eb;
            text-decoration: none;
            font-weight: 500;
        }
        .card-link:hover {
            text-decoration: underline;
        }

        /* 빈 상태 카드 */
        .empty-card {
            text-align: center;
            color: #6b7280;
            padding: 3rem 1rem;
        }

        /* 캘린더 컨테이너 스타일 */
        .calendar-wrapper {
            display: inline-block;
            background-color: #ffffff;
            border-radius: 0.75rem;
            border: 1px solid #e5e7eb;
            padding: 1rem;
        }
        .calendar-info {
            font-size: 0.8rem;
            color: #6b7280;
            margin-top: 0.5rem;
        }

        /* 날짜 뱃지 (리포트가 존재하는 날짜 표시용 텍스트) */
        .date-badge {
            display: inline-flex;
            align-items: center;
            padding: 0.15rem 0.5rem;
            border-radius: 999px;
            background-color: #eff6ff;
            color: #1d4ed8;
            font-size: 0.75rem;
            margin-right: 0.25rem;
            margin-bottom: 0.25rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # ======= 헤더 =======
    st.markdown(
        """
        <div class="header">
          <div class="header-inner">
            <div class="header-icon">📄</div>
            <h1 class="header-title">법령 분석 리포트</h1>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 메인 컨테이너
    main_container = st.container()
    with main_container:
        st.markdown('<div style="max-width: 72rem; margin: 0 auto;">', unsafe_allow_html=True)

        # ======= 오늘의 리포트 섹션 =======
        st.markdown('<div class="section-title">오늘의 리포트</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-desc">최신 법령 변경사항을 확인하세요</div>',
            unsafe_allow_html=True,
        )

        today_reports = get_today_reports()

        if today_reports:
            # React의 grid-cols-1 md:grid-cols-2 느낌으로 구현
            cols = st.columns(2) if len(today_reports) > 1 else [st.container()]
            for idx, report in enumerate(today_reports):
                col = cols[idx % len(cols)]
                with col:
                    st.markdown(
                        f"""
                        <div class="card">
                            <div class="card-title">{report['title']}</div>
                            <div class="card-date">{report['date']}</div>
                            <div class="card-summary">{report['summary']}</div>
                            <a class="card-link" href="{report['link']}" target="_blank">
                                리포트 자세히 보기 ↗
                            </a>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
        else:
            st.markdown(
                """
                <div class="card empty-card">
                    오늘 발행된 리포트가 없습니다.
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("---")

        # ======= 리포트 캘린더 섹션 =======
        st.markdown('<div class="section-title">리포트 캘린더</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-desc">날짜를 선택하여 해당 일자의 리포트를 확인하세요</div>',
            unsafe_allow_html=True,
        )

        report_dates = get_report_dates()
        report_dates_set = set(report_dates)

        col_cal, col_info = st.columns([1, 2])

        with col_cal:
            st.markdown('<div class="calendar-wrapper">', unsafe_allow_html=True)

            # Streamlit의 date_input은 react-calendar처럼 타일별 스타일링은 안 되지만
            # 동일한 UX 흐름(클릭 → 리포트 조회)을 제공합니다.
            selected_date = st.date_input(
                "날짜 선택",
                value=date.today(),
                format="YYYY-MM-DD",
                key="report_calendar",
            )

            # 리포트가 있는 날짜들을 텍스트로 표시
            if report_dates:
                st.markdown(
                    '<div class="calendar-info">● 리포트가 있는 날짜</div>',
                    unsafe_allow_html=True,
                )
                badge_html = ""
                for d in report_dates:
                    badge_html += f'<span class="date-badge">{d}</span>'
                st.markdown(badge_html, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

        # 선택한 날짜의 리포트 (React의 CalendarModal 대체)
        with col_info:
            st.markdown(
                f"#### 선택한 날짜: {selected_date.strftime('%Y-%m-%d')}",
            )

            selected_reports = get_reports_by_date(selected_date)

            if selected_reports:
                for r in selected_reports:
                    st.markdown(
                        f"""
                        <div class="card" style="margin-bottom: 0.75rem;">
                            <div class="card-title">{r['title']}</div>
                            <div class="card-date">{r['date']}</div>
                            <div class="card-summary">{r['summary']}</div>
                            <a class="card-link" href="{r['link']}" target="_blank">
                                리포트 자세히 보기 ↗
                            </a>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
            else:
                st.info("해당 날짜에 발행된 리포트가 없습니다.")

        st.markdown("</div>", unsafe_allow_html=True)
