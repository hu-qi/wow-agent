# LlamaIndex Agent API 兼容说明

本文档用于记录 wow-agent 教程中 LlamaIndex Agent 示例的 API 兼容问题，尤其是旧版 `ReActAgent.from_tools(...).chat(...)` 与新版 workflow agent 写法之间的差异。

## 背景

教程中第05课、第06课使用了类似下面的写法：

```python
from llama_index.core.agent import ReActAgent
from llama_index.core.tools import FunctionTool

agent = ReActAgent.from_tools([multiply_tool, add_tool], llm=llm, verbose=True)
response = agent.chat("20+（2*4）等于多少？使用工具计算每一步")
```

如果当前安装的 LlamaIndex 版本中 `ReActAgent` 已经切换到 workflow agent 实现，可能会遇到：

- `ReActAgent` 没有 `.chat()` 方法
- `ReActAgent.from_tools` 不存在或行为变化
- Agent 执行需要异步 `await`
- 导入路径从 `llama_index.core.agent` 变成 `llama_index.core.agent.workflow`

## 新版 workflow agent 写法参考

在较新的 LlamaIndex workflow agent API 中，`ReActAgent` 可以直接构造，然后通过 `AgentWorkflow` 执行。

```python
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
```

如果在普通 `.py` 文件中运行，可以包一层 `asyncio.run`：

```python
import asyncio


async def main():
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

## 旧版与新版的主要差异

| 维度 | 旧版教程写法 | 新版 workflow 写法 |
| --- | --- | --- |
| 导入路径 | `llama_index.core.agent import ReActAgent` | `llama_index.core.agent.workflow.react_agent import ReActAgent` |
| Agent 创建 | `ReActAgent.from_tools(...)` | `ReActAgent(name=..., tools=..., llm=...)` |
| 执行入口 | `agent.chat(...)` | `workflow.run(user_msg=...)` |
| 同步 / 异步 | 同步调用 | 异步 handler，通常需要 `await` |
| 多 Agent 扩展 | 直接在单个 agent 上扩展 | 使用 `AgentWorkflow(agents=[...], root_agent=...)` 管理 |

## 后续修复建议

建议不要一次性替换所有 LlamaIndex 章节，而是按下面顺序逐步处理：

1. 第05课：先补一个 workflow agent 的最小可运行示例。
2. 第06课：把数据库查询工具接入 workflow agent。
3. 第07课：把 RAG query engine 封装成 tool 后接入 workflow agent。
4. 第08课：检查搜索引擎工具依赖和异步执行方式。
5. notebooks：最后再同步，因为 notebook diff 较大，不适合作为第一批 PR。

## 注意事项

- 如果教程希望保持旧版 LlamaIndex，请在 `requirements.txt` 中固定版本。
- 如果教程希望跟随新版 LlamaIndex，应逐步迁移到 workflow agent 写法。
- 不建议在同一个 PR 中同时做依赖升级、API 迁移和 notebook 输出清理。
