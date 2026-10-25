import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# 1. 한글 폰트 및 스타일 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 2. 데이터 불러오기
csv_path = r"c:\Users\30nuy\OneDrive\바탕 화면\Practice\archive\esports_gaming_biometrics_250k.csv"
print("25만 건 데이터 로딩 중...")
df = pd.read_csv(csv_path)

x = df['Sleep_Hours'].values
y = df['Reaction_Time_ms'].values

# 선형 회귀 추세선 계산 (y = mx + b)
slope, intercept = np.polyfit(x, y, 1)
x_line = np.linspace(x.min(), x.max(), 100)
y_line = slope * x_line + intercept

print(f"추세선 식: Reaction_Time_ms = {intercept:.2f} {slope:+.2f} * Sleep_Hours")

# 3. 1행 3열 종합 밀도 시각화 대시보드 생성
fig, axes = plt.subplots(1, 3, figsize=(18, 6))
fig.suptitle("수면 시간(Sleep_Hours) vs 반응 속도(Reaction_Time_ms) 밀도 및 추세 분석 (N=250,000)",
             fontsize=16, fontweight='bold', y=0.98)

# -------------------------------------------------------------
# [패널 1] 산점도 (Scatter Plot) + 추세선 (Regression Line)
# -------------------------------------------------------------
ax1 = axes[0]
# 25만 개 전체를 얇은 투명도로 표현 (오버플로팅 완화)
sample_df = df.sample(n=10000, random_state=42)
ax1.scatter(sample_df['Sleep_Hours'], sample_df['Reaction_Time_ms'],
            alpha=0.18, color='#2980b9', s=12, edgecolors='none', label='표본 관측치 (10,000건)')
ax1.plot(x_line, y_line, color='#c0392b', linewidth=2.8, linestyle='-',
         label=f'추세선 (y = {intercept:.1f} {slope:.2f}x)')

ax1.set_title("1. 산점도 (Scatter Plot) & 회귀 추세선", fontsize=13, fontweight='bold', pad=12)
ax1.set_xlabel("수면 시간 (시간)", fontsize=11, fontweight='bold')
ax1.set_ylabel("반응 속도 (ms, 낮을수록 우수)", fontsize=11, fontweight='bold')
ax1.set_xlim(1.5, 12.5)
ax1.set_ylim(190, 340)
ax1.grid(True, linestyle=':', alpha=0.5)
ax1.legend(loc='upper right', frameon=True)

# -------------------------------------------------------------
# [패널 2] 2D Hexbin 밀도 히트맵 (Hexagonal Binning)
# -------------------------------------------------------------
ax2 = axes[1]
hb = ax2.hexbin(x, y, gridsize=40, cmap='YlOrRd', mincnt=1, bins='log')
cb = fig.colorbar(hb, ax=ax2, shrink=0.82, pad=0.03)
cb.set_label('밀집 빈도 (log10 scale)', rotation=-90, va='bottom', fontsize=10, fontweight='bold')

# 추세선 덧그리기
ax2.plot(x_line, y_line, color='#2c3e50', linewidth=2.5, linestyle='--', label='회귀 추세선')

ax2.set_title("2. 2D Hexbin 밀도 히트맵 (전체 25만 건)", fontsize=13, fontweight='bold', pad=12)
ax2.set_xlabel("수면 시간 (시간)", fontsize=11, fontweight='bold')
ax2.set_ylabel("반응 속도 (ms)", fontsize=11, fontweight='bold')
ax2.set_xlim(1.5, 12.5)
ax2.set_ylim(190, 340)
ax2.legend(loc='upper right', frameon=True)

# -------------------------------------------------------------
# [패널 3] 2D KDE 밀도 등고선 히트맵 (Kernel Density Estimation)
# -------------------------------------------------------------
ax3 = axes[2]
kde_sample = df.sample(n=15000, random_state=42)
sns.kdeplot(
    data=kde_sample,
    x='Sleep_Hours',
    y='Reaction_Time_ms',
    ax=ax3,
    cmap='mako',
    fill=True,
    thresh=0.02,
    levels=15,
    alpha=0.85
)
ax3.plot(x_line, y_line, color='#e74c3c', linewidth=2.5, linestyle='-', label='회귀 추세선')

# 밀집 핫스팟(중심점) 표시
ax3.scatter([7.0], [260.0], color='red', s=60, marker='+', linewidths=2.5, label='밀집 중심점 (~7h, 260ms)')

ax3.set_title("3. 2D KDE 연속 확률 밀도 히트맵", fontsize=13, fontweight='bold', pad=12)
ax3.set_xlabel("수면 시간 (시간)", fontsize=11, fontweight='bold')
ax3.set_ylabel("반응 속도 (ms)", fontsize=11, fontweight='bold')
ax3.set_xlim(1.5, 12.5)
ax3.set_ylim(190, 340)
ax3.grid(True, linestyle=':', alpha=0.3, color='white')
ax3.legend(loc='upper right', frameon=True)

plt.tight_layout()

# 4. 이미지 저장 및 실행
output_path = r"c:\Users\30nuy\OneDrive\바탕 화면\Practice\archive\sleep_reaction_density_plots.png"
plt.savefig(output_path, dpi=300)
print(f"밀도 시각화 차트 저장 완료: {output_path}")

try:
    os.startfile(output_path)
    print("시스템 기본 뷰어로 차트를 열었습니다.")
except Exception as e:
    print(f"뷰어 열기 오류: {e}")
