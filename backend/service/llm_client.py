# Production-safe LLM client wrapper (LangChain)
# Uses OpenAI-compatible endpoint (works with NVIDIA NIM gateways that expose OpenAI API format)
import os
from langchain_openai import ChatOpenAI

def get_llm(model: str | None = None, temperature: float = 0.2):
    api_key = "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"
    base_url = "https://integrate.api.nvidia.com/v1"  # set this to your NIM gateway if needed
    model = model or "moonshotai/kimi-k2-instruct"  # Use a valid NVIDIA model
    if not api_key:
        raise RuntimeError("Missing NIM_API_KEY/OPENAI_API_KEY")

    return ChatOpenAI(
        model=model,
        temperature=temperature,
        api_key=api_key,
        base_url=base_url  # if using NIM with OpenAI-compatible API
    )
