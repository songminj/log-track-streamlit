# report_detail_app.py
import streamlit as st
from datetime import date

# ---------- 페이지 기본 설정 ----------
st.set_page_config(
    page_title="법령 분석 리포트 상세",
    page_icon="📄",
    layout="wide",
)

# ---------- Mock Data & Helper ----------
REPORTS = [
    {
        "id": "1",
        "lawName": "산업안전보건법 시행령",
        "title": "산업안전보건법 시행령 개정에 따른 안전관리 규정 강화",
        "publishDate": "2025-11-24",
        "summary": "홈페이지 첫 화면 공개 의무화 및 사전 공지 의무가 신설되며, 근로자 알권리 보장이 강화됩니다.",
        "beforeChange": "기존에는 사업장 내 게시판 비치 또는 홈페이지 공지 중 하나만으로도 충분했습니다.",
        "afterChange": "개정 후에는 사업장 홈페이지 첫 화면에 안전관리 규정 변경사항을 의무적으로 공개해야 하며, 변경 7일 전 사전 공지 의무가 신설되었습니다.",
        "impactScore": 8.5,
        "impactReason": "안전 규정 공개와 사전 공지 의무가 강화됨에 따라, 내부 커뮤니케이션 및 시스템 개편이 필요하며, 이를 소홀히 할 경우 과태료 위험이 높습니다.",
        "riskAnalysis": {
            "level": "high",
            "description": "공지 미이행 시 제재 및 근로자 민원 발생 가능성이 높습니다.",
            "concerns": [
                "홈페이지 개편 지연 시 법 위반 소지",
                "사전 공지 누락으로 인한 민원/분쟁 발생",
                "지점/사업장별 공지 수준 편차로 인한 리스크"
            ]
        },
        "responseStrategy": {
            "shortTerm": [
                "홈페이지 메인 화면에 안전규정 공지 영역 신설",
                "변경 시 7일 전 자동 안내 메일/문자 발송 플로우 설계",
                "법무/안전부서와 협업하여 공지 템플릿 표준화"
            ],
            "longTerm": [
                "안전 규정 변경 관리 시스템 구축",
                "지점/사업장별 공지 이행 현황 모니터링 대시보드 운영",
                "정기 교육 커리큘럼에 관련 내용 반영"
            ]
        }
    },
    # 필요하면 2, 3, 4도 이 형식으로 추가
]

def get_report_by_id(report_id: str):
    for r in REPORTS:
        if r["id"] == report_id:
            return r
    return None

def get_risk_color(level: str):
    # 텍스트/배경색 조합 (간단 버전)
    if level == "high":
        return "#fee2e2", "#b91c1c"   # bg, text
    if level == "medium":
        return "#ffedd5", "#c2410c"
    if level == "low":
        return "#dcfce7", "#15803d"
    return "#f9fafb", "#4b5563"

def get_risk_label(level: str):
    if level == "high":
        return "높음"
    if level == "medium":
        return "보통"
    if level == "low":
        return "낮음"
    return level
  
def render_report_by_id(report_id: str):
    if not report_id:
        st.error("리포트 ID가 지정되지 않았습니다. (?id=1 형태로 접근해 주세요.)")
        st.stop()
    # ---------- 공통 스타일 ----------
    st.markdown(
        """
        <style>
        html, body, [data-testid="stAppViewContainer"], [data-testid="stAppViewContainer"] > .main {
            background-color: #ffffff !important;
        }

        /* 중앙 컨테이너 (block-container)도 흰색 */
        .main .block-container {
            background-color: #ffffff !important;
            padding-top: 0rem;
            padding-bottom: 3rem;
        }

        .header {
            background-color: #ffffff;
            border-bottom: 1px solid #e5e7eb;
            padding: 1.5rem 2rem;
            margin: 0 -4rem 1.5rem -4rem;
        }
        .header-inner {
            max-width: 60rem;
            margin: 0 auto;
        }
        .back-link {
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            color: #4b5563;
            font-size: 0.9rem;
            text-decoration: none;
            margin-bottom: 1rem;
        }
        .back-link:hover {
            color: #111827;
            text-decoration: underline;
        }
        .header-title-row {
            display: flex;
            justify-content: space-between;
            gap: 1.5rem;
        }
        .law-chip {
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            font-size: 0.85rem;
            color: #2563eb;
            margin-bottom: 0.5rem;
        }
        .law-icon {
            width: 1.5rem;
            height: 1.5rem;
            border-radius: 999px;
            background-color: #eff6ff;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.85rem;
        }
        .header-title {
            font-size: 1.3rem;
            font-weight: 600;
            color: #111827;
            margin-bottom: 0.25rem;
        }
        .header-date {
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            font-size: 0.85rem;
            color: #6b7280;
        }
        .meta-card {
            background-color: #ffffff;    
            border-radius: 0.75rem;
            color: #111827;   
        }

        .section-card {
            background-color: #ffffff;
            border-radius: 0.75rem;
            border: 1px solid #e5e7eb;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
        }
        .section-title {
            font-size: 1.05rem;
            font-weight: 600;
            color: #111827;
            margin-bottom: 0.75rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        .section-subtext {
            font-size: 0.9rem;
            color: #4b5563;
        }

        .summary-card {
            background-color: #eff6ff;
            border: 1px solid #bfdbfe;
            border-radius: 0.75rem;
            padding: 1.25rem 1.5rem;
            margin-bottom: 1.5rem;
        }

        .pill-label {
            font-size: 0.9rem;
            border-radius: 999px;
            padding: 0.4rem 1rem;
            border: 1px solid transparent;
        }

        .flex-row {
            display: flex;
            gap: 1.5rem;
        }
        .flex-col {
            flex: 1;
        }

        .impact-bar-bg {
            width: 12rem;
            height: 0.5rem;
            background-color: #e5e7eb;
            border-radius: 999px;
            overflow: hidden;
        }
        .impact-bar-fill {
            height: 100%;
            background: linear-gradient(to right, #22c55e, #eab308, #ef4444);
            border-radius: 999px;
        }

        .chip-small {
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            padding: 0.15rem 0.6rem;
            border-radius: 999px;
            font-size: 0.75rem;
            background-color: #eef2ff;
            color: #4338ca;
            margin-bottom: 0.5rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # ---------- URL에서 id 읽기 ----------
    # http://localhost:8501/?id=1 같이 호출한다고 가정

    if not report_id:
        st.error("리포트 ID가 지정되지 않았습니다. (?id=1 형태로 접근해 주세요.)")
        st.stop()

    report = get_report_by_id(report_id)

    if not report:
        st.markdown(
            """
            <div style="min-height: 60vh; display:flex; align-items:center; justify-content:center;">
              <div style="text-align:center;">
                <h2 style="font-size:1.1rem; margin-bottom:0.75rem;">리포트를 찾을 수 없습니다</h2>
                <p style="font-size:0.9rem; color:#4b5563;">올바른 리포트 ID인지 확인해 주세요.</p>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.stop()

    # ---------- 헤더 ----------
    bg_color, text_color = get_risk_color(report["riskAnalysis"]["level"])
    risk_label = get_risk_label(report["riskAnalysis"]["level"])

    st.markdown(
        f"""
        <div class="header">
          <div class="header-inner">
            <a class="back-link" href="javascript:history.back()">
              ← 목록으로 돌아가기
            </a>
            <div class="header-title-row">
              <div>
                <div class="law-chip">
                  <div class="law-icon">📑</div>
                  <span>{report["lawName"]}</span>
                </div>
                <h1 class="header-title">{report["title"]}</h1>
                <div class="header-date">
                  <span>📅</span>
                  <span>{report["publishDate"]}</span>
                </div>
              </div>
              <div>
                <span
                  class="pill-label"
                  style="background-color:{bg_color}; color:{text_color}; border-color:{text_color}33; border-width:1px; border-style:solid;"
                >
                  리스크: {risk_label}
                </span>
              </div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 헤더 바로 아래에 배치
    with st.container():
        col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""
            <div class="meta-card">
              <div class="meta-label">Risk Level</div>
              <div class="meta-value">{risk_label}</div>
              <div class="meta-sub">법 위반·민원 발생 가능성</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div class="meta-card">
              <div class="meta-label">Impact Score</div>
              <div class="meta-value">{10}/10</div>
              <div class="meta-sub">내부 시스템·운영 영향도 종합</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
            <div class="meta-card">
              <div class="meta-label">시행 대비</div>
              <div class="meta-value">사전 준비 필요</div>
              <div class="meta-sub">공지·커뮤니케이션 체계 점검 권장</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


    # ---------- 메인 컨테이너 ----------
    st.markdown('<div style="max-width: 60rem; margin: 0 auto; padding: 1.5rem 1.5rem 3rem 1.5rem;">',
                unsafe_allow_html=True)

    # ==== 1. 리포트 요약 ====
    st.markdown(
        f"""
        <div class="summary-card">
          <div style="display:flex; gap:0.75rem;">
            <div style="flex-shrink:0; width:2.25rem; height:2.25rem; border-radius:999px; background:#dbeafe; display:flex; align-items:center; justify-content:center; font-size:1.2rem; margin-top:0.25rem;">
              📄
            </div>
            <div>
              <div style="font-size:1.05rem; font-weight:600; color:#111827; margin-bottom:0.5rem;">리포트 요약</div>
              <p style="font-size:0.9rem; color:#374151; line-height:1.6;">
                {report["summary"]}
              </p>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ==== 2. 법령 변경 내용 상세 비교 ====
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-title">법령 변경 내용 상세 비교</div>',
        unsafe_allow_html=True,
    )

    # Before/After 두 칼럼
    col_before, col_after = st.columns(2)

    with col_before:
        st.markdown(
            """
            <div style="position:relative; border-radius:0.75rem; border:2px solid #fecaca; background:linear-gradient(135deg,#fee2e2,#fee2e2); padding:1.25rem 1.5rem; margin-bottom:0.75rem;">
              <div style="position:absolute; top:-0.8rem; left:1rem; background:#dc2626; color:#fff; padding:0.25rem 0.75rem; border-radius:999px; font-size:0.8rem;">
                기존 규정
              </div>
              <div style="margin-top:0.5rem; font-size:0.9rem; color:#1f2937; line-height:1.6;">
            """,
            unsafe_allow_html=True,
        )
        st.markdown(report["beforeChange"], unsafe_allow_html=True)
        st.markdown("</div></div>", unsafe_allow_html=True)

    with col_after:
        st.markdown(
            """
            <div style="position:relative; border-radius:0.75rem; border:2px solid #bbf7d0; background:linear-gradient(135deg,#dcfce7,#ecfdf5); padding:1.25rem 1.5rem; margin-bottom:0.75rem;">
              <div style="position:absolute; top:-0.8rem; left:1rem; background:#16a34a; color:#fff; padding:0.25rem 0.75rem; border-radius:999px; font-size:0.8rem;">
                개정 규정
              </div>
              <div style="margin-top:0.5rem; font-size:0.9rem; color:#1f2937; line-height:1.6;">
            """,
            unsafe_allow_html=True,
        )
        st.markdown(report["afterChange"], unsafe_allow_html=True)
        st.markdown("</div></div>", unsafe_allow_html=True)

    # 주요 변경사항 (id별 분기)
    st.markdown(
        """
        <div style="margin-top:1rem; background:#eff6ff; border:1px solid #bfdbfe; border-radius:0.75rem; padding:1rem 1.25rem;">
          <div style="display:flex; align-items:center; gap:0.5rem; margin-bottom:0.75rem;">
            <div style="width:0.25rem; height:1.1rem; border-radius:999px; background:#2563eb;"></div>
            <div style="font-weight:600; color:#111827; font-size:0.95rem;">주요 변경사항</div>
          </div>
        """,
        unsafe_allow_html=True,
    )

    if report["id"] == "1":
        st.markdown(
            """
            <ul style="list-style:none; padding-left:0; margin:0;">
              <li style="margin-bottom:0.5rem;">
                1) <span style="text-decoration:line-through; color:#b91c1c;">홈페이지 또는 사업장 비치</span>
                → <span style="color:#15803d;">홈페이지 첫 화면 공개 의무화</span>
              </li>
              <li style="margin-bottom:0.5rem;">
                2) <span style="color:#15803d;">신규 추가:</span> 변경 시 7일 전 사전 공지 의무
              </li>
              <li>
                3) <span style="color:#15803d;">신규 추가:</span> 간편 열람 요청 온라인 시스템 제공 의무
              </li>
            </ul>
            """,
            unsafe_allow_html=True,
        )
    # (필요하면 2,3,4도 elif로 추가)

    st.markdown("</div></div>", unsafe_allow_html=True)  # 주요 변경사항 card + section-card 닫기

    # ==== 3. 영향도 평가 ====
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="section-title">
          <span>📈</span>
          <span>영향도 평가</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    impact_score = report["impactScore"]
    impact_width = min(max(impact_score * 10, 0), 100)  # 0~100%

    st.markdown(
        f"""
        <div style="background:#f5f3ff; border:1px solid #ddd6fe; border-radius:0.75rem; padding:1rem 1.25rem; margin-bottom:0.75rem;">
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <span style="font-size:0.9rem; color:#374151;">영향도 점수</span>
            <div style="display:flex; align-items:center; gap:0.5rem;">
              <div class="impact-bar-bg">
                <div class="impact-bar-fill" style="width:{impact_width}%;"></div>
              </div>
              <span style="font-size:0.9rem; font-weight:600; color:#4c1d95; min-width:3.5rem; text-align:right;">
                {impact_score}/10
              </span>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div style="background:#f9fafb; border-radius:0.75rem; padding:1rem 1.25rem;">
          <div style="font-weight:600; color:#111827; font-size:0.95rem; margin-bottom:0.5rem;">평가 근거</div>
          <p style="font-size:0.9rem; color:#374151; line-height:1.6;">
            {report["impactReason"]}
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)  # section-card

    # ==== 4. 리스크 분석 ====
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="section-title">
          <span>⚠️</span>
          <span>리스크 분석</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <p class="section-subtext">
          {report["riskAnalysis"]["description"]}
        </p>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div style="margin-top:0.75rem; background:#fffbeb; border:1px solid #fed7aa; border-radius:0.75rem; padding:1rem 1.25rem;">
          <div style="font-weight:600; color:#111827; font-size:0.95rem; margin-bottom:0.5rem;">주요 우려사항</div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<ul style='list-style:none; padding-left:0; margin:0;'>", unsafe_allow_html=True)
    for c in report["riskAnalysis"]["concerns"]:
        st.markdown(
            f"""
            <li style="display:flex; gap:0.5rem; margin-bottom:0.4rem;">
              <span style="width:0.4rem; height:0.4rem; border-radius:999px; background:#ea580c; margin-top:0.4rem;"></span>
              <span style="font-size:0.9rem; color:#374151; line-height:1.6;">{c}</span>
            </li>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("</ul></div></div>", unsafe_allow_html=True)  # 우려사항 card + section-card

    # ==== 5. 대응 전략 ====
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="section-title">
          <span>🎯</span>
          <span>대응 전략</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_short, col_long = st.columns(2)

    with col_short:
        st.markdown(
            """
            <div style="background:#fefce8; border:1px solid #facc15; border-radius:0.75rem; padding:1rem 1.25rem;">
              <div style="display:flex; align-items:center; gap:0.4rem; margin-bottom:0.5rem;">
                <span>⚡</span>
                <span style="font-weight:600; color:#92400e;">단기 대응</span>
              </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("<ul style='list-style:none; padding-left:0; margin:0;'>", unsafe_allow_html=True)
        for i, s_item in enumerate(report["responseStrategy"]["shortTerm"], start=1):
            st.markdown(
                f"""
                <li style="display:flex; gap:0.5rem; margin-bottom:0.4rem;">
                  <div style="width:1.5rem; height:1.5rem; border-radius:999px; background:#fef3c7; display:flex; align-items:center; justify-content:center; font-size:0.85rem; color:#92400e; flex-shrink:0; margin-top:0.1rem;">
                    {i}
                  </div>
                  <span style="font-size:0.9rem; color:#374151; line-height:1.6;">{s_item}</span>
                </li>
                """,
                unsafe_allow_html=True,
            )
        st.markdown("</ul></div>", unsafe_allow_html=True)

    with col_long:
        st.markdown(
            """
            <div style="background:#ecfdf5; border:1px solid #22c55e; border-radius:0.75rem; padding:1rem 1.25rem;">
              <div style="display:flex; align-items:center; gap:0.4rem; margin-bottom:0.5rem;">
                <span>⏱️</span>
                <span style="font-weight:600; color:#166534;">중장기 대응</span>
              </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("<ul style='list-style:none; padding-left:0; margin:0;'>", unsafe_allow_html=True)
        for i, l_item in enumerate(report["responseStrategy"]["longTerm"], start=1):
            st.markdown(
                f"""
                <li style="display:flex; gap:0.5rem; margin-bottom:0.4rem;">
                  <div style="width:1.5rem; height:1.5rem; border-radius:999px; background:#bbf7d0; display:flex; align-items:center; justify-content:center; font-size:0.85rem; color:#166534; flex-shrink:0; margin-top:0.1rem;">
                    {i}
                  </div>
                  <span style="font-size:0.9rem; color:#374151; line-height:1.6;">{l_item}</span>
                </li>
                """,
                unsafe_allow_html=True,
            )
        st.markdown("</ul></div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)  # section-card 종료
    st.markdown("</div>", unsafe_allow_html=True)  # outer container 종료
