import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 1. 한글 폰트 및 스타일 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 2. 데이터 불러오기
csv_path = r"c:\Users\30nuy\OneDrive\바탕 화면\Practice\archive\esports_gaming_biometrics_250k.csv"
print("데이터셋 로드 중...")
df = pd.read_csv(csv_path)

# 3. 에너지 드링크 섭취량별 통계 집계 (평균, 표준편차, 표본 수, 표준오차)
target_cols = ['Heart_Rate_BPM', 'APM', 'Reaction_Time_ms']
grouped = df.groupby('Energy_Drinks')[target_cols]

mean_df = grouped.mean()
std_df = grouped.std()
count_df = grouped.count()
sem_df = grouped.sem()  # 표준오차 (Standard Error of Mean)

print("=" * 60)
print("1. 에너지 드링크 섭취량별 평균 (Mean)")
print("=" * 60)
print(mean_df.round(2))

print("\n" + "=" * 60)
print("2. 에너지 드링크 섭취량별 표준편차 (Std)")
print("=" * 60)
print(std_df.round(2))

# 4. 임계점(꺾이는 지점) 수치 검증
diff_apm = mean_df['APM'].diff()
diff_react = mean_df['Reaction_Time_ms'].diff()

analysis_summary = pd.DataFrame({
    'Heart_Rate_BPM': mean_df['Heart_Rate_BPM'].round(2),
    'APM': mean_df['APM'].round(2),
    'APM_변화량': diff_apm.round(2),
    'Reaction_Time_ms': mean_df['Reaction_Time_ms'].round(2),
    '반응시간_변화량': diff_react.round(2)
})

print("\n" + "=" * 60)
print("3. 변화량 및 임계점 분석")
print("=" * 60)
print(analysis_summary)

# 최적 반응속도(최솟값) 및 임계점 탐색
best_intake = mean_df['Reaction_Time_ms'].idxmin()
threshold_intake = mean_df['Reaction_Time_ms'].diff().idxmax()
print(f"\n* 최적 반응 속도(가장 민첩한 지점): {best_intake}캔 ({mean_df.loc[best_intake, 'Reaction_Time_ms']:.2f} ms)")
print(f"* 반응 속도가 다시 느려지는 임계점: {threshold_intake}캔 (+{diff_react.loc[threshold_intake]:.2f} ms 증가)")

# 5. 시각화 (서브플롯 2개: 심박수 & APM vs 반응속도 임계점)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
drinks = mean_df.index.values

# [왼쪽 그래프] APM 및 심박수(Heart Rate) 추이 (계속 증가)
color_apm = '#2980b9'
color_hr = '#c0392b'

ax1_twin = ax1.twinx()
line1 = ax1.plot(drinks, mean_df['APM'], color=color_apm, marker='s', linewidth=2.5, markersize=8, label='APM (분당 조작수)')
line2 = ax1_twin.plot(drinks, mean_df['Heart_Rate_BPM'], color=color_hr, marker='^', linewidth=2.5, markersize=8, linestyle='--', label='심박수 (BPM)')

ax1.set_xlabel('에너지 드링크 섭취량 (캔)', fontsize=12, fontweight='bold')
ax1.set_ylabel('평균 APM (Actions Per Minute)', color=color_apm, fontsize=12, fontweight='bold')
ax1_twin.set_ylabel('평균 심박수 (BPM)', color=color_hr, fontsize=12, fontweight='bold')
ax1.set_xticks(drinks)
ax1.grid(True, linestyle=':', alpha=0.6)
ax1.set_title("에너지 드링크 섭취량별 APM 및 심박수 추이 (지속 상승)", fontsize=13, fontweight='bold', pad=15)

lines = line1 + line2
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc='upper left', frameon=True)

for x, y in zip(drinks, mean_df['APM']):
    ax1.annotate(f"{y:.1f}", (x, y), textcoords="offset points", xytext=(0, 8), ha='center', fontsize=10, fontweight='bold', color=color_apm)

for x, y in zip(drinks, mean_df['Heart_Rate_BPM']):
    ax1_twin.annotate(f"{y:.1f}", (x, y), textcoords="offset points", xytext=(0, -15), ha='center', fontsize=10, fontweight='bold', color=color_hr)

# [오른쪽 그래프] 반응 속도 (Reaction_Time_ms) 및 임계점(꺾이는 지점)
color_react = '#8e44ad'
ax2.plot(drinks, mean_df['Reaction_Time_ms'], color=color_react, marker='o', linewidth=3, markersize=9)
ax2.set_xlabel('에너지 드링크 섭취량 (캔)', fontsize=12, fontweight='bold')
ax2.set_ylabel('평균 반응 속도 (Reaction Time, ms)', color=color_react, fontsize=12, fontweight='bold')
ax2.set_xticks(drinks)
ax2.set_ylim(258, 268)
ax2.grid(True, linestyle=':', alpha=0.6)
ax2.set_title("반응 속도 임계점 분석 (2캔 최적 -> 3캔부터 급격히 둔화)", fontsize=13, fontweight='bold', pad=15)

for x, y in zip(drinks, mean_df['Reaction_Time_ms']):
    ax2.annotate(f"{y:.2f} ms", (x, y), textcoords="offset points", xytext=(0, 10), ha='center', fontsize=10, fontweight='bold', color=color_react)

# 임계점 강조 표시
ax2.annotate(
    f'★ 최적점 (2캔)\n{mean_df.loc[2, "Reaction_Time_ms"]:.2f} ms',
    xy=(2, mean_df.loc[2, 'Reaction_Time_ms']),
    xytext=(1.2, 261.5),
    arrowprops=dict(facecolor='#27ae60', shrink=0.08, width=2, headwidth=8),
    fontsize=11, fontweight='bold', color='#1e8449',
    bbox=dict(boxstyle="round,pad=0.3", fc="#eafaf1", ec="#27ae60", lw=1.5)
)

ax2.annotate(
    f'▲ 임계점 (3캔: 급격히 둔화)\n+{diff_react.loc[3]:.2f} ms 악화',
    xy=(3, mean_df.loc[3, 'Reaction_Time_ms']),
    xytext=(2.7, 267.2),
    arrowprops=dict(facecolor='#c0392b', shrink=0.08, width=2, headwidth=8),
    fontsize=11, fontweight='bold', color='#922b21',
    bbox=dict(boxstyle="round,pad=0.3", fc="#fdedec", ec="#c0392b", lw=1.5)
)

plt.tight_layout()

# 6. 이미지 저장
output_path = r"c:\Users\30nuy\OneDrive\바탕 화면\Practice\archive\energy_drinks_threshold_analysis.png"
plt.savefig(output_path, dpi=300)
print(f"\n시각화 차트 저장 완료: {output_path}")

# 7. 기본 뷰어로 열기
try:
    os.startfile(output_path)
    print("시스템 기본 뷰어로 차트를 열었습니다.")
except Exception as e:
    print(f"뷰어 열기 실패: {e}")
