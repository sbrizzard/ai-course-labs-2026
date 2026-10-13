"""统一模型配置，不使用云 API 密钥。"""
import os
from langchain_ollama import ChatOllama

llm = ChatOllama(model=os.environ.get("OLLAMA_MODEL", "qwen3-lab"),
                 base_url=os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434"),
                 temperature=0, reasoning=False, num_ctx=16384,
                 num_predict=1024, keep_alive="10m",
                 client_kwargs={"trust_env": False},
                 async_client_kwargs={"trust_env": False})
