import streamlit as st
import pandas as pd
import time
import os

st.set_page_config(page_title="AI Data Analyst PRO", layout="wide", page_icon="🪄")

# ================= 1. 모의 스킬(Skills) 정의 =================
def get_sales_summary(period: str) -> dict:
    """DB/API 호출 시뮬레이션 (Custom Skill)"""
    summaries = {
        "2025 Q1": {"revenue": "₩1.2억", "yoy": "+18%", "top_product": "Widget A"},
        "2025 Q2": {"revenue": "₩1.5억", "yoy": "+25%", "top_product": "Widget B"},
    }
    return summaries.get(period, {"revenue": "N/A", "yoy": "N/A", "top_product": "N/A"})

# ================= 2. 스타일링 및 메인 UI 로직 =================
# 프리미엄 룩을 위한 커스텀 스타일
st.markdown("""
<style>
.stMetric {
    background-color: #f7f9fc;
    border-radius: 10px;
    padding: 10px 20px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}
[data-testid="stSidebar"] {
    background-color: #f0f4f8;
}
</style>
""", unsafe_allow_html=True)

st.title("🪄 AI Productivity Agent PRO")
st.markdown("""
단순한 텍스트 챗봇이 아닙니다. **분석할 키워드를 섞어 명령**하면 AI가 **1) DB 요약 함수**와 **2) Code Interpreter(Pandas 실행)** 를 동적으로 호출 및 조합하여 실시간 대시보드를 구축하는 과정을 완전히 입체적으로 경험할 수 있습니다.
""")

# 좌측 사이드바: 샌드박스
with st.sidebar:
    st.header("📂 Data Sandbox")
    st.markdown("Code Interpreter가 접근 및 통제 가능한 클라우드 스토리지입니다.")
    uploaded_file = st.file_uploader("분석할 CSV 파일", type=["csv"])
    
    fallback_file = "sales_data.csv"
    active_data = None
    if uploaded_file is not None:
        df_preview = pd.read_csv(uploaded_file)
        st.success("새 데이터 준비 완료!")
        active_data = uploaded_file
    else:
        if os.path.exists(fallback_file):
            st.info("⚙️ 기본 데모 데이터 (sales_data.csv) 연동됨")
            df_preview = pd.read_csv(fallback_file)
            active_data = fallback_file
        else:
            df_preview = pd.DataFrame()
            
    if not df_preview.empty:
        with st.expander("데이터 열람하기 (Data Preview)", expanded=False):
            st.dataframe(df_preview, use_container_width=True)

# 모의 대화 내역 (메모리) 저장소
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "안녕하세요! 원하시는 분석 내용을 말씀해주세요.\n\n💡 **AI가 알아듣는 다이나믹 프롬프트 시도해보기:**\n- \"2025 Q1 매출 요약해주고, CSV 기반 **분기별** 차트 그려줘\"\n- \"이번 분기 정보 주고, **제품별** 판매량(Units_Sold) 좀 분석해봐\"\n- \"**카테고리별** 기준으로 매출을 비교해서 시각화해줘\""}
    ]

# 중앙 채팅 및 이전 대화 렌더링
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        # Custom Skill의 Metric 결과가 있다면 UI화
        if "metrics" in msg:
            st.markdown("###### 📊 기업 DB 조회 완료 (Custom Skill 결과)")
            cols = st.columns(3)
            cols[0].metric("25 Q1 매출 요약", msg["metrics"]["revenue"])
            cols[1].metric("YoY 증감율", msg["metrics"]["yoy"])
            cols[2].metric("Best 판매 제품", msg["metrics"]["top_product"])
        # Code Interpreter 소스코드가 있다면
        if "code" in msg:
            with st.expander("💻 Code Interpreter가 작성한 파이썬 소스코드 보기"):
                st.code(msg["code"], language="python")
        # 동적 생성 차트
        if "chart_data" in msg and msg["chart_data"] is not None:
            st.bar_chart(msg["chart_data"])

# 사용자 입력창
if prompt := st.chat_input("예: 카테고리별 판매량을 막대그래프로 그려줘"):
    # 1. 사용자 질문 출력
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. Agent 응답 체인 시작
    with st.chat_message("assistant"):
        with st.status("🧠 Agent가 도구를 선택하고 행동을 계획합니다...", expanded=True) as status:
            time.sleep(1)
            st.write("🔍 **의도 파악 완료:** 사내 메타데이터 조회(DB) + 샌드박스 데이터 분석(Python) 플로우 동시 가동")
            time.sleep(0.5)
            
            # (A) Function Skill 실행 모사
            st.write("🛠️ **Tool 1: `get_sales_summary()` 함수 호출**")
            summary_dict = get_sales_summary("2025 Q1")
            time.sleep(0.8)
            
            # (B) Code Interpreter 모사 - 키워드에 따른 동적 판단 (NLP)
            is_product = "제품" in prompt or "product" in prompt.lower()
            is_category = "카테고리" in prompt or "category" in prompt.lower()
            
            group_by_col = "Product" if is_product else "Category" if is_category else "Quarter"
            # 판매량 키워드가 있으면 Units_Sold로 전환
            val_col = "Units_Sold" if "판매량" in prompt or "수량" in prompt else "Revenue"
            
            st.write(f"💻 **Tool 2: Code Interpreter 실행 중...**")
            st.caption(f"↳ 프롬프트를 분석하여 `{group_by_col}` 기준으로 `{val_col}` 값을 그루핑하는 Python 로직 작성 중")
            time.sleep(1.2)
            
            # Python 생성 코드 시뮬레이션 공개
            gen_code = f"""import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('{active_data}')
df['Date'] = pd.to_datetime(df['Date'])
df['Quarter'] = df['Date'].dt.to_period('Q').dt.strftime('%Y Q%q')

# LLM이 작성한 집계 로직
chart_data = df.groupby('{group_by_col}')['{val_col}'].sum()
"""
            st.code(gen_code, language="python")

            chart_data = None
            if active_data is not None:
                st.write("▶️ **샌드박스에서 파이썬 코드 실행 완료 (Runtime: Python 3.10)**")
                time.sleep(1.0)
                try:
                    df = pd.read_csv(active_data)
                    df['Date'] = pd.to_datetime(df['Date'])
                    df['Quarter'] = df['Date'].dt.to_period('Q').dt.strftime('%Y Q%q')
                    chart_data = df.groupby(group_by_col)[val_col].sum()
                    st.caption("✅ 정상적으로 메모리에 차트 데이터가 적재되었습니다.")
                except Exception as e:
                    st.error(f"런타임 오류 발생: {e}")
            
            status.update(label="에이전트 모든 도구 실행 완료!", state="complete", expanded=False)

        # 3. 최종 완성 응답
        final_answer = "분석이 성공적으로 완료되었습니다! 두 개의 도구(Skill & Code Interpreter)를 조합한 다차원 리포트입니다."
        st.markdown(final_answer)
        
        # UI Metrics 컴포넌트 렌더링
        st.markdown("###### 📊 기업 DB 조회 완료 (Custom Skill 결과)")
        cols = st.columns(3)
        cols[0].metric("25 Q1 매출 요약", summary_dict["revenue"])
        cols[1].metric("YoY 증감율", summary_dict["yoy"])
        cols[2].metric("Best 판매 제품", summary_dict["top_product"])

        # 메모리에 저장할 메시지 형태 조립
        res_msg = {
            "role": "assistant", 
            "content": final_answer, 
            "metrics": summary_dict, 
            "code": gen_code
        }

        # UI 차트 렌더링
        if chart_data is not None:
            st.markdown(f"**📈 {group_by_col}별 {val_col} 자동 분석 차트**")
            st.bar_chart(chart_data)
            res_msg["chart_data"] = chart_data
            
        st.session_state.messages.append(res_msg)
        
        # 프리미엄 피드백용 Toast 알림
        st.toast('💡 AI 리포트 생성이 완료되었습니다!', icon='🚀')
