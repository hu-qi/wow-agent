"""Minimal LlamaIndex workflow database agent example.

This example adapts the database-agent idea from 第06课 to the newer
LlamaIndex workflow agent API.

It intentionally keeps the LLM and embedding setup as adapter functions so
learners can plug in the LLM/embedding configuration used in the tutorial, such
as Ollama or another LlamaIndex-compatible provider.
"""

from __future__ import annotations

import asyncio
import sqlite3
from pathlib import Path
from typing import Any

from llama_index.core import SQLDatabase, Settings
from llama_index.core.agent.workflow.multi_agent_workflow import AgentWorkflow
from llama_index.core.agent.workflow.react_agent import ReActAgent
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.query_engine import NLSQLTableQueryEngine
from llama_index.core.tools import FunctionTool, QueryEngineTool
from sqlalchemy import create_engine


DB_PATH = Path("llmdb.db")
TABLE_NAME = "section_stats"


def build_llm() -> Any:
    """Return a LlamaIndex-compatible LLM.

    Replace this function with the LLM initialization used in the tutorial.

    Example with Ollama:

        from llama_index.llms.ollama import Ollama
        return Ollama(base_url="http://127.0.0.1:11434", model="qwen2.5:7b")
    """
    raise NotImplementedError(
        "Please replace build_llm() with the LLM initialization from the tutorial."
    )


def build_embedding() -> Any:
    """Return a LlamaIndex-compatible embedding model.

    Replace this function with the embedding initialization used in the tutorial.

    Example with Ollama:

        from llama_index.embeddings.ollama import OllamaEmbedding
        return OllamaEmbedding(
            base_url="http://127.0.0.1:11434",
            model_name="qwen2.5:7b",
        )
    """
    raise NotImplementedError(
        "Please replace build_embedding() with the embedding initialization from the tutorial."
    )


def prepare_sqlite_database(db_path: Path = DB_PATH) -> None:
    """Create and populate the demo SQLite database."""
    con = sqlite3.connect(db_path)
    cursor = con.cursor()

    cursor.execute(f"DROP TABLE IF EXISTS {TABLE_NAME}")
    cursor.execute(
        f"""
        CREATE TABLE {TABLE_NAME} (
            部门 varchar(100) DEFAULT NULL,
            人数 int DEFAULT NULL
        );
        """
    )

    rows = [
        ("专利部", 22),
        ("商标部", 25),
    ]
    cursor.executemany(
        f"INSERT INTO {TABLE_NAME} (部门, 人数) VALUES (?, ?)",
        rows,
    )

    con.commit()
    cursor.close()
    con.close()


def add(a: float, b: float) -> float:
    """Add two numbers and return the sum."""
    return a + b


async def main() -> None:
    prepare_sqlite_database()

    llm = build_llm()
    embedding = build_embedding()
    Settings.llm = llm
    Settings.embed_model = embedding

    engine = create_engine(f"sqlite:///{DB_PATH}")
    sql_database = SQLDatabase(engine, include_tables=[TABLE_NAME])
    query_engine = NLSQLTableQueryEngine(
        sql_database=sql_database,
        tables=[TABLE_NAME],
        llm=Settings.llm,
    )

    add_tool = FunctionTool.from_defaults(fn=add)
    staff_tool = QueryEngineTool.from_defaults(
        query_engine=query_engine,
        name="section_staff",
        description="查询部门的人数。输入部门名称，返回该部门人数。",
    )

    database_agent = ReActAgent(
        name="database_agent",
        description="Answers questions about department staff counts.",
        system_prompt="你是一个数据库查询助手。需要时先查询数据库，再使用工具完成计算。",
        tools=[add_tool, staff_tool],
        llm=llm,
    )

    workflow = AgentWorkflow(
        agents=[database_agent],
        root_agent="database_agent",
    )

    memory = ChatMemoryBuffer.from_defaults()
    handler = workflow.run(
        user_msg="请从数据库表中获取`专利部`和`商标部`的人数，并将这两个部门的人数相加！",
        memory=memory,
    )

    response = await handler
    print(response)


if __name__ == "__main__":
    asyncio.run(main())
