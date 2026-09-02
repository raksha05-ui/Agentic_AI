from pathlib import Path
import sqlite3


BASE_DIR = Path(__file__).resolve().parents[2]
DB_DIR = BASE_DIR / "data"
DB_PATH = DB_DIR / "store.db"
SCHEMA_PATH = BASE_DIR / "db" / "schema.sql"


def _init_db_at(path: Path, schema_path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    with open(schema_path, "r", encoding="utf-8") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()


def _resolve_db_path() -> Path:
    """Return a usable DB path. If `store.db` exists but is invalid, create `store_new.db` and return it."""
    DB_DIR.mkdir(parents=True, exist_ok=True)
    if not DB_PATH.exists():
        # create fresh DB from schema
        _init_db_at(DB_PATH, SCHEMA_PATH)
        return DB_PATH

    # If exists, test if it's a valid SQLite DB
    try:
        sqlite3.connect(DB_PATH).execute("PRAGMA schema_version;").close()
        return DB_PATH
    except sqlite3.DatabaseError:
        # fallback to alternate DB so app can run while user fixes the original
        alt = DB_DIR / "store_new.db"
        if not alt.exists():
            _init_db_at(alt, SCHEMA_PATH)
        return alt


def get_connection():
    path = _resolve_db_path()
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db_from_schema(schema_path: Path, out_path: Path = None):
    """Initialize a DB file at out_path (or default DB_PATH) using schema_path."""
    target = out_path or DB_PATH
    _init_db_at(target, schema_path)
    return target
import sqlite3

def connect_db(db_name='data/store.db'):
    conn = sqlite3.connect(db_name)
    return conn

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        FOREIGN KEY (product_id) REFERENCES products (product_id)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS reviews (
        review_id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
        rating INTEGER NOT NULL,
        comment TEXT,
        FOREIGN KEY (product_id) REFERENCES products (product_id)
    )
    ''')
    
    conn.commit()
    conn.close()