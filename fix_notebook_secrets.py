import json
import pathlib
import re

paths = [
    pathlib.Path(r"C:\Users\user\Desktop\agentic_ai\health_analysis\bloodHealth.ipynb"),
    pathlib.Path(r"C:\Users\user\Desktop\agentic_ai\rag_basics\rag.ipynb"),
]

for path in paths:
    nb = json.loads(path.read_text(encoding="utf-8"))
    changed = 0
    for cell in nb.get("cells", []):
        src = "".join(cell.get("source", []))
        new = src

        new = re.sub(
            r'os\.environ\s*\[\s*["\']GOOGLE_API_KEY["\']\s*\]\s*=\s*["\'][^"\']+["\']',
            'os.environ["GOOGLE_API_KEY"] = "[REDACTED]"',
            new,
        )
        new = re.sub(
            r'os\.environ\s*\[\s*["\']GROQ_API_KEY["\']\s*\]\s*=\s*["\'][^"\']+["\']',
            'os.environ["GROQ_API_KEY"] = "[REDACTED]"',
            new,
        )
        new = re.sub(
            r'(?i)(GOOGLE_API_KEY|GROQ_API_KEY)\s*=\s*["\'][^"\']+["\']',
            r'\1 = "[REDACTED]"',
            new,
        )

        if new != src:
            changed += 1
            cell["source"] = new.splitlines(keepends=True)

    if changed:
        path.write_text(json.dumps(nb, indent=1, ensure_ascii=False), encoding="utf-8")
        print(f"Updated {path.name} ({changed} cells)")
