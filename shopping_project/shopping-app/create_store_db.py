from pathlib import Path
import sqlite3
import argparse
import sys


def main(force: bool = False):
    base_dir = Path(__file__).resolve().parent
    db_dir = base_dir / "data"
    db_path = db_dir / "store.db"
    schema_path = base_dir / "db" / "schema.sql"

    db_dir.mkdir(parents=True, exist_ok=True)

    if not schema_path.exists():
        raise FileNotFoundError(f"Schema file not found: {schema_path}")

    if db_path.exists():
        if force:
            try:
                db_path.unlink()
            except PermissionError:
                print("Cannot remove existing database file because it is open in another program.")
                print("Please close any editor or program that has 'data/store.db' open, then re-run this script.")
                return 2
        else:
            # quick check: see if it is a valid SQLite DB
            try:
                sqlite3.connect(db_path).execute("PRAGMA schema_version;").close()
                print("Existing database detected and appears valid. Use --force to recreate.")
                return 0
            except sqlite3.DatabaseError:
                try:
                    db_path.unlink()
                except PermissionError:
                    print("Cannot remove existing database file because it is open in another program.")
                    print("Please close any editor or program that has 'data/store.db' open, then re-run this script.")
                    return 2

    conn = sqlite3.connect(db_path)
    with open(schema_path, "r", encoding="utf-8") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()

    print(f"Database created/initialized at: {db_path}")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true", help="Force recreate DB by deleting existing file")
    args = parser.parse_args()
    code = main(force=args.force)
    sys.exit(code)
