import os
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 1. 폰트 및 스타일 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 2. 데이터 불러오기 및 그룹 정의
csv_path = r"c:\Users\30nuy\OneDrive\바탕 화면\Practice\archive\esports_gaming_biometrics_250k.csv"
print("데이터 로딩 중...")
df = pd.read_csv(csv_path)

# 수면 구간 정의 (6시간 미만: 수면 부족, 6시간 이상: 수면 충분)
df['Sleep_Group'] = np.where(df['Sleep_Hours'] < 6, '수면 부족 (<6시간)', '수면 충분 (≥6시간)')

# 3. [수면 구간 x 에너지 드링크] 교차 테이블 산출
print("=" * 75)
print("1. [수면 구간 x 에너지 드링크 섭취량] 표본 수 교차 테이블")
print("=" * 75)
ct_counts = pd.crosstab(df['Sleep_Group'], df['Energy_Drinks'])
print(ct_counts)

print("\n" + "=" * 75)
print("2. [수면 구간 x 에너지 드링크] 반응 속도 (Reaction_Time_ms) 평균 ± 표준편차")
print("=" * 75)
pt_react_mean = df.pivot_table(index='Sleep_Group', columns='Energy_Drinks', values='Reaction_Time_ms', aggfunc='mean')
pt_react_std = df.pivot_table(index='Sleep_Group', columns='Energy_Drinks', values='Reaction_Time_ms', aggfunc='std')
react_table = pt_react_mean.round(2).astype(str) + " ± " + pt_react_std.round(2).astype(str)
print(react_table)

print("\n" + "=" * 75)
print("3. [수면 구간 x 에너지 드링크] 심박수 (Heart_Rate_BPM) 평균 ± 표준편차")
print("=" * 75)
pt_hr_mean = df.pivot_table(index='Sleep_Group', columns='Energy_Drinks', values='Heart_Rate_BPM', aggfunc='mean')
pt_hr_std = df.pivot_table(index='Sleep_Group', columns='Energy_Drinks', values='Heart_Rate_BPM', aggfunc='std')
hr_table = pt_hr_mean.round(2).astype(str) + " ± " + pt_hr_std.round(2).astype(str)
print(hr_table)

# 4. 2-Way ANOVA 계산 함수
def calculate_2way_anova(y_col):
    y = df[y_col].values
    N = len(y)
    
    d_sleep = pd.get_dummies(df['Sleep_Group'], drop_first=True, dtype=float).values
    d_energy = pd.get_dummies(df['Energy_Drinks'], drop_first=True, dtype=float).values
    d_inter = d_sleep * d_energy
    
    def fit_sse(X):
        X_mat = np.column_stack([np.ones(N), X]) if X.shape[1] > 0 else np.ones((N, 1))
        beta = np.linalg.lstsq(X_mat, y, rcond=None)[0]
        residuals = y - X_mat @ beta
        return np.sum(residuals**2)
    
    sse_0 = np.sum((y - np.mean(y))**2)
    sse_A = fit_sse(d_sleep)
    sse_B = fit_sse(d_energy)
    sse_add = fit_sse(np.column_stack([d_sleep, d_energy]))
    sse_full = fit_sse(np.column_stack([d_sleep, d_energy, d_inter]))
    
    df_A, df_B, df_AB = 1, 4, 4
    df_E = N - 10
    
    ss_A = sse_B - sse_add
    ss_B = sse_A - sse_add
    ss_AB = sse_add - sse_full
    ss_E = sse_full
    ss_total = sse_0
    
    ms_A = ss_A / df_A
    ms_B = ss_B / df_B
    ms_AB = ss_AB / df_AB
    ms_E = ss_E / df_E
    
    f_A = ms_A / ms_E
    f_B = ms_B / ms_E
    f_AB = ms_AB / ms_E
    
    # p-values (df2 is ~250k, Chi-square asymptotic)
    def p_val_df1(f):
        t = math.sqrt(f)
        return 2 * (1 - 0.5 * (1 + math.erf(t / math.sqrt(2))))
        
    def p_val_df4(f):
        x = 4 * f
        return math.exp(-x / 2) * (1 + x / 2)
        
    p_A = p_val_df1(f_A)
    p_B = p_val_df4(f_B)
    p_AB = p_val_df4(f_AB)
    
    anova_df = pd.DataFrame({
        'SS (제곱합)': [ss_A, ss_B, ss_AB, ss_E, ss_total],
        'df (자유도)': [df_A, df_B, df_AB, df_E, N - 1],
        'MS (평균제곱)': [ms_A, ms_B, ms_AB, ms_E, np.nan],
        'F-value': [f_A, f_B, f_AB, np.nan, np.nan],
        'p-value': [p_A, p_B, p_AB, np.nan, np.nan]
    }, index=['수면상태(A)', '에너지드링크(B)', '상호작용(A×B)', '잔차(Error)', '총합(Total)'])
    
    return anova_df

anova_react = calculate_2way_anova('Reaction_Time_ms')
anova_hr = calculate_2way_anova('Heart_Rate_BPM')

print("\n" + "=" * 75)
print("4. 반응 속도 (Reaction_Time_ms) 2-Way ANOVA 결과")
print("=" * 75)
print(anova_react.to_string())

print("\n" + "=" * 75)
print("5. 심박수 (Heart_Rate_BPM) 2-Way ANOVA 결과")
print("=" * 75)
print(anova_hr.to_string())

# 5. 시각화 (상호작용 플롯 2개 대시보드)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

drinks = sorted(df['Energy_Drinks'].unique())
colors = {'수면 부족 (<6시간)': '#e74c3c', '수면 충분 (≥6시간)': '#2980b9'}
markers = {'수면 부족 (<6시간)': 'o', '수면 충분 (≥6시간)': 's'}

# [왼쪽] 반응 속도 상호작용 플롯
for grp in ['수면 부족 (<6시간)', '수면 충분 (≥6시간)']:
    means = pt_react_mean.loc[grp, drinks].values
    ax1.plot(drinks, means, marker=markers[grp], color=colors[grp],
             linewidth=2.5, markersize=8, label=grp)
    for x, y in zip(drinks, means):
        ax1.annotate(f"{y:.1f}", (x, y), textcoords="offset points",
                     xytext=(0, 8 if grp.startswith('수면 부족') else -14),
                     ha='center', fontsize=9.5, fontweight='bold', color=colors[grp])

ax1.set_title("반응 속도 (Reaction_Time_ms) 상호작용 플롯\n[상호작용 F=0.29, p=0.883 (유의하지 않음: 완전 평행 효과)]",
              fontsize=12, fontweight='bold', pad=15)
ax1.set_xlabel("에너지 드링크 섭취량 (캔)", fontsize=11, fontweight='bold')
ax1.set_ylabel("평균 반응 속도 (ms, 낮을수록 우수)", fontsize=11, fontweight='bold')
ax1.set_xticks(drinks)
ax1.set_ylim(252, 277)
ax1.grid(True, linestyle=':', alpha=0.6)
ax1.legend(loc='lower right', frameon=True, fontsize=10.5)

# 주석 박스
ax1.text(0.04, 0.94, "두 그래프가 평행 유지:\n수면 상태와 무관하게 동일한 패턴\n(2캔까지 단축 -> 3캔에서 둔화)",
         transform=ax1.transAxes, fontsize=10, verticalalignment='top',
         bbox=dict(boxstyle='round,pad=0.4', facecolor='#fdedec', edgecolor='#e74c3c', lw=1.2))

# [오른쪽] 심박수 상호작용 플롯
for grp in ['수면 부족 (<6시간)', '수면 충분 (≥6시간)']:
    means = pt_hr_mean.loc[grp, drinks].values
    ax2.plot(drinks, means, marker=markers[grp], color=colors[grp],
             linewidth=2.5, markersize=8, linestyle='--' if grp.startswith('수면 충분') else '-',
             label=grp)
    for x, y in zip(drinks, means):
        ax2.annotate(f"{y:.1f}", (x, y), textcoords="offset points",
                     xytext=(0, 8 if grp.startswith('수면 부족') else -14),
                     ha='center', fontsize=9.5, fontweight='bold', color=colors[grp])

ax2.set_title("심박수 (Heart_Rate_BPM) 상호작용 플롯\n[상호작용 F=0.18, p=0.948 (유의하지 않음: 거의 완전 일치)]",
              fontsize=12, fontweight='bold', pad=15)
ax2.set_xlabel("에너지 드링크 섭취량 (캔)", fontsize=11, fontweight='bold')
ax2.set_ylabel("평균 심박수 (BPM)", fontsize=11, fontweight='bold')
ax2.set_xticks(drinks)
ax2.set_ylim(76, 102)
ax2.grid(True, linestyle=':', alpha=0.6)
ax2.legend(loc='lower right', frameon=True, fontsize=10.5)

ax2.text(0.04, 0.94, "두 선이 거의 완벽하게 겹침:\n수면 여부와 관계없이 에너지 드링크가\n심박수에 동일한 상승 효과를 줌",
         transform=ax2.transAxes, fontsize=10, verticalalignment='top',
         bbox=dict(boxstyle='round,pad=0.4', facecolor='#eafaf1', edgecolor='#27ae60', lw=1.2))

plt.tight_layout()

# 6. 이미지 저장
output_path = r"c:\Users\30nuy\OneDrive\바탕 화면\Practice\archive\sleep_energy_interaction_anova.png"
plt.savefig(output_path, dpi=300)
print(f"\n상호작용 시각화 차트 저장 완료: {output_path}")

# 7. 기본 뷰어로 열기
try:
    os.startfile(output_path)
    print("시스템 기본 뷰어로 차트를 열었습니다.")
except Exception as e:
    print(f"뷰어 열기 실패: {e}")
