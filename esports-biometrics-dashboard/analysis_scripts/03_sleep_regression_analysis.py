import os
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 1. 폰트 및 스타일 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 2. 데이터 불러오기
csv_path = r"c:\Users\30nuy\OneDrive\바탕 화면\Practice\archive\esports_gaming_biometrics_250k.csv"
print("데이터셋 로드 중...")
df = pd.read_csv(csv_path)

# 3. 수면 시간 세그먼트 생성
bins = [-np.inf, 4, 6, 8, np.inf]
labels = ['4시간 이하', '4~6시간', '6~8시간', '8시간 이상']
df['Sleep_Segment'] = pd.cut(df['Sleep_Hours'], bins=bins, labels=labels)

# 세그먼트별 요약 통계
seg_summary = df.groupby('Sleep_Segment', observed=False).agg(
    표본수=('Reaction_Time_ms', 'count'),
    평균수면시간=('Sleep_Hours', 'mean'),
    수면시간_표준편차=('Sleep_Hours', 'std'),
    평균반응속도=('Reaction_Time_ms', 'mean'),
    반응속도_표준편차=('Reaction_Time_ms', 'std')
)

print("=" * 65)
print("1. 수면 시간 세그먼트별 요약 통계")
print("=" * 65)
print(seg_summary.round(2))

# 4. 단순 선형 회귀분석 (OLS)
x = df['Sleep_Hours'].values
y = df['Reaction_Time_ms'].values
n = len(x)

x_mean = np.mean(x)
y_mean = np.mean(y)

ss_xx = np.sum((x - x_mean)**2)
ss_yy = np.sum((y - y_mean)**2)
ss_xy = np.sum((x - x_mean) * (y - y_mean))

slope = ss_xy / ss_xx
intercept = y_mean - slope * x_mean

y_pred = intercept + slope * x
residuals = y - y_pred
sse = np.sum(residuals**2)
s_err = np.sqrt(sse / (n - 2))
se_slope = s_err / np.sqrt(ss_xx)
se_intercept = s_err * np.sqrt(1 / n + x_mean**2 / ss_xx)

t_slope = slope / se_slope
t_intercept = intercept / se_intercept

# p-value 계산 (Z 근사)
def z_pvalue(t):
    return 2 * (1 - 0.5 * (1 + math.erf(abs(t) / math.sqrt(2))))

p_slope = z_pvalue(t_slope)
r_squared = (ss_xy**2) / (ss_xx * ss_yy)
r_corr = np.corrcoef(x, y)[0, 1]

# 95% 신뢰구간 (기울기)
ci_lower = slope - 1.96 * se_slope
ci_upper = slope + 1.96 * se_slope

# 수면 1시간 감소 시 반응시간 증가량
slowdown_per_hour = -slope

print("\n" + "=" * 65)
print("2. 수면 시간 - 반응 속도 선형 회귀분석 결과")
print("=" * 65)
print(f"회귀 방정식: Reaction_Time_ms = {intercept:.4f} + ({slope:.4f}) * Sleep_Hours")
print(f"기울기 (Slope, β1): {slope:.4f} ms/시간 (표준오차: {se_slope:.6f})")
print(f"절편 (Intercept, β0): {intercept:.4f} ms (표준오차: {se_intercept:.6f})")
print(f"95% 신뢰구간: [{ci_lower:.4f}, {ci_upper:.4f}]")
print(f"결정계수 (R²): {r_squared:.4f} (설명력 약 {r_squared * 100:.2f}%)")
print(f"피어슨 상관계수 (r): {r_corr:.4f}")
print(f"t-통계량: {t_slope:.2f}")
print(f"p-value: {p_slope} (p < 0.001, 매우 유의미)")
print(f"\n=> 결론: 수면 시간이 1시간 줄어들 때마다 반응 시간은 평균 {slowdown_per_hour:.2f} ms 느려집니다.")

# 5. 시각화 생성 (1행 2열 대시보드)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# [왼쪽] 산점도 표본 + 회귀선
sample_df = df.sample(n=3000, random_state=42)
ax1.scatter(sample_df['Sleep_Hours'], sample_df['Reaction_Time_ms'],
            alpha=0.15, color='#34495e', s=12, label='표본 관측치 (3,000건 추출)')

x_line = np.linspace(df['Sleep_Hours'].min(), df['Sleep_Hours'].max(), 100)
y_line = intercept + slope * x_line
ax1.plot(x_line, y_line, color='#e74c3c', linewidth=3,
         label=f'회귀선: y = {intercept:.1f} - {slowdown_per_hour:.2f}x')

ax1.set_xlabel('수면 시간 (Sleep_Hours, 시간)', fontsize=12, fontweight='bold')
ax1.set_ylabel('반응 속도 (Reaction_Time_ms, 밀리초)', fontsize=12, fontweight='bold')
ax1.set_title('수면 시간 vs 반응 속도 회귀분석', fontsize=13, fontweight='bold', pad=15)
ax1.grid(True, linestyle=':', alpha=0.6)
ax1.legend(loc='upper right', frameon=True)

# 통계량 텍스트 박스
stats_text = (
    f"회귀식: Reaction = {intercept:.2f} - {slowdown_per_hour:.2f} × Sleep\n"
    f"기울기(β1): {slope:.4f} (p < 0.001 ***)\n"
    f"수면 1시간 감소 시: +{slowdown_per_hour:.2f} ms 지연\n"
    f"결정계수(R²): {r_squared:.4f} (r = {r_corr:.2f})"
)
ax1.text(0.04, 0.05, stats_text, transform=ax1.transAxes,
         fontsize=10.5, verticalalignment='bottom',
         bbox=dict(boxstyle='round,pad=0.5', facecolor='#fcf3cf', edgecolor='#f39c12', lw=1.5))

# [오른쪽] 세그먼트별 평균 반응속도 막대그래프
colors = ['#c0392b', '#e67e22', '#2980b9', '#27ae60']
seg_names = seg_summary.index.tolist()
means = seg_summary['평균반응속도'].values
stds = seg_summary['반응속도_표준편차'].values

bars = ax2.bar(seg_names, means, color=colors, width=0.55, edgecolor='black', alpha=0.85)
ax2.set_ylabel('평균 반응 속도 (ms, 낮을수록 우수)', fontsize=12, fontweight='bold')
ax2.set_title('수면 시간 세그먼트별 평균 반응 속도 비교', fontsize=13, fontweight='bold', pad=15)
ax2.set_ylim(235, 290)
ax2.grid(axis='y', linestyle=':', alpha=0.6)

for bar in bars:
    height = bar.get_height()
    ax2.annotate(f"{height:.2f} ms",
                 xy=(bar.get_x() + bar.get_width() / 2, height),
                 xytext=(0, 5), textcoords="offset points",
                 ha='center', va='bottom', fontsize=11, fontweight='bold')

# 구간별 지연 차이 화살표/텍스트
diff_seg = means[0] - means[-1]
ax2.text(0.5, 0.92, f"최저 수면군 대비 최고 수면군: {diff_seg:.2f} ms 빠름",
         transform=ax2.transAxes, ha='center', fontsize=11, fontweight='bold', color='#196f3d',
         bbox=dict(boxstyle='round,pad=0.4', facecolor='#eafaf1', edgecolor='#27ae60', lw=1.2))

plt.tight_layout()

# 6. 이미지 저장
output_path = r"c:\Users\30nuy\OneDrive\바탕 화면\Practice\archive\sleep_reaction_regression.png"
plt.savefig(output_path, dpi=300)
print(f"\n회귀분석 시각화 이미지 저장 완료: {output_path}")

# 7. 기본 뷰어로 열기
try:
    os.startfile(output_path)
    print("시스템 기본 뷰어로 이미지를 열었습니다.")
except Exception as e:
    print(f"뷰어 실행 실패: {e}")
