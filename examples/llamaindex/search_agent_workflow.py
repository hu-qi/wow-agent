"""Minimal LlamaIndex workflow search agent example.

This example adapts the search-engine agent idea from 第08课 to the newer
LlamaIndex workflow agent API.

It uses Bocha Web Search as the default search tool because the original lesson
already demonstrates that API. You can replace `bocha_web_search_tool` with any
other search function that returns a string.
"""

from __future__ import annotations

import asyncio
import os
from typing import Any

import requests
from dotenv import load_dotenv
from llama_index.core.agent.workflow.multi_agent_workflow import AgentWorkflow
from llama_index.core.agent.workflow.react_agent import ReActAgent
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.tools import FunctionTool


load_dotenv()


def build_llm() -> Any:
    """Return a LlamaIndex-compatible LLM.

    Replace this function with the LLM initialization used in the tutorial.

    For example, after defining `OurLLM` in 第08课, you can return:

        return OurLLM(api_key=api_key, base_url=base_url, model_name=chat_model)
    """
    raise NotImplementedError(
        "Please replace build_llm() with the LLM initialization from the tutorial."
    )


def bocha_web_search_tool(query: str, count: int = 8) -> str:
    """Search the web with Bocha Web Search API and return raw JSON text.

    Args:
        query: Search query.
        count: Number of search results to return.

    Returns:
        Search results as a string so the agent can read and summarize them.
    """
    api_key = os.getenv("BOCHA_API_KEY")
    if not api_key:
        raise RuntimeError(
            "BOCHA_API_KEY is not set. Add it to your .env file before running."
        )

    url = "https://api.bochaai.com/v1/web-search"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "query": query,
        "freshness": "noLimit",
        "summary": True,
        "count": count,
    }

    response = requests.post(url, headers=headers, json=payload, timeout=30)
    if response.status_code != 200:
        raise RuntimeError(
            f"Bocha API request failed: {response.status_code}, {response.text}"
        )

    return str(response.json())


async def main() -> None:
    llm = build_llm()
    search_tool = FunctionTool.from_defaults(fn=bocha_web_search_tool)

    search_agent = ReActAgent(
        name="search_agent",
        description="Searches the web and summarizes fresh information.",
        system_prompt="你是一个联网搜索助手。需要最新信息时先使用搜索工具，再根据搜索结果回答。",
        tools=[search_tool],
        llm=llm,
    )

    workflow = AgentWorkflow(
        agents=[search_agent],
        root_agent="search_agent",
    )

    memory = ChatMemoryBuffer.from_defaults()
    query = "阿里巴巴2024年的ESG报告主要讲了哪些内容？"
    handler = workflow.run(
        user_msg=f"请帮我搜索以下内容：{query}",
        memory=memory,
    )

    response = await handler
    print(response)


if __name__ == "__main__":
    asyncio.run(main())
