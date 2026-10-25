# eSports Biometrics & Cognitive Performance Dashboard

> 25만 건의 프로게이머 생체 지표(Biometrics) 데이터를 활용한 수면 및 카페인 섭취 기반 인지 능 분석 및 실시간 컨디셔닝 대시보드 프로젝트

---

## 1. 프로젝트 개요 (Project Overview)
- 배경: 이스포츠 선수단 및 프로게이머의 수면 부족과 과도한 에너지드링크(카페인) 섭취는 심박수 증가 및 인지 반응 속도 저하를 유발합니다.
- 목적: 25만 건의 실공학 생체 데이터셋을 바탕으로 통계적 임계점(Threshold)을 검증하고, 코칭스태프가 선수 컨디션을 실시간 모니터링 및 시뮬레이션할 수 있는 웹 대시보드를 구축합니다.
- 주요 기능:
  - 수면 시간 및 에너지드링크 섭취량 조절에 따른 실시간 반응속도/심박수 예측 시뮬레이터
  - Rule-based 경고 알림 시스템 (GREEN / AMBER / RED)
  - 이중 축(Dual-axis) APM 및 반응속도 분석 차트
  - 수면 부채(Sleep Debt) 선형 회귀 분석 및 2-Way ANOVA 히트맵 표출

---

## 2. 핵심 분석 인사이트 (Key Insights)
1. 수면 1시간당 반응속도 손실: 수면 시간이 1시간 감소할 때마다 Reaction Time이 평균 **+14.2ms 지연** ($p < 0.001$).
2. 에너지드링크 꺾이는 임계점 (U자형 곡선): 
   - 1~2캔 섭취 시: APM 상승 및 반응속도 개선 효과.
   - 3캔 이상 섭취 시: 심박수(BPM) 과다 상승 및 반응속도 다시 저하 (+18ms 손실).
3. 수면 x 카페인 교차 효과 (2-Way ANOVA): 
   - 수면이 5시간 미만인 상태에서 3캔 이상의 에너지드링크를 마실 경우 인지 저하 위험 폭증.

---

## 3. 기술 스택 (Tech Stack)
- Language: Python 3.10+
- Data Analysis & Stat: Pandas, NumPy, SciPy, Statsmodels
- Visualization & Web App: Streamlit, Seaborn, Matplotlib, Plotly

---

## 4. 실행 방법 (How to Run)

1. 저장소 클론 (Clone)
```bash
git clone https://github.com/your-username/esports-biometrics-dashboard.git
cd esports-biometrics-dashboard
```

2. 필수 패키지 설치 (Requirements)
```bash
pip install -r requirements.txt
```

3. Streamlit 앱 실행
```bash
streamlit run app.py
```