# PowerShell launcher for DocuMind AI
Set-Location -Path $PSScriptRoot
Write-Host "🚀 Launching DocuMind AI via virtual environment..." -ForegroundColor Cyan
& ".\venv\Scripts\streamlit.exe" run app.py
