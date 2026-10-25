from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

# Streamlit 페이지 설정
st.set_page_config(
    page_title="eSports Biometrics & Cognitive Analytics",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Streamlit 기본 여백 최소화 (대시보드가 꽉 차게 보이도록 설정)
st.markdown(
    """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .block-container {
            padding-top: 0rem;
            padding-bottom: 0rem;
            padding-left: 0rem;
            padding-right: 0rem;
            max-width: 100%;
        }
        iframe {
            border: none;
            width: 100% !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# index.html 파일 로드 및 임베딩
html_path = Path(__file__).parent / "index.html"

if html_path.exists():
    with open(html_path, "r", encoding="utf-8") as f:
        html_code = f.read()
    # 대시보드 전체를 포함할 수 있도록 넉넉한 높이 및 스크롤 허용
    components.html(html_code, height=2400, scrolling=True)
else:
    st.error("대시보드 HTML 파일(index.html)을 찾을 수 없습니다.")