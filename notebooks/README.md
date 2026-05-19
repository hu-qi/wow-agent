# notebooks 运行说明

本目录存放 wow-agent 课程对应的 Jupyter Notebook。由于不同章节依赖的模型服务、SDK 版本和外部 API 不完全相同，建议在运行前先确认环境和密钥配置。

## 推荐运行环境

建议使用 Python 3.10 或 Python 3.11，并为项目创建独立虚拟环境：

```bash
python -m venv .venv
source .venv/bin/activate  # macOS / Linux
# .venv\Scripts\activate  # Windows PowerShell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

如果需要在 Jupyter 中运行：

```bash
pip install notebook ipykernel
python -m ipykernel install --user --name wow-agent --display-name "wow-agent"
```

然后在 Notebook 中选择 `wow-agent` kernel。

## 环境变量

建议在项目根目录创建 `.env` 文件，并按实际情况填写：

```bash
OPENAI_API_KEY=your_openai_key_here
# OPENAI_BASE_URL=https://your-compatible-endpoint/v1

ZISHU_API_KEY=your_zishu_key_here
# ZHIPU_API_KEY=your_zhipu_key_here
# BOCHA_API_KEY=your_bocha_key_here
```

不同章节使用的变量不同。运行前请先查看 notebook 中的 `os.getenv(...)` 调用，确认 `.env` 中已经配置对应密钥。

## LlamaIndex 章节注意事项

LlamaIndex 相关 notebook 对应第05课到第08课，可能涉及：

- `llama-index-core`
- `llama-index-llms-ollama`
- `llama-index-embeddings-ollama`
- `llama-index-vector-stores-faiss`
- `SQLAlchemy`
- `requests`

如果遇到 `ReActAgent` 没有 `.chat()` 方法、`from_tools` 不存在、异步调用报错，通常是 LlamaIndex 版本差异导致的。可以先参考：

```text
../docs/llamaindex-agent-api-compat.md
../docs/llamaindex-react-agent-workflow-minimal.md
../examples/llamaindex/
```

## Ollama 本地模型

部分 LlamaIndex 示例使用 Ollama。可以先拉取模型：

```bash
ollama pull qwen2.5:7b
```

确认服务可访问：

```bash
curl http://127.0.0.1:11434
```

如果返回类似 `Ollama is running`，说明服务正常。

如果 notebook 中使用的是局域网地址，例如：

```python
base_url="http://192.168.0.123:11434"
```

请替换为自己的实际地址。本机运行通常可以使用：

```python
base_url="http://127.0.0.1:11434"
```

## Jupyter 中的异步调用

新版 LlamaIndex workflow agent 可能需要 `await`：

```python
handler = workflow.run(user_msg="...")
response = await handler
```

在普通 `.py` 文件中可以使用：

```python
asyncio.run(main())
```

但在 Jupyter Notebook 中通常已经有事件循环，不建议直接调用 `asyncio.run(main())`。如果遇到：

```text
RuntimeError: asyncio.run() cannot be called from a running event loop
```

请改用：

```python
await main()
```

或者直接执行：

```python
response = await handler
print(response)
```

## 建议运行顺序

建议先运行依赖最少的 notebook，再运行依赖外部服务较多的 notebook：

1. OpenAI 基础章节 notebook
2. LlamaIndex 第05课基础 Agent notebook
3. LlamaIndex 第06课数据库 Agent notebook
4. LlamaIndex 第07课 RAG Agent notebook
5. LlamaIndex 第08课搜索引擎 Agent notebook
6. Zigent / MetaGPT 相关 notebook

搜索引擎 Agent 可能需要付费 API，例如 `BOCHA_API_KEY`。没有对应密钥时，可以先跳过该 notebook 或只阅读代码结构。

## 提交 notebook 修改前的建议

Notebook diff 通常较大，建议修改前先注意：

- 不要提交真实 API Key。
- 尽量不要提交过多运行输出。
- 如果只是修文档说明，优先改 Markdown 教程或本 README。
- 如果需要迁移代码，建议先在 `examples/` 中给出可运行脚本，再同步到 notebook。
- 每次 PR 尽量只处理一个 notebook 或一个主题，避免 review 成本过高。
