@echo off
cd /d C:\Users\user\Desktop\agentic_ai\shopping_project\shopping-app
python create_store_db.py --force
python verify_db.py
