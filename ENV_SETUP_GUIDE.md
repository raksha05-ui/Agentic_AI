# Environment Variables & API Keys Setup Guide

## Overview
This project uses environment variables to securely manage sensitive information like API keys and secrets. **Never commit `.env` files to version control** — they are already excluded via `.gitignore`.

---

## Quick Start

### 1. Root Project (.env for main.py and general project)

Copy `.env.example` to `.env` and fill in your actual values:

```bash
cp .env.example .env
```

Edit `.env` with your credentials:
```
GOOGLE_API_KEY=your_actual_google_api_key
GROQ_API_KEY=your_actual_groq_api_key
GOOGLE_MODEL=gemini-2.0-flash
DEBUG=False
```

### 2. Shopping App (.env for shopping_project/shopping-app)

Copy `.env.example` to `.env` inside the shopping app directory:

```bash
cd shopping_project/shopping-app
cp .env.example .env
```

Edit `.env`:
```
GOOGLE_API_KEY=your_actual_google_api_key
GROQ_API_KEY=your_actual_groq_api_key
GOOGLE_MODEL=gemini-2.0-flash
SECRET_KEY=your_secure_secret_key_generated_with_secrets
DEBUG=False
DATABASE_URL=sqlite:///data/store.db
ALLOWED_HOSTS=localhost,127.0.0.1
```

---

## Getting API Keys

### Google Gemini API
1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click "Create API Key"
3. Copy the key and paste into `GOOGLE_API_KEY` in your `.env`

### Groq API (LLaMA models)
1. Go to [Groq Console](https://console.groq.com)
2. Sign up / Log in
3. Generate API key
4. Paste into `GROQ_API_KEY` in your `.env`

---

## Generating a Secure SECRET_KEY

For Django/Flask applications, generate a cryptographically secure key:

```bash
python -c "from secrets import token_urlsafe; print(token_urlsafe(32))"
```

Copy the output and set `SECRET_KEY` in your `.env` file.

---

## Environment Variable Reference

### Root Project (.env)
| Variable | Description | Example |
|----------|-------------|---------|
| `GOOGLE_API_KEY` | Google Gemini API key | `AIzaSy...` |
| `GROQ_API_KEY` | Groq API key for LLaMA models | `gsk_...` |
| `GOOGLE_MODEL` | Default Gemini model | `gemini-2.0-flash` |
| `DEBUG` | Debug mode (True/False) | `False` |
| `ENVIRONMENT` | Environment type | `development` or `production` |

### Shopping App (shopping_project/shopping-app/.env)
| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | SQLite database path | `sqlite:///data/store.db` |
| `SECRET_KEY` | Flask/Django secret key (REQUIRED) | Generated with secrets module |
| `DEBUG` | Debug mode | `False` |
| `GOOGLE_API_KEY` | Google API key (if using LLMs) | `AIzaSy...` |
| `GROQ_API_KEY` | Groq API key (if using LLMs) | `gsk_...` |
| `GOOGLE_MODEL` | Model to use | `gemini-2.0-flash` |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts | `localhost,127.0.0.1` |
| `EMAIL_HOST` | SMTP server | `smtp.gmail.com` |
| `EMAIL_PORT` | SMTP port | `587` |
| `EMAIL_USE_TLS` | Use TLS for email | `True` |
| `EMAIL_HOST_USER` | Email address | `your_email@gmail.com` |
| `EMAIL_HOST_PASSWORD` | Email password or app password | `xxxxx` |

---

## How It Works

### In Python Code
```python
import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# Access variables
api_key = os.getenv("GOOGLE_API_KEY")
secret = os.getenv("SECRET_KEY")

# With defaults
debug = os.getenv("DEBUG", "False").lower() == "true"
```

### In Settings Files
```python
# settings.py example
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY not set in environment")
```

---

## Security Best Practices

✅ **DO:**
- Store `.env` in your home directory for local development
- Use strong, unique SECRET_KEY values
- Rotate API keys periodically
- Use environment-specific `.env` files (.env.development, .env.production)
- Keep `.env` in `.gitignore` to prevent accidental commits

❌ **DON'T:**
- Commit `.env` files to version control
- Share `.env` files via email or chat
- Use the same keys for development and production
- Hardcode secrets in Python files
- Log or print sensitive values

---

## Verifying Your Setup

Run this to check if environment variables are loaded:

```python
import os
from dotenv import load_dotenv

load_dotenv()
print("GOOGLE_API_KEY:", "✓ Set" if os.getenv("GOOGLE_API_KEY") else "✗ Not Set")
print("SECRET_KEY:", "✓ Set" if os.getenv("SECRET_KEY") else "✗ Not Set")
```

---

## Troubleshooting

**"API key not found" error:**
- Check `.env` file exists in the correct directory
- Verify the environment variable name matches exactly (case-sensitive)
- Run `load_dotenv()` before accessing the variable

**"SECRET_KEY not set or uses default value" error:**
- Generate a new key: `python -c "from secrets import token_urlsafe; print(token_urlsafe(32))"`
- Add to `.env`: `SECRET_KEY=your_generated_key`

**Changes to `.env` not reflecting:**
- Restart your application (Streamlit, Flask, etc.)
- For Jupyter notebooks, restart the kernel
- Ensure `.env` is in the correct directory (same as `main.py` or settings file)

---

## Additional Resources

- [python-dotenv documentation](https://github.com/theskumar/python-dotenv)
- [12 Factor App - Config](https://12factor.net/config)
- [OWASP - Secrets Management](https://owasp.org/www-project-top-ten/)
