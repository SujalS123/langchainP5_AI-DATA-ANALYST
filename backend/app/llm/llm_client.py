from ..config import settings
from langchain_google_genai import ChatGoogleGenerativeAI
import os


class LLMClient:
    def __init__(self):
        provider = settings.LLM_PROVIDER.upper()
        self.provider = provider
        if provider == "GEMINI" and not settings.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is not set in environment variables.")
        if provider == "GEMINI":
            self._client = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=settings.GEMINI_API_KEY, temperature=0.0)
        elif provider == "OPENAI":
            # Assuming an OpenAI client would be initialized here if needed
            # For now, we'll keep it as ChatGoogleGenerativeAI for consistency with the original code's structure
            # This part would need to be properly implemented if OpenAI is truly intended to be used.
            self._client = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=settings.GEMINI_API_KEY, temperature=0.0) # Placeholder
        else:
            raise ValueError(f"Unsupported LLM_PROVIDER: {provider}")
        

    def chat(self, prompt: str, temperature: float = 0.0, max_tokens: int = 1024):
        if self.provider == "OPENAI":
            resp = self._client.ChatCompletion.create(
                model="gpt-4o-mini",  # adapt the model name
                messages=[{"role":"user","content":prompt}],
                temperature=temperature,
                max_tokens=max_tokens
            )
            return resp["choices"][0]["message"]["content"]
        elif self.provider == "GEMINI":
            from langchain_core.messages import HumanMessage
            message = HumanMessage(content=prompt)
            resp = self._client.invoke([message], temperature=temperature, max_tokens=max_tokens)
            return resp.content