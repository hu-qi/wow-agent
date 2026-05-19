"""Minimal LlamaIndex workflow ReActAgent example.

This example demonstrates the newer LlamaIndex workflow agent style as a
replacement path for older tutorial code such as:

    ReActAgent.from_tools(...).chat(...)

Before running this script, make sure you have a working `llm` implementation.
The `build_llm()` function below is intentionally left as a small adapter point
so learners can plug in the LLM used in the tutorial, such as OurLLM, Ollama, or
another LlamaIndex-compatible LLM.
"""

from __future__ import annotations

import asyncio
from typing import Any

from llama_index.core.agent.workflow.multi_agent_workflow import AgentWorkflow
from llama_index.core.agent.workflow.react_agent import ReActAgent
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.tools import FunctionTool


def multiply(a: float, b: float) -> float:
    """Multiply two numbers and return the product."""
    return a * b


def add(a: float, b: float) -> float:
    """Add two numbers and return the sum."""
    return a + b


def build_llm() -> Any:
    """Return a LlamaIndex-compatible LLM.

    Replace this function with the LLM initialization used in the tutorial.

    For example, after defining `OurLLM` in 第05课, you can return:

        return OurLLM(api_key=api_key, base_url=base_url, model_name=chat_model)

    Or, if you use a LlamaIndex integration such as Ollama, return that LLM
    object here.
    """
    raise NotImplementedError(
        "Please replace build_llm() with the LLM initialization from the tutorial."
    )


async def main() -> None:
    llm = build_llm()

    multiply_tool = FunctionTool.from_defaults(fn=multiply)
    add_tool = FunctionTool.from_defaults(fn=add)

    calculator_agent = ReActAgent(
        name="calculator",
        description="Performs basic arithmetic operations.",
        system_prompt="You are a calculator assistant. Use tools step by step.",
        tools=[multiply_tool, add_tool],
        llm=llm,
    )

    workflow = AgentWorkflow(
        agents=[calculator_agent],
        root_agent="calculator",
    )

    memory = ChatMemoryBuffer.from_defaults()
    handler = workflow.run(
        user_msg="20+（2*4）等于多少？使用工具计算每一步",
        memory=memory,
    )

    response = await handler
    print(response)


if __name__ == "__main__":
    asyncio.run(main())
