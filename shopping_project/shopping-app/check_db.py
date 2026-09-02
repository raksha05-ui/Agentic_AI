from src.utils.database import get_connection
conn = get_connection()
print(conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall())
conn.close()