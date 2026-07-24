import sqlite3
import time
from typing import Optional

class History:
    """
    History logs every action taken in the graph.
    It records "What happened".
    """
    def __init__(self, db_path: str = "icg_memory.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._init_db()

    def _init_db(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS execution_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contract_id TEXT,
                capability TEXT,
                node TEXT,
                status TEXT,
                error TEXT,
                cost REAL DEFAULT 0.0,
                tokens INTEGER DEFAULT 0,
                start_time REAL,
                end_time REAL
            )
        ''')
        self.conn.commit()

    def log_start(self, contract_id: str, capability: str, node: str) -> int:
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO execution_history (contract_id, capability, node, status, start_time) VALUES (?, ?, ?, ?, ?)",
            (contract_id, capability, node, "STARTED", time.time())
        )
        self.conn.commit()
        return cursor.lastrowid

    def log_success(self, record_id: int, cost: float = 0.0, tokens: int = 0):
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE execution_history SET status = ?, end_time = ?, cost = ?, tokens = ? WHERE id = ?",
            ("SUCCESS", time.time(), cost, tokens, record_id)
        )
        self.conn.commit()

    def log_failure(self, record_id: int, error: str):
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE execution_history SET status = ?, error = ?, end_time = ? WHERE id = ?",
            ("FAILED", error, time.time(), record_id)
        )
        self.conn.commit()
