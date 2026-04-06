import time
import os
import csv

def get_sales_summary(period: str) -> str:
    """Mock Custom Skill (Function Tool)"""
    summaries = {
        "2025 Q1": "매출 1.2억, YoY +18%, Top 제품: Widget A",
        "2025 Q2": "매출 1.5억, YoY +25%, Top 제품: Widget B",
    }
    return summaries.get(period, "데이터가 없습니다.")

def simulate_agent():
    print("🤖 [User] 이 sales_data.csv 파일을 분석해서 2025 Q1 매출 요약을 해주고, 분기별/제품별 매출 바 차트를 만들어줘.")
    time.sleep(1.5)

    print("\n============================== [Agent 작동 과정 시뮬레이션] ==============================")
    print("⚙️ [Agent 사고 과정] 'get_sales_summary' 도구를 사용해야겠다...")
    time.sleep(1)
    
    summary = get_sales_summary("2025 Q1")
    print(f"✨ [도구 실행 결과 - Custom Skill]: {summary}")
    time.sleep(1.5)

    print("\n⚙️ [Agent 사고 과정] 이번에는 CSV 파일을 분석하기 위해 'Code Interpreter' 도구를 사용해야겠다...")
    time.sleep(1)
    
    print("💻 [Code Interpreter 실행 중]: Python 스크립트로 sales_data.csv 파싱 및 집계 중...")
    time.sleep(1)
    
    # 순수 Python으로 CSV 파싱 (Pandas/Matplotlib 미설치 환경도 고려하여 Ascii-Art 형태로 차트를 시뮬레이션)
    try:
        if not os.path.exists("sales_data.csv"):
            print("❌ sales_data.csv 파일을 찾을 수 없습니다.")
            return

        with open("sales_data.csv", "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            revenue_by_quarter = {"Q1": 0, "Q2": 0}
            
            for row in reader:
                rev = int(row["Revenue"])
                if "01" <= row["Date"].split("-")[1] <= "03":
                    revenue_by_quarter["Q1"] += rev
                else:
                    revenue_by_quarter["Q2"] += rev
                    
        print("\n📊 [Code Interpreter: 콘솔에 분석 내용 출력 완료]")
        print("   --- 2025년 분기별 매출 분석 ---")
        for q, rev in revenue_by_quarter.items():
            bar_length = int(rev / 10000)
            print(f"   {q} | {'█' * bar_length} ({rev:,} 원)")
            
    except Exception as e:
        print(f"⚠️ 읽기 오류 발생: {e}")
        
    time.sleep(1.5)
    print("========================================================================================\n")

    print("🤖 Agent 최종 응답:")
    print("요청하신 2025 Q1 매출 요약 데이터입니다.")
    print(f"👉 **{summary}**\n")
    print("또한 제가 Code Interpreter를 사용하여 sales_data.csv를 분석한 결과, 각 분기별로 매출을 집계하여 바 차트 형태로 렌더링했습니다. \n(위의 표 및 이미지 출력물 참조)")

if __name__ == "__main__":
    simulate_agent()
