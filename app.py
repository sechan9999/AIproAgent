import streamlit as st
import pandas as pd
import time
import os

st.set_page_config(page_title="AI Data Analyst", layout="wide", page_icon="🤖")

# ================= 1. 모의 스킬(Skills) 정의 =================
def get_sales_summary(period: str) -> str:
    """DB/API 호출 시뮬레이션 (Custom Skill)"""
    summaries = {
        "2025 Q1": "매출 1.2억, YoY +18%, Top 제품: Widget A",
        "2025 Q2": "매출 1.5억, YoY +25%, Top 제품: Widget B",
    }
    return summaries.get(period, "해당 기간의 요약 데이터가 없습니다.")

# ================= 2. 메인 UI 로직 =================
st.title("📈 AI Productivity Agent (Local Demo)")
st.markdown("Azure 없이 순수 **Streamlit**을 이용해 만든 로컬 데모 앱입니다. **Function Skill**과 **Code Interpreter**가 시각적으로 어떻게 연계되어 동작하는지 체감하실 수 있습니다.")

# 좌측 사이드바: 파일 업로드 공간 (샌드박스 역할)
with st.sidebar:
    st.header("📂 Data Sandbox")
    st.markdown("Agent의 **Code Interpreter**가 이공간의 파일에 접근합니다.")
    uploaded_file = st.file_uploader("분석할 CSV 파일", type=["csv"])
    
    fallback_file = "sales_data.csv"
    if uploaded_file is not None:
        df_preview = pd.read_csv(uploaded_file)
        st.success("데이터가 Agent 환경에 준비되었습니다.")
        st.dataframe(df_preview, use_container_width=True)
        active_data = uploaded_file
    else:
        # 데모용 기본 파일 사용
        if os.path.exists(fallback_file):
            st.info("파일이 없으면 데모 데이터(sales_data.csv)가 쓰입니다.")
            active_data = fallback_file
        else:
            active_data = None

# 모의 대화 내역 저장소
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "안녕하세요! 원하시는 분석 내용을 말씀해주시거나 CSV 파일을 올려주세요. \n\n**(예시: \"2025 Q1 매출 요약해주고, CSV 기반 분기별 차트를 그려줘\")**"}
    ]

# 중앙 채팅 출력
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "chart_data" in msg and msg["chart_data"] is not None:
            st.bar_chart(msg["chart_data"])

# 사용자 입력창
if prompt := st.chat_input("질문을 입력하세요..."):
    # 1. 사용자 입력 출력
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. Agent 응답 생성
    with st.chat_message("assistant"):
        # Agent의 Thinking 과정 시각화
        with st.status("🧠 Agent가 최적의 도구를 고민 중입니다...", expanded=True) as status:
            time.sleep(1)
            st.write("🔍 **Skill 판별:** 사용자의 질문에서 '매출 요약' 과 '차트' 의도 인식")
            time.sleep(1)
            
            # (A) Function Skill 실행
            st.write("🛠️ **Custom Skill 호출:** `get_sales_summary(period='2025 Q1')`")
            summary_result = get_sales_summary("2025 Q1")
            st.caption(f"↳ 결과 데이터 확보: {summary_result}")
            time.sleep(1)

            # (B) Code Interpreter 실행 모사
            chart_data = None
            if active_data is not None:
                st.write("💻 **Code Interpreter 실행:** 내부 환경에서 Python(pandas) 코드를 자동 작성 후 실행 중...")
                time.sleep(1.5)
                try:
                    df = pd.read_csv(active_data)
                    # 시계열 분기 변환 로직 적용(시뮬레이션)
                    df['Date'] = pd.to_datetime(df['Date'])
                    df['Quarter'] = df['Date'].dt.to_period('Q').dt.strftime('%Y Q%q')
                    
                    chart_data = df.groupby('Quarter')['Revenue'].sum()
                    st.caption("↳ 결과: 데이터 차트용 집계(`groupby`) 렌더링 완료")
                except Exception as e:
                    st.error(f"데이터 분석 오류: {e}")
            else:
                st.warning("분석할 CSV 파일이 환경에 존재하지 않아, 차트 생성은 생략합니다.")
                
            time.sleep(0.5)
            status.update(label="응답 생성 완료!", state="complete", expanded=False)

        # 3. 최종 결과물 조합
        final_answer = "분석이 완료되었습니다!\n\n"
        final_answer += f"**1. 2025 Q1 요약 (사내 DB 조회 Custom Skill 활용)**\n> {summary_result}\n\n"
        final_answer += "**2. 분기별 매출 동향 (Code Interpreter 활용)**\n아래는 업로드된 CSV 데이터를 Python으로 즉시 분석해 그려낸 차트입니다."
        
        st.markdown(final_answer)
        if chart_data is not None:
            st.bar_chart(chart_data)
            
        # 세션 상태 업데이트
        st.session_state.messages.append(
            {"role": "assistant", "content": final_answer, "chart_data": chart_data}
        )
