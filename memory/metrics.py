import sqlite3

class Metrics:
    """
    Metrics calculates and stores "How successful it was".
    Used for Capability Routing (RL / Policy learning) later.
    """
    def __init__(self, db_path: str = "icg_memory.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._init_db()

    def _init_db(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS node_metrics (
                node TEXT,
                capability TEXT,
                attempts INTEGER DEFAULT 0,
                successes INTEGER DEFAULT 0,
                total_duration REAL DEFAULT 0.0,
                total_cost REAL DEFAULT 0.0,
                total_tokens INTEGER DEFAULT 0,
                PRIMARY KEY (node, capability)
            )
        ''')
        self.conn.commit()

    def update_metrics(self, node: str, capability: str, success: bool, duration: float, cost: float = 0.0, tokens: int = 0):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO node_metrics (node, capability, attempts, successes, total_duration, total_cost, total_tokens)
            VALUES (?, ?, 1, ?, ?, ?, ?)
            ON CONFLICT(node, capability) DO UPDATE SET
                attempts = attempts + 1,
                successes = successes + excluded.successes,
                total_duration = total_duration + excluded.total_duration,
                total_cost = total_cost + excluded.total_cost,
                total_tokens = total_tokens + excluded.total_tokens
        ''', (node, capability, 1 if success else 0, duration, cost, tokens))
        self.conn.commit()
