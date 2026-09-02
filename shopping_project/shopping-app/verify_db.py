from src.utils.database import get_connection

conn = get_connection()
tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;").fetchall()
print("Tables created:", tables)
for table in tables:
    cols = conn.execute(f"PRAGMA table_info({table[0]});").fetchall()
    print(f"  {table[0]}: {[c[1] for c in cols]}")
conn.close()
