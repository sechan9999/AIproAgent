import os
import asyncio
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    CodeInterpreterTool,
    FunctionTool,
    ToolSet,
    AgentRun,
)

load_dotenv()

# ====================== 1. Custom Skill (Function Tool) 정의 ======================
# 예: 매출 요약 함수 (실제로는 DB나 API 호출로 확장 가능)
def get_sales_summary(period: str) -> str:
    """지정된 기간의 매출 요약을 반환합니다."""
    # 실제로는 Azure SQL / Databricks 호출로 대체
    summaries = {
        "2025 Q1": "매출 1.2억, YoY +18%, Top 제품: Widget A",
        "2025 Q2": "매출 1.5억, YoY +25%, Top 제품: Widget B",
    }
    return summaries.get(period, "데이터가 없습니다.")

# FunctionTool로 변환 (Agent가 호출할 수 있게)
sales_tool = FunctionTool(
    functions=[get_sales_summary],  # 여러 개 추가 가능
    description="매출 기간별 요약을 제공하는 도구"
)

# ====================== 2. Code Interpreter Skill ======================
code_interpreter = CodeInterpreterTool()  # Python 코드 자동 실행 + 파일 분석

# ====================== 3. ToolSet에 Skills 합치기 ======================
toolset = ToolSet()
toolset.add(code_interpreter)      # Skill 1
toolset.add(sales_tool)            # Skill 2 (Custom)

# ====================== 4. Agent 생성 ======================
async def main():
    credential = DefaultAzureCredential()
    project_client = AIProjectClient(
        endpoint=os.getenv("AZURE_FOUNDRY_ENDPOINT"),
        credential=credential
    )

    with project_client:
        # Agent 생성 (한 번만 하면 됨, ID 저장해서 재사용)
        agent = project_client.agents.create_agent(
            model=os.getenv("AZURE_FOUNDRY_MODEL_DEPLOYMENT_NAME"),
            name="Productivity-Agent",
            instructions="""너는 생산성 전문 AI 어시스턴트야.
            - 사용자가 CSV 파일을 주면 Code Interpreter로 분석하고 차트 만들어줘.
            - 매출 요약이 필요하면 sales_summary 도구를 사용해.
            - 항상 친절하고 정확하게 답변해.""",
            tools=toolset.definitions,          # Skills(도구) 연결
            tool_resources=toolset.resources,   # 파일 등 리소스
        )
        print(f"✅ Agent 생성 완료! ID: {agent.id}")

        # 파일 업로드 (Code Interpreter 전용)
        # sales_data.csv 첨부를 위해 파일을 업로드하고 thread_id 메시지에 연결합니다.
        try:
            print("🚀 sales_data.csv 파일 업로드를 시도합니다...")
            file = project_client.files.upload(file_path="sales_data.csv", purpose="agents")
            file_id = file.id
            print(f"✅ 파일 업로드 완료! File ID: {file_id}")
        except Exception as e:
            print(f"⚠️ 파일 업로드 실패: {e}")
            file_id = None

        # ====================== 5. Thread(대화) 만들고 실행 ======================
        thread = project_client.agents.create_thread()

        # 예시 질문: CSV 분석 + Custom Skill 동시 사용
        user_message = (
            "이 sales_data.csv 파일을 분석해서 "
            "2025 Q1 매출 요약을 해주고, "
            "분기별 매출 바 차트를 만들어줘."
        )

        # 메시지 생성 (파일이 정상 업로드 되었다면 첨부)
        message_kwargs = {
            "thread_id": thread.id,
            "role": "user",
            "content": user_message
        }
        
        # NOTE: azure-ai-projects 버전에 따라 file 첨부의 방식이 다를 수 있음
        # 아래는 일반적인 attachments 방식입니다.
        if file_id:
            message_kwargs["attachments"] = [
                {"file_id": file_id, "tools": [{"type": "code_interpreter"}]}
            ]

        try:
            project_client.agents.create_message(**message_kwargs)
        except Exception as e:
            print(f"⚠️ 메시지 전달 중 문제 발생: {e}")
            # fall back
            project_client.agents.create_message(thread_id=thread.id, role="user", content=user_message)

        # Agent 실행 (도구 자동 호출됨)
        run: AgentRun = project_client.agents.create_run(
            thread_id=thread.id,
            agent_id=agent.id
        )
        print("⏳ Agent가 생각중입니다... 분기별 매출 요약과 차트를 생성합니다.")

        # 결과 기다리기
        while run.status in ["queued", "in_progress", "requires_action"]:
            await asyncio.sleep(2)
            run = project_client.agents.get_run(thread_id=thread.id, run_id=run.id)

        if run.status == "completed":
            print("\n================================")
            messages = project_client.agents.list_messages(thread_id=thread.id)
            for msg in reversed(messages.data): # 시간순 정렬을 위해 거꾸로
                if msg.role == "assistant":
                    print("\n🤖 Agent 답변:")
                    # 텍스트 출력
                    for content_item in msg.content:
                        if hasattr(content_item, 'text'):
                            print(content_item.text.value)
                        elif hasattr(content_item, 'image_file'):
                            img_file_id = content_item.image_file.file_id
                            print(f"📊 [차트 생성 완료 - 파일 ID: {img_file_id}]")
                            # 로컬로 이미지 파일 다운로드
                            project_client.files.download(file_id=img_file_id, target_file_path=f"chart_{img_file_id}.png")
                            print(f"✅ 차트 다운로드 완료: chart_{img_file_id}.png")
            print("================================\n")
        else:
            print(f"❌ 에러 발생 (Status: {run.status}):", run.last_error)

if __name__ == "__main__":
    asyncio.run(main())
