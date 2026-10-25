import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ==========================================
# 1. 데이터 불러오기 및 통계 집계
# ==========================================
csv_path = r"c:\Users\30nuy\OneDrive\바탕 화면\Practice\archive\esports_gaming_biometrics_250k.csv"
print("데이터셋 로드 중...")
df = pd.read_csv(csv_path)

# 에너지 드링크별 APM 및 반응속도 평균/표준오차 계산
stats_df = df.groupby('Energy_Drinks').agg(
    APM_mean=('APM', 'mean'),
    APM_std=('APM', 'std'),
    Reaction_mean=('Reaction_Time_ms', 'mean'),
    Reaction_std=('Reaction_Time_ms', 'std')
).reset_index()

print("=== 집계 데이터 ===")
print(stats_df.round(2))

# ==========================================
# 2. Seaborn + Matplotlib 이중 축(Dual-Axis) 차트
# ==========================================
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

fig, ax1 = plt.subplots(figsize=(10, 6))

# (1) 좌측 Y축: APM 막대그래프 (Seaborn barplot)
color_bar = '#3498db'
sns.barplot(
    data=stats_df,
    x='Energy_Drinks',
    y='APM_mean',
    ax=ax1,
    color=color_bar,
    alpha=0.75,
    edgecolor='black',
    linewidth=1.2,
    label='평균 APM'
)

ax1.set_xlabel('에너지 드링크 섭취량 (캔)', fontsize=12, fontweight='bold', labelpad=10)
ax1.set_ylabel('평균 APM (Actions Per Minute)', color='#1f618d', fontsize=12, fontweight='bold')
ax1.tick_params(axis='y', labelcolor='#1f618d')
ax1.set_ylim(160, 260)
ax1.grid(axis='y', linestyle=':', alpha=0.5)

# 막대 상단에 수치 라벨 표기
for i, row in stats_df.iterrows():
    ax1.text(i, row['APM_mean'] + 2, f"{row['APM_mean']:.1f}",
             ha='center', va='bottom', fontsize=10, fontweight='bold', color='#154360')

# (2) 우측 Y축: Reaction_Time_ms 선그래프 (Seaborn lineplot via twinx)
ax2 = ax1.twinx()
color_line = '#e74c3c'
sns.lineplot(
    data=stats_df,
    x=range(len(stats_df)),
    y='Reaction_mean',
    ax=ax2,
    color=color_line,
    marker='o',
    markersize=9,
    linewidth=2.8,
    label='평균 반응 속도 (ms)'
)

ax2.set_ylabel('평균 반응 속도 (Reaction_Time_ms, 낮을수록 우수)', color='#922b21', fontsize=12, fontweight='bold')
ax2.tick_params(axis='y', labelcolor='#922b21')
ax2.set_ylim(258, 268)

# 선 포인트에 수치 라벨 표기 및 임계점 강조
for i, row in stats_df.iterrows():
    val = row['Reaction_mean']
    ax2.text(i, val + 0.4, f"{val:.2f} ms",
             ha='center', va='bottom', fontsize=10, fontweight='bold', color=color_line)

# 범례(Legend) 결합
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', frameon=True, fontsize=10.5)

plt.title('에너지 드링크 섭취량별 APM(막대) 및 반응 속도(선) 이중 축 차트', fontsize=14, fontweight='bold', pad=15)
plt.tight_layout()

# Seaborn 차트 저장 및 실행
seaborn_out = r"c:\Users\30nuy\OneDrive\바탕 화면\Practice\archive\dual_axis_seaborn.png"
plt.savefig(seaborn_out, dpi=300)
print(f"Seaborn 차트 저장 완료: {seaborn_out}")

try:
    os.startfile(seaborn_out)
    print("Seaborn 이미지 차트를 열었습니다.")
except Exception as e:
    print(f"이미지 열기 오류: {e}")

# ==========================================
# 3. Plotly 인터랙티브 이중 축(Dual-Axis) 차트
# ==========================================
fig_plotly = make_subplots(specs=[[{"secondary_y": True}]])

# (1) 1차 Y축: APM 막대그래프
fig_plotly.add_trace(
    go.Bar(
        x=stats_df['Energy_Drinks'].astype(str) + "캔",
        y=stats_df['APM_mean'].round(1),
        name="평균 APM (조작속도)",
        marker=dict(color='rgba(52, 152, 219, 0.75)', line=dict(color='#2980b9', width=1.5)),
        text=stats_df['APM_mean'].round(1),
        textposition='outside',
        hovertemplate='에너지 드링크: %{x}<br>평균 APM: %{y:.1f}<extra></extra>'
    ),
    secondary_y=False
)

# (2) 2차 Y축: 반응속도 선그래프
fig_plotly.add_trace(
    go.Scatter(
        x=stats_df['Energy_Drinks'].astype(str) + "캔",
        y=stats_df['Reaction_mean'].round(2),
        name="평균 반응 속도 (Reaction Time)",
        mode='lines+markers+text',
        marker=dict(size=10, color='#e74c3c'),
        line=dict(width=3, color='#e74c3c'),
        text=stats_df['Reaction_mean'].round(2).astype(str) + " ms",
        textposition='top center',
        hovertemplate='에너지 드링크: %{x}<br>평균 반응시간: %{y:.2f} ms<extra></extra>'
    ),
    secondary_y=True
)

# 레이아웃 및 축 스타일링
fig_plotly.update_layout(
    title=dict(
        text="<b>에너지 드링크 섭취량별 APM 및 반응 속도 이중 축(Dual-Axis) 분석</b>",
        font=dict(size=17, family="Malgun Gothic")
    ),
    xaxis=dict(title=dict(text="<b>에너지 드링크 섭취량</b>", font=dict(size=13))),
    yaxis=dict(
        title=dict(text="<b>평균 APM</b>", font=dict(size=13, color="#2980b9")),
        range=[150, 260],
        showgrid=True,
        gridcolor='lightgray'
    ),
    yaxis2=dict(
        title=dict(text="<b>평균 반응 속도 (ms, 낮을수록 우수)</b>", font=dict(size=13, color="#c0392b")),
        range=[256, 268],
        overlaying='y',
        side='right',
        showgrid=False
    ),
    legend=dict(x=0.02, y=0.98, bgcolor='rgba(255,255,255,0.85)', bordercolor='gray', borderwidth=1),
    template='plotly_white',
    width=950,
    height=600
)

plotly_out = r"c:\Users\30nuy\OneDrive\바탕 화면\Practice\archive\dual_axis_plotly.html"
fig_plotly.write_html(plotly_out)
print(f"Plotly 인터랙티브 HTML 차트 저장 완료: {plotly_out}")

try:
    os.startfile(plotly_out)
    print("Plotly 인터랙티브 HTML 차트를 기본 브라우저로 열었습니다.")
except Exception as e:
    print(f"HTML 열기 오류: {e}")
