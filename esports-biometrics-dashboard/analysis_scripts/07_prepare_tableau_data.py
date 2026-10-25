import pandas as pd
import numpy as np

csv_path = r"c:\Users\30nuy\OneDrive\바탕 화면\Practice\archive\esports_gaming_biometrics_250k.csv"
df = pd.read_csv(csv_path)

# 1. 수면 구간 범주화
df['Sleep_Segment'] = pd.cut(
    df['Sleep_Hours'],
    bins=[-np.inf, 4, 6, 8, np.inf],
    labels=['4h 이하 (Critical)', '4~6h (Lack)', '6~8h (Normal)', '8h 이상 (Sufficient)']
)

# 2. 에너지 드링크 임계점 초과 여부 (3캔 이상 경고)
df['Energy_Drink_Alert'] = np.where(df['Energy_Drinks'] >= 3, '경고 (3캔 이상)', '정상 (2캔 이하)')

# 3. 종합 컨디션 알람 등급 (Alert Level)
def get_alert_level(row):
    # 위험: 3캔 이상 섭취 또는 반응속도 275ms 초과 또는 수면 4시간 이하
    if row['Energy_Drinks'] >= 3 or row['Reaction_Time_ms'] >= 275.0 or row['Sleep_Hours'] <= 4.0:
        return 'Critical (위험)'
    # 주의: 수면 6시간 미만 또는 심박수 92 BPM 초과
    elif row['Sleep_Hours'] < 6.0 or row['Heart_Rate_BPM'] >= 92.0:
        return 'Warning (주의)'
    # 최적: 수면 7시간 이상, 드링크 2캔 이하, 반응속도 260ms 이하
    elif row['Sleep_Hours'] >= 7.0 and row['Reaction_Time_ms'] <= 260.0 and row['Energy_Drinks'] <= 2:
        return 'Optimal (최적)'
    else:
        return 'Good (양호)'

df['Condition_Alert_Level'] = df.apply(get_alert_level, axis=1)

# 4. 알람 집계용 이진 플래그 (Tableau KPI 측정값용)
df['Is_Critical_Alert'] = (df['Condition_Alert_Level'] == 'Critical (위험)').astype(int)
df['Is_Warning_Alert'] = (df['Condition_Alert_Level'] == 'Warning (주의)').astype(int)
df['Is_Optimal'] = (df['Condition_Alert_Level'] == 'Optimal (최적)').astype(int)

output_csv = r"c:\Users\30nuy\OneDrive\바탕 화면\Practice\archive\esports_tableau_ready.csv"
df.to_csv(output_csv, index=False, encoding='utf-8-sig')
print("Saved cleanly to:", output_csv)
