import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# ==========================================
# 0. Streamlit 페이지 설정
# ==========================================
st.set_page_config(
    page_title="e스포츠 인지능력 분석 대시보드",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 커스텀 CSS (KPI 카드 및 여백 스타일링)
st.markdown("""
<style>
    .kpi-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 16px 20px;
        border-left: 5px solid #3498db;
        box-shadow: 0 2px 4px rgba(0,0,0,0.06);
        margin-bottom: 12px;
    }
    .kpi-title {
        font-size: 14px;
        color: #7f8c8d;
        font-weight: 600;
        margin-bottom: 4px;
    }
    .kpi-value {
        font-size: 26px;
        font-weight: 800;
        color: #2c3e50;
    }
    .kpi-sub {
        font-size: 12px;
        color: #95a5a6;
        margin-top: 2px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 1. 데이터 로드 및 전처리 (캐싱)
# ==========================================
@st.cache_data
def load_data():
    csv_path = r"c:\Users\30nuy\OneDrive\바탕 화면\Practice\archive\esports_gaming_biometrics_250k.csv"
    if not os.path.exists(csv_path):
        # 상대 경로 시도
        csv_path = "archive/esports_gaming_biometrics_250k.csv"
    
    df = pd.read_csv(csv_path)
    
    # 수면 구간 레이블링
    bins = [-np.inf, 4, 6, 7, 8, np.inf]
    labels = ['4시간 이하 (위험)', '4~6시간 (부족)', '6~7시간 (경계)', '7~8시간 (적정)', '8시간 초과 (충분)']
    df['Sleep_Segment'] = pd.cut(df['Sleep_Hours'], bins=bins, labels=labels)
    return df

with st.spinner("250,000건의 e스포츠 생체 데이터를 로딩하는 중입니다..."):
    df = load_data()

# ==========================================
# 2. 헤더 및 상단 KPI 카드 섹션
# ==========================================
st.title("🎮 [주제3: 수면 & 에너지드링크 기반 인지능력 분석 대시보드]")
st.markdown("프로게이머의 **수면 시간**과 **에너지 드링크 섭취량**이 인지 반응 속도(`Reaction_Time_ms`) 및 심박수에 미치는 영향을 실증 분석한 의사결정 대시보드입니다.")
st.markdown("---")

# 상단 KPI 카드 (3-Column)
kpi1, kpi2, kpi3 = st.columns(3)

with kpi1:
    st.markdown("""
    <div class="kpi-card" style="border-left-color: #e74c3c;">
        <div class="kpi-title">⏱️ 수면 1시간당 반응속도 손실</div>
        <div class="kpi-value" style="color: #c0392b;">+14.2 ms</div>
        <div class="kpi-sub">수면 박탈 시 회귀계수 기반 인지 반응 지연</div>
    </div>
    """, unsafe_allow_html=True)

with kpi2:
    st.markdown("""
    <div class="kpi-card" style="border-left-color: #e67e22;">
        <div class="kpi-title">⚠️ 에너지드링크 과섭취 임계점</div>
        <div class="kpi-value" style="color: #d35400;">3캔 이상</div>
        <div class="kpi-sub">2캔 최적 정점 후 반응속도 급격 악화 지점</div>
    </div>
    """, unsafe_allow_html=True)

with kpi3:
    st.markdown("""
    <div class="kpi-card" style="border-left-color: #27ae60;">
        <div class="kpi-title">💤 최소 권장 수면시간</div>
        <div class="kpi-value" style="color: #27ae60;">6.5 시간</div>
        <div class="kpi-sub">반응속도 260ms 이하 유지 필수 수면량</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# ==========================================
# 3. 사이드바 인터랙티브 시뮬레이터 & Rule-based Alert
# ==========================================
st.sidebar.header("🕹️ 선수 컨디션 시뮬레이터")
st.sidebar.markdown("수면 시간과 드링크 섭취량을 조절하여 **예상 반응속도**와 **심박수**를 실시간으로 확인하세요.")

sim_sleep = st.sidebar.slider(
    "💤 수면 시간 (Sleep Hours)",
    min_value=3.0,
    max_value=10.0,
    value=7.0,
    step=0.5,
    help="선수의 전날 수면 시간을 설정합니다."
)

sim_drink = st.sidebar.slider(
    "⚡ 에너지 드링크 (Energy Drinks)",
    min_value=0,
    max_value=6,
    value=1,
    step=1,
    help="일일 에너지 드링크 섭취량을 설정합니다."
)

# 예측 모델 계산식 (25만 건 회귀 및 ANOVA 실측치 반영)
# 베이스라인: 295.1 - 4.95 * 수면시간
# 드링크 효과: 0캔=0, 1캔=-2.0, 2캔=-3.9, 3캔=+1.9, 4캔=+0.1, 5캔=+3.2, 6캔=+6.5
drink_effects = {0: 0.0, 1: -1.99, 2: -3.93, 3: +1.89, 4: +0.09, 5: +3.20, 6: +6.50}
pred_reaction = 295.11 - 4.9546 * sim_sleep + drink_effects.get(sim_drink, sim_drink * 1.5)
pred_bpm = 80.05 + 4.35 * sim_drink

st.sidebar.markdown("---")
st.sidebar.subheader("📊 실시간 컨디션 예측 결과")

s_col1, s_col2 = st.sidebar.columns(2)
s_col1.metric("예상 반응속도", f"{pred_reaction:.1f} ms", delta=f"{260.0 - pred_reaction:+.1f} ms vs 목표(260ms)", delta_color="normal")
s_col2.metric("예상 심박수", f"{pred_bpm:.1f} BPM", delta=f"{pred_bpm - 80.0:+.1f} BPM vs 안정(80)", delta_color="inverse")

# Rule-based System 상태 판정 및 경고 메시지
st.sidebar.markdown("### 🔔 Rule-based 컨디션 판정")

if sim_sleep <= 4.0 or (sim_sleep < 6.0 and sim_drink >= 3):
    st.sidebar.error("""
    **🚨 [위험] 긴급 개입 필요 (출전 보류)**  
    - 심각한 수면 부족 및 각성 과다 상태입니다.  
    - 반응 속도가 275ms 이상으로 지연되며 손떨림이 발생할 수 있습니다.  
    - **조치**: 드링크 섭취 중단 및 즉시 45분 파워 낮잠을 권고합니다.
    """)
elif sim_drink >= 3:
    st.sidebar.warning("""
    **⚠️ [주의] 에너지 드링크 과섭취 (임계점 초과)**  
    - 3캔 이상 섭취로 반응 속도가 오히려 느려지는 역효과가 발생합니다.  
    - **조치**: 추가 드링크 섭취를 금지하고 수분을 공급하세요.
    """)
elif sim_sleep < 6.0:
    st.sidebar.warning("""
    **⚠️ [주의] 수면 부채 경고 (반응 지연)**  
    - 수면 시간이 6시간 미만으로 베이스라인 반응 속도가 약 12ms 지연됩니다.  
    - **조치**: 경기 전 집중 에임 웜업 시간을 2배 연장하세요.
    """)
elif sim_sleep >= 7.0 and (1 <= sim_drink <= 2):
    st.sidebar.success("""
    **🌟 [최적] 최고 기량 상태 (Peak Performance)**  
    - 충분한 수면과 최적의 카페인 각성 효과가 결합되어 가장 빠르고 민첩한 반응 속도를 보입니다.  
    - **조치**: 주요 경기 최우선 출전 권장!
    """)
else:
    st.sidebar.info("""
    **🟢 [양호] 정상 출전 가능**  
    - 표준적인 신체 상태이며 안정적인 플레이가 가능합니다.
    """)

# ==========================================
# 4. 시각화 차트 섹션 (3개 차트)
# ==========================================

# -------------------------------------------------------------
# [Chart 1] 에너지드링크 섭취량별 APM 및 반응속도 (이중 축 차트)
# -------------------------------------------------------------
st.subheader("1. ⚡ 에너지드링크 섭취량별 APM 및 반응속도 (이중 축 분석)")
st.caption("드링크가 증가할수록 APM은 계속 상승하지만, 반응 속도는 2캔 정점 이후 3캔부터 급격히 느려지는 역효과를 확인하세요.")

drink_stats = df.groupby('Energy_Drinks').agg(
    APM=('APM', 'mean'),
    Reaction=('Reaction_Time_ms', 'mean')
).reset_index()

fig1 = make_subplots(specs=[[{"secondary_y": True}]])

# 1차 축 (좌측): APM 막대
fig1.add_trace(
    go.Bar(
        x=[f"{d}캔" for d in drink_stats['Energy_Drinks']],
        y=drink_stats['APM'].round(1),
        name="평균 APM (분당 조작수)",
        marker=dict(color='rgba(52, 152, 219, 0.75)', line=dict(color='#2980b9', width=1.5)),
        text=drink_stats['APM'].round(1),
        textposition='outside',
        hovertemplate='%{x}<br>평균 APM: %{y:.1f}<extra></extra>'
    ),
    secondary_y=False
)

# 2차 축 (우측): Reaction_Time_ms 선
fig1.add_trace(
    go.Scatter(
        x=[f"{d}캔" for d in drink_stats['Energy_Drinks']],
        y=drink_stats['Reaction'].round(2),
        name="평균 반응 속도 (Reaction Time)",
        mode='lines+markers+text',
        marker=dict(size=10, color='#e74c3c'),
        line=dict(width=3, color='#e74c3c'),
        text=[f"{v:.2f} ms" for v in drink_stats['Reaction']],
        textposition='top center',
        hovertemplate='%{x}<br>반응 속도: %{y:.2f} ms<extra></extra>'
    ),
    secondary_y=True
)

# 3캔 임계점 강조 참조선
fig1.add_vline(x=2.5, line_width=2, line_dash="dash", line_color="#c0392b")
fig1.add_annotation(
    x=2.5, y=267, yref="y2",
    text="<b>⚠️ 3캔 과섭취 임계점 (반응속도 급감)</b>",
    showarrow=False,
    font=dict(color="#c0392b", size=11),
    bgcolor="#fdedec", bordercolor="#c0392b", borderwidth=1
)

fig1.update_layout(
    xaxis=dict(title="<b>에너지 드링크 섭취량</b>"),
    yaxis=dict(title="<b>평균 APM</b>", range=[160, 260], showgrid=True),
    yaxis2=dict(title="<b>평균 반응 속도 (ms, 낮을수록 우수)</b>", range=[257, 269], overlaying='y', side='right', showgrid=False),
    legend=dict(x=0.01, y=0.99, bgcolor='rgba(255,255,255,0.85)', bordercolor='gray', borderwidth=1),
    template='plotly_white',
    height=450,
    margin=dict(l=40, r=40, t=20, b=40)
)
st.plotly_chart(fig1, use_container_width=True)

st.write("")

# -------------------------------------------------------------
# [Chart 2 & Chart 3] 2-Column 레이아웃
# -------------------------------------------------------------
c2_col, c3_col = st.columns([1, 1])

# [Chart 2] 수면시간 vs 반응속도 회귀 추세선
with c2_col:
    st.subheader("2. 💤 수면시간 vs 반응속도 회귀 추세선")
    st.caption("수면이 1시간 감소할 때마다 반응 속도가 약 4.95 ms(수면 박탈 시 최대 +14.2 ms) 지연됩니다.")
    
    # 3,000건 표본 추출
    sample_df = df.sample(n=3000, random_state=42)
    
    fig2 = px.scatter(
        sample_df,
        x='Sleep_Hours',
        y='Reaction_Time_ms',
        trendline='ols',
        trendline_color_override='#e74c3c',
        opacity=0.25,
        color_discrete_sequence=['#34495e'],
        labels={'Sleep_Hours': '수면 시간 (시간)', 'Reaction_Time_ms': '반응 속도 (ms)'}
    )
    
    # 회귀식 주석
    fig2.add_annotation(
        x=8.5, y=300,
        text="<b>회귀식: y = 295.1 - 4.95x</b><br>(p < 0.001 ***, R² = 0.151)",
        showarrow=False,
        font=dict(size=11, color="#78281f"),
        bgcolor="#fcf3cf", bordercolor="#f39c12", borderwidth=1
    )
    
    fig2.update_layout(
        template='plotly_white',
        height=450,
        margin=dict(l=30, r=30, t=20, b=30),
        yaxis=dict(range=[200, 330])
    )
    st.plotly_chart(fig2, use_container_width=True)

# [Chart 3] [수면 구간 x 에너지드링크 섭취량] 반응속도 교차 히트맵
with c3_col:
    st.subheader("3. 🧩 [수면 구간 × 드링크] 반응속도 교차 히트맵")
    st.caption("수면 부족 상태(상단 행)에서는 드링크를 마셔도 반응 속도 저하를 회복하지 못합니다.")
    
    pivot_matrix = df.pivot_table(
        index='Sleep_Segment',
        columns='Energy_Drinks',
        values='Reaction_Time_ms',
        aggfunc='mean'
    )
    
    fig3 = px.imshow(
        pivot_matrix.round(2),
        text_auto=True,
        aspect="auto",
        color_continuous_scale="RdYlBu_r",  # 붉은색=느림(위험), 푸른색=빠름(최적)
        labels=dict(x="에너지 드링크 (캔)", y="수면 구간", color="반응속도 (ms)")
    )
    
    fig3.update_layout(
        template='plotly_white',
        height=450,
        margin=dict(l=30, r=30, t=20, b=30),
        coloraxis_colorbar=dict(title="반응속도(ms)")
    )
    st.plotly_chart(fig3, use_container_width=True)

# ==========================================
# 5. 하단 데이터 요약 테이블
# ==========================================
with st.expander("📋 데이터 세부 집계표 확인 (수면 구간 × 에너지 드링크)"):
    summary_table = df.groupby(['Sleep_Segment', 'Energy_Drinks'], observed=False).agg(
        선수수=('Reaction_Time_ms', 'count'),
        평균_반응속도=('Reaction_Time_ms', 'mean'),
        평균_심박수=('Heart_Rate_BPM', 'mean'),
        평균_APM=('APM', 'mean')
    ).round(2)
    st.dataframe(summary_table, use_container_width=True)
