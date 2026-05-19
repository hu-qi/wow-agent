"""Minimal LlamaIndex workflow RAG agent example.

This example adapts the RAG-as-a-tool idea from 第07课 to the newer
LlamaIndex workflow agent API.

It keeps the LLM and embedding setup as adapter functions so learners can plug
in the provider used in the tutorial, such as Ollama, OpenAI-compatible models,
or another LlamaIndex-compatible provider.
"""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Any, Iterable

import faiss
from llama_index.core import Document, Settings, StorageContext, VectorStoreIndex
from llama_index.core.agent.workflow.multi_agent_workflow import AgentWorkflow
from llama_index.core.agent.workflow.react_agent import ReActAgent
from llama_index.core.ingestion.pipeline import run_transformations
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.response_synthesizers import get_response_synthesizer
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.vector_stores.faiss import FaissVectorStore


DEFAULT_INPUT_FILE = Path("docs/问答手册.txt")


def build_llm() -> Any:
    """Return a LlamaIndex-compatible LLM.

    Example with Ollama:

        from llama_index.llms.ollama import Ollama
        return Ollama(base_url="http://127.0.0.1:11434", model="qwen2.5:7b")
    """
    raise NotImplementedError(
        "Please replace build_llm() with the LLM initialization from the tutorial."
    )


def build_embedding() -> Any:
    """Return a LlamaIndex-compatible embedding model.

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


def load_documents(input_file: Path = DEFAULT_INPUT_FILE) -> list[Document]:
    """Load the RAG source file used by the tutorial.

    The original tutorial reads `../docs/问答手册.txt`. This script uses
    `docs/问答手册.txt` when executed from the repository root.
    """
    if not input_file.exists():
        raise FileNotFoundError(
            f"Cannot find {input_file}. Run this script from the repository root "
            "or update DEFAULT_INPUT_FILE."
        )

    return [Document(text=input_file.read_text(encoding="utf-8"))]


def build_rag_query_engine(
    documents: Iterable[Document],
    embedding: Any,
    llm: Any,
) -> RetrieverQueryEngine:
    """Build the RAG query engine from tutorial documents."""
    transformations = [SentenceSplitter(chunk_size=512)]
    nodes = run_transformations(list(documents), transformations=transformations)

    sample_embedding = embedding.get_text_embedding("你好呀呀")
    vector_store = FaissVectorStore(
        faiss_index=faiss.IndexFlatL2(len(sample_embedding))
    )
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    index = VectorStoreIndex(
        nodes=nodes,
        storage_context=storage_context,
        embed_model=embedding,
    )

    retriever = VectorIndexRetriever(
        index=index,
        similarity_top_k=5,
        dimensions=len(sample_embedding),
    )
    response_synthesizer = get_response_synthesizer(llm=llm, streaming=True)

    return RetrieverQueryEngine(
        retriever=retriever,
        response_synthesizer=response_synthesizer,
    )


async def main() -> None:
    llm = build_llm()
    embedding = build_embedding()
    Settings.llm = llm
    Settings.embed_model = embedding

    documents = load_documents()
    rag_query_engine = build_rag_query_engine(
        documents=documents,
        embedding=embedding,
        llm=llm,
    )

    rag_tool = QueryEngineTool(
        query_engine=rag_query_engine,
        metadata=ToolMetadata(
            name="rag_tool",
            description="用于在原文中检索相关信息并回答问题。",
        ),
    )

    rag_agent = ReActAgent(
        name="rag_agent",
        description="Answers questions by retrieving information from local documents.",
        system_prompt="你是一个 RAG 查询助手。需要时使用 rag_tool 从原文中检索信息。",
        tools=[rag_tool],
        llm=llm,
    )

    workflow = AgentWorkflow(
        agents=[rag_agent],
        root_agent="rag_agent",
    )

    memory = ChatMemoryBuffer.from_defaults()
    handler = workflow.run(
        user_msg="What are the applications of Agent AI systems ?",
        memory=memory,
    )

    response = await handler
    print(response)


if __name__ == "__main__":
    asyncio.run(main())
