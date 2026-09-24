from openai import OpenAI
from .config import settings
from .documents import extract_text
from .memory import MemoryStore
from .search import search_web


class PersonalAgent:
    def __init__(self):
        self.memory = MemoryStore(settings.database_path)
        self.client = OpenAI(api_key=settings.llm_api_key or "ollama", base_url=settings.llm_base_url)

    def ingest(self, path: str) -> str:
        text = extract_text(path).strip()
        if not text:
            return "I could not extract any text from that file."
        self.memory.remember(f"Document {path}: {text[:12000]}")
        return f"Stored the contents of {path} in long-term memory."

    def respond(self, user_message: str, use_web: bool = False) -> str:
        memories = self.memory.search(user_message)
        web_results = search_web(user_message) if use_web and settings.web_search_enabled else []
        context = "\n".join(f"- {item}" for item in memories) or "No relevant memories."
        web_context = "\n".join(f"- {r['title']}: {r['snippet']} ({r['url']})" for r in web_results) or "No web results requested."
        system = f"""You are {settings.agent_name}, a helpful personal AI assistant.\n\nRelevant long-term memory:\n{context}\n\nWeb context (may be empty):\n{web_context}\n\nBe clear and practical. Never claim to have sent messages, changed calendars, or completed external actions unless a verified tool reports success. Ask for confirmation before consequential actions."""
        history = self.memory.recent_messages()
        messages = [{"role": "system", "content": system}, *history, {"role": "user", "content": user_message}]
        response = self.client.chat.completions.create(model=settings.llm_model, messages=messages, temperature=0.3)
        answer = response.choices[0].message.content or "I could not generate a response."
        self.memory.add_message("user", user_message)
        self.memory.add_message("assistant", answer)
        return answer
