"""学习助手：三项工具、SQLite 记忆、Trim 中间件和结构化输出。"""
import argparse
from datetime import date
from decimal import Decimal
import json
from pathlib import Path
from typing import Literal
from langchain.agents import create_agent
from langchain.agents.middleware import before_model
from langchain_core.messages import AIMessage, HumanMessage, trim_messages
from langchain_core.tools import tool
from langgraph.checkpoint.sqlite import SqliteSaver
from pydantic import BaseModel, Field
from llm import llm

ROOT = Path(__file__).resolve().parent
MEMORY_EVENTS = []


class BudgetInput(BaseModel):
    amounts: list[float] = Field(description="各笔非负费用，如 [12.5, 8, 20]")


@tool(args_schema=BudgetInput)
def sum_budget(amounts: list[float]) -> str:
    """精确求和多笔费用；需要计算总费用时使用。"""
    values = [Decimal(str(x)) for x in amounts]
    if any(not x.is_finite() or x < 0 for x in values):
        raise ValueError("费用必须为有限的非负数字")
    return str(sum(values, Decimal("0")).quantize(Decimal("0.01")))


@tool
def days_between(start_date: str, end_date: str) -> int:
    """计算两个 YYYY-MM-DD 日期之间的天数，截止日期当天记为0天。"""
    return (date.fromisoformat(end_date) - date.fromisoformat(start_date)).days


@tool
def lookup_topic(topic: str) -> str:
    """查询本地课程知识表，只支持 WSL、Git、Docker、LangChain 四个主题。"""
    knowledge = {
        "wsl": "WSL 在 Windows 上运行 Linux；Ubuntu 发行版提供 Linux 用户空间。",
        "git": "Git 工作区保存文件，add 放入暂存区，commit 保存本地快照，push 上传远程。",
        "docker": "镜像是模板，容器是运行实例，Volume 持久保存数据，Compose 编排多个服务。",
        "langchain": "LangChain 提供模型与工具接口；LangGraph 管理状态与执行；LangSmith 用于追踪评估。",
    }
    return knowledge.get(topic.strip().lower(), "知识表中没有此主题，请查询 WSL、Git、Docker 或 LangChain。")


class StudyReply(BaseModel):
    answer: str = Field(description="简洁中文回答，必须与实际工具返回值一致")
    action: Literal["chat", "calculation", "lookup", "plan"] = Field(description="回答类型")
    next_step: str = Field(description="下一步学习建议，没有建议时填无")


@before_model
def manage_history(state, runtime):
    """按消息条数保留最近完整交互，避免切断 tool_call 与 ToolMessage 配对。"""
    messages = state["messages"]
    trimmed = trim_messages(messages, max_tokens=14, token_counter=len,
                            strategy="last", start_on="human", end_on=("human", "tool"),
                            include_system=True, allow_partial=False)
    MEMORY_EVENTS.append({"before": len(messages), "sent_to_model": len(trimmed)})
    # llm_input_messages 只控制本次模型上下文，SQLite 保留完整状态用于审计。
    return {"llm_input_messages": trimmed}


SYSTEM_PROMPT = """你是课程学习助手，使用中文。
身份：帮助用户完成学习计划和课程概念理解。
约束：费用运算必须调用 sum_budget；日期差必须调用 days_between；
课程主题知识查询必须调用 lookup_topic。不要编造工具结果或未提供的用户信息。
上下文：根据当前会话记忆回答姓名、学号等信息；不知道时明确说不知道。
输出：用简洁的中文直接回答用户；工具调用结束后必须停止重复调用。
回答尽量简短，不展示思考过程。"""


def build_agent(checkpointer):
    return create_agent(model=llm, tools=[sum_budget, days_between, lookup_topic],
                        system_prompt=SYSTEM_PROMPT, middleware=[manage_history],
                        checkpointer=checkpointer)


def chat(agent, question, thread_id):
    config = {"configurable": {"thread_id": thread_id}, "recursion_limit": 20}
    print("USER:", question, flush=True)
    for mode, event in agent.stream({"messages": [HumanMessage(question)]}, config,
                                    stream_mode=["messages", "updates"]):
        if mode == "messages":
            chunk, meta = event
            if isinstance(chunk, AIMessage) and chunk.content:
                print(chunk.content, end="", flush=True)
        else:
            for node, data in event.items():
                if not isinstance(data, dict):
                    continue
                for message in data.get("messages", []):
                    if isinstance(message, AIMessage) and message.tool_calls:
                        print("\nTOOL_CALL:", json.dumps(message.tool_calls, ensure_ascii=False), flush=True)
                    elif message.type == "tool":
                        print("TOOL_RESULT:", message.name, message.content, flush=True)
    state = agent.get_state(config).values
    final_text = state["messages"][-1].content
    # 小模型先完成工具决策，再通过 Ollama 原生 JSON Schema 生成 Pydantic 输出。
    # 分开这两步可避免模型把业务工具参数与输出字段混在一起。
    reply = llm.with_structured_output(StudyReply, method="json_schema").invoke([
        HumanMessage("将下面的助手回答整理为结构化结果。保留原答案事实，action按内容选chat/calculation/lookup/plan，"
                     "next_step没有建议则写无。\n问题：" + question + "\n回答：" + str(final_text))])
    print("\nSTRUCTURED:", reply.model_dump_json() if reply else "missing", flush=True)
    print("MEMORY:", MEMORY_EVENTS[-1], flush=True)
    return reply


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--demo", action="store_true")
    parser.add_argument("--thread", default="sxh-demo-001")
    parser.add_argument("--question")
    args = parser.parse_args()
    with SqliteSaver.from_conn_string(str(ROOT / "checkpoints.sqlite")) as saver:
        saver.setup()
        agent = build_agent(saver)
        if args.demo:
            questions = [
                "你好，我叫孙晞皓，学号241820001，正在学习实验2到5。请记住。",
                "我叫什么名字，学号是多少？",
                "我买书花12.5元、笔记本8元、文具20元，请计算总费用。",
                "从2026-10-10到2026-10-13相差几天？",
                "请从课程知识表查询Docker的基本概念。",
                "请给我一个今天完成实验报告的三步计划。",
            ]
            replies = [chat(agent, q, args.thread) for q in questions]
            (ROOT / "demo_results.json").write_text(json.dumps(
                {"replies": [r.model_dump() if r else None for r in replies],
                 "memory_events": MEMORY_EVENTS}, ensure_ascii=False, indent=2), encoding="utf-8")
        elif args.question:
            chat(agent, args.question, args.thread)
        else:
            while True:
                question = input("你: ").strip()
                if question.lower() in {"exit", "quit", "q"}:
                    break
                if question:
                    chat(agent, question, args.thread)


if __name__ == "__main__":
    main()
