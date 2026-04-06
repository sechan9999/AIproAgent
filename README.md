# AI Productivity Agent (Azure Foundry + Local Simulation)

본 프로젝트는 **Microsoft Azure AI Foundry Agent** 구조를 기반으로, 외부 데이터(DB/API) 연동과 CSV 데이터 기반 Python 데이터 분석(Code Interpreter)을 동시에 수행하는 다기능 에이전트(Multi-tool Agent)의 구현 예제 및 로컬 시뮬레이터입니다.

## 🌟 주요 기능 (Key Skills)

1. **Custom Function Skill**: 사용자의 질문에 맞춰 지정된 백엔드/DB 함수를 호출하여 텍스트형 메타데이터(예: 분기별 매출 요약)를 확보합니다.
2. **Code Interpreter Skill**: 업로드된 CSV 구조를 실시간으로 파악하고 내부적으로 파이썬(Pandas/Matplotlib)을 동작시켜 통계 처리 및 차트를 자동 생성합니다.
3. **Agentic Orchestration**: 단 한 번의 자연어 명령어만으로 AI가 도구의 우선순위와 사용 여부를 계획하여 결과물을 종합합니다.

## 📂 구조 (Files)

- `main.py`: 제공해주신 실제 **Azure AI SDK** 기반의 Agent 배포/실행 코드입니다.
- `app.py`: Azure 없이 로컬 **Streamlit** 환경에서 Agent의 데이터 채팅 UI와 시각화 과정을 데모로 보여줍니다. (추천)
- `local_simulation.py`: 순수 파이썬 터미널 환경에서 가짜 딜레이를 주어 에이전트의 구동 원리(사고 흐름)를 출력합니다.
- `sales_data.csv`: Code Interpreter 분석 테스트용 머신러닝/통계 가상 데이터입니다.
- `.env.sample`: 활용할 Azure Key 포맷을 저장한 샘플 파일입니다.

## 🚀 실행 가이드 (How to Run)

### 1. 로컬 UI 웹 대시보드 (추천)
API 키 없이 즉시 브라우저에서 생산성 에이전트 UI를 테스트합니다.
```bash
pip install streamlit pandas matplotlib
streamlit run app.py
```

### 2. 터미널 시뮬레이션
에이전트가 어떤 모듈을 부르고 어떻게 대답하는지 터미널 로고 형식으로 관찰합니다.
```bash
python local_simulation.py
```

### 3. 실제 Azure AI Foundry 연동
Azure Portal 환경이 세팅된 경우, `.env.sample`을 `.env`로 바꾸고 값을 채운 후 실행합니다.
```bash
pip install azure-ai-projects azure-identity python-dotenv
python main.py
```
