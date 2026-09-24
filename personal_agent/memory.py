import sqlite3
from datetime import datetime, timezone
from pathlib import Path


class MemoryStore:
    def __init__(self, path: str):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(path, check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("""CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL
        )""")
        self.connection.execute("""CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL
        )""")
        self.connection.commit()

    def remember(self, content: str) -> None:
        self.connection.execute("INSERT INTO memories(content, created_at) VALUES (?, ?)", (content, self._now()))
        self.connection.commit()

    def search(self, query: str, limit: int = 8) -> list[str]:
        terms = [term for term in query.split() if len(term) > 2]
        if not terms:
            return []
        where = " OR ".join("content LIKE ?" for _ in terms)
        rows = self.connection.execute(f"SELECT content FROM memories WHERE {where} ORDER BY id DESC LIMIT ?", [f"%{t}%" for t in terms] + [limit]).fetchall()
        return [row["content"] for row in rows]

    def add_message(self, role: str, content: str) -> None:
        self.connection.execute("INSERT INTO messages(role, content, created_at) VALUES (?, ?, ?)", (role, content, self._now()))
        self.connection.commit()

    def recent_messages(self, limit: int = 12) -> list[dict[str, str]]:
        rows = self.connection.execute("SELECT role, content FROM messages ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
        return [dict(row) for row in reversed(rows)]

    @staticmethod
    def _now() -> str:
        return datetime.now(timezone.utc).isoformat()
