import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 1. 폰트 및 시각화 기본 설정 (Windows 맑은 고딕)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 2. 데이터 불러오기
csv_path = r"c:\Users\30nuy\OneDrive\바탕 화면\Practice\archive\esports_gaming_biometrics_250k.csv"
print("데이터셋 로딩 중...")
df = pd.read_csv(csv_path)

# 3. 상관분석 대상 피처 준비
# 범주형 이진 피처 수치화 (승리 여부, 블루라이트 필터 사용 여부)
df['Match_Outcome_Win'] = (df['Match_Outcome'] == 'Win').astype(int)
df['Blue_Light_Filter_On'] = (df['Blue_Light_Filter'] == 'Yes').astype(int)

# 분석 대상 피처 정의
feature_cols = [
    'Age',
    'PlayTime_Hours',
    'Sleep_Hours',
    'Energy_Drinks',
    'Screen_Brightness',
    'Blue_Light_Filter_On',
    'APM',
    'Heart_Rate_BPM',
    'HRV_Score',
    'Reaction_Time_ms',
    'Match_Outcome_Win'
]

# 한글 라벨 매핑 (가독성 향상)
label_map = {
    'Age': '나이 (Age)',
    'PlayTime_Hours': '플레이시간 (PlayTime)',
    'Sleep_Hours': '수면시간 (Sleep)',
    'Energy_Drinks': '에너지드링크 (Energy)',
    'Screen_Brightness': '화면밝기 (Brightness)',
    'Blue_Light_Filter_On': '블루라이트필터 (Filter)',
    'APM': '분당행동수 (APM)',
    'Heart_Rate_BPM': '심박수 (BPM)',
    'HRV_Score': '심박변이도 (HRV)',
    'Reaction_Time_ms': '반응속도 (Reaction)',
    'Match_Outcome_Win': '경기승리 (Win)'
}

korean_labels = [label_map[col] for col in feature_cols]

# 4. 피어슨 상관계수 행렬 계산
corr_matrix = df[feature_cols].corr()

# 5. 히트맵 시각화 생성
fig, ax = plt.subplots(figsize=(12, 10))
im = ax.imshow(corr_matrix, cmap='coolwarm', vmin=-1.0, vmax=1.0)

# 컬러바 설정
cbar = ax.figure.colorbar(im, ax=ax, shrink=0.8, pad=0.03)
cbar.ax.set_ylabel("피어슨 상관계수 (Pearson Correlation)", rotation=-90, va="bottom", fontsize=11, fontweight='bold')

# 축 눈금 및 라벨 설정
n = len(feature_cols)
ax.set_xticks(np.arange(n))
ax.set_yticks(np.arange(n))
ax.set_xticklabels(korean_labels, rotation=40, ha="right", rotation_mode="anchor", fontsize=10.5, fontweight='bold')
ax.set_yticklabels(korean_labels, fontsize=10.5, fontweight='bold')

# 각 셀에 상관계수 수치 표시
for i in range(n):
    for j in range(n):
        val = corr_matrix.iloc[i, j]
        # 배경색 대비에 따른 텍스트 색상 결정
        text_color = "white" if abs(val) > 0.45 else "black"
        ax.text(j, i, f"{val:.2f}",
                ha="center", va="center",
                color=text_color, fontsize=10,
                fontweight='bold' if abs(val) >= 0.2 else 'normal')

ax.set_title("e스포츠 게이머 생체 지표 및 게임 환경 상관관계 히트맵 (250,000건)",
             fontsize=15, fontweight='bold', pad=20)

plt.tight_layout()

# 6. 이미지 저장
output_path = r"c:\Users\30nuy\OneDrive\바탕 화면\Practice\archive\esports_biometrics_heatmap.png"
plt.savefig(output_path, dpi=300)
print(f"히트맵 이미지 저장 완료: {output_path}")

# 7. 기본 뷰어로 열기
try:
    os.startfile(output_path)
    print("시스템 기본 뷰어로 이미지를 열었습니다.")
except Exception as e:
    print(f"뷰어 실행 실패: {e}")
