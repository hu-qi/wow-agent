# LlamaIndex workflow examples

本目录用于存放 LlamaIndex 新版 workflow agent API 的示例脚本，主要用于辅助迁移第05课到第08课中旧版 `ReActAgent.from_tools(...).chat(...)` 写法。

## 示例列表

| 脚本 | 对应教程 | 说明 |
| --- | --- | --- |
| `react_agent_workflow_minimal.py` | 第05课 | 基础工具 Agent 示例，包含 `add` 和 `multiply` 工具 |
| `database_agent_workflow.py` | 第06课 | SQLite / SQLAlchemy / `QueryEngineTool` 数据库 Agent 示例 |
| `rag_agent_workflow.py` | 第07课 | FAISS / RAG / `QueryEngineTool` Agent 示例 |
| `search_agent_workflow.py` | 第08课 | Bocha Web Search / `FunctionTool` 搜索 Agent 示例 |

## 环境变量

运行示例前，建议先从项目根目录复制 `.env.example`：

```bash
cp .env.example .env
```

Windows PowerShell 可以使用：

```powershell
Copy-Item .env.example .env
```

然后按需要填写模型服务和外部工具所需的变量，例如：

```bash
OLLAMA_BASE_URL=http://127.0.0.1:11434
OLLAMA_CHAT_MODEL=qwen2.5:7b
OLLAMA_EMBED_MODEL=qwen2.5:7b
BOCHA_API_KEY=your_bocha_api_key_here
```

不要提交真实 `.env` 或真实 API Key。

## 为什么脚本里保留 `build_llm()` / `build_embedding()`

这些脚本默认不硬编码具体模型服务，因为学习者可能使用：

- 教程中的 `OurLLM`
- Ollama
- OpenAI-compatible endpoint
- 其他 LlamaIndex 兼容 LLM / embedding provider

因此脚本保留了适配点：

```python
def build_llm():
    ...


def build_embedding():
    ...
```

运行前需要替换为实际模型配置。

## 使用 Ollama 进行本地验证

如果使用 Ollama，可以先安装并拉取模型：

```bash
ollama pull qwen2.5:7b
```

确认 Ollama 服务可访问：

```bash
curl http://127.0.0.1:11434
```

如果返回类似 `Ollama is running`，说明服务正常。

然后可以在脚本中把 `build_llm()` 替换成：

```python
from llama_index.llms.ollama import Ollama


def build_llm():
    return Ollama(
        base_url="http://127.0.0.1:11434",
        model="qwen2.5:7b",
    )
```

如果脚本还需要 embedding，把 `build_embedding()` 替换成：

```python
from llama_index.embeddings.ollama import OllamaEmbedding


def build_embedding():
    return OllamaEmbedding(
        base_url="http://127.0.0.1:11434",
        model_name="qwen2.5:7b",
    )
```

也可以在代码中读取 `.env` 中的 Ollama 配置：

```python
import os
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding


def build_llm():
    return Ollama(
        base_url=os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434"),
        model=os.getenv("OLLAMA_CHAT_MODEL", "qwen2.5:7b"),
    )


def build_embedding():
    return OllamaEmbedding(
        base_url=os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434"),
        model_name=os.getenv("OLLAMA_EMBED_MODEL", "qwen2.5:7b"),
    )
```

## 运行顺序建议

建议按复杂度从低到高验证：

```bash
python examples/llamaindex/react_agent_workflow_minimal.py
python examples/llamaindex/database_agent_workflow.py
python examples/llamaindex/rag_agent_workflow.py
python examples/llamaindex/search_agent_workflow.py
```

其中：

- `react_agent_workflow_minimal.py` 只需要 LLM。
- `database_agent_workflow.py` 需要 LLM、embedding、SQLite、SQLAlchemy。
- `rag_agent_workflow.py` 需要 LLM、embedding、FAISS，并且需要能读取 `docs/问答手册.txt`。
- `search_agent_workflow.py` 需要 LLM，并且需要 `.env` 中配置 `BOCHA_API_KEY`。

## Notebook 环境注意事项

如果把脚本代码复制到 Jupyter Notebook 中运行，通常不要使用：

```python
asyncio.run(main())
```

Notebook 通常已经有事件循环。可以改成：

```python
await main()
```

或者只执行：

```python
response = await handler
print(response)
```

如果看到：

```text
RuntimeError: asyncio.run() cannot be called from a running event loop
```

说明当前环境已经有事件循环，按 Notebook 写法调整即可。

## 常见问题

### 1. 找不到 `llama_index.llms.ollama`

请确认已经安装：

```bash
pip install llama-index-llms-ollama
```

### 2. 找不到 `llama_index.embeddings.ollama`

请确认已经安装：

```bash
pip install llama-index-embeddings-ollama
```

### 3. 找不到 `sqlalchemy`

请确认已经安装：

```bash
pip install SQLAlchemy
```

### 4. RAG 示例找不到 `docs/问答手册.txt`

请从仓库根目录运行脚本，或者修改 `rag_agent_workflow.py` 中的 `DEFAULT_INPUT_FILE`。

### 5. 搜索示例提示缺少 `BOCHA_API_KEY`

在项目根目录创建 `.env`，并写入：

```bash
BOCHA_API_KEY=your_api_key_here
```
