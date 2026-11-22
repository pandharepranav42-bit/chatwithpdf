@echo off
title DocuMind AI - Chat with PDF
cd /d "%~dp0"
echo Starting DocuMind AI in Python virtual environment...
call "venv\Scripts\activate.bat"
streamlit run app.py
pause
