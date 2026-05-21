# LlamaIndex ReActAgent workflow 最小示例

本文档给出一个面向新版 LlamaIndex workflow agent API 的最小示例，用来替代旧教程中的 `ReActAgent.from_tools(...).chat(...)` 调用方式。

对应的可执行脚本骨架位于：

```text
examples/llamaindex/react_agent_workflow_minimal.py
```

脚本中保留了 `build_llm()` 适配点，使用时需要替换为第05课中的 `OurLLM`、Ollama 或其他 LlamaIndex 兼容 LLM 初始化方式。

## 使用前提

本示例默认你已经完成第05课前面的 LLM 初始化，并已经得到一个可用的 `llm` 对象，例如：

```python
llm = OurLLM(api_key=api_key, base_url=base_url, model_name=chat_model)
```

如果你使用 Ollama、OpenAI 或其他 LlamaIndex 支持的 LLM，也可以替换成对应的 `llm` 对象。

## 新版 workflow agent 写法

```python
import asyncio

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


async def main():
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
```

## 和旧版写法的对应关系

旧版教程中常见写法：

```python
agent = ReActAgent.from_tools([multiply_tool, add_tool], llm=llm, verbose=True)
response = agent.chat("20+（2*4）等于多少？使用工具计算每一步")
```

新版 workflow agent 写法将这两步拆成：

```python
calculator_agent = ReActAgent(
    name="calculator",
    description="Performs basic arithmetic operations.",
    tools=[multiply_tool, add_tool],
    llm=llm,
)

workflow = AgentWorkflow(
    agents=[calculator_agent],
    root_agent="calculator",
)

handler = workflow.run(user_msg="20+（2*4）等于多少？使用工具计算每一步")
response = await handler
```

## Notebook 中的写法

如果在 Jupyter Notebook 中运行，通常已经处于事件循环环境中，不建议再直接调用 `asyncio.run(main())`。可以改成：

```python
response = await handler
print(response)
```

如果遇到 `RuntimeError: asyncio.run() cannot be called from a running event loop`，说明当前环境已经有事件循环，按上面的 Notebook 写法执行即可。

## 后续迁移建议

- 第05课可以先保留旧版 `.chat()` 示例，再追加本示例作为新版 API 兼容方案。
- 第06课的数据库查询工具也可以按相同方式接入 `AgentWorkflow`。
- 第07课和第08课建议先确认 query engine / search tool 是否能单独运行，再接入 workflow agent。
