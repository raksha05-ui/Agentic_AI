from src.utils.database import get_connection

def main():
    conn = get_connection()
    rows = conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    print('tables:', rows)
    conn.close()

if __name__ == '__main__':
    main()
