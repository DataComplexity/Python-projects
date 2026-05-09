@echo off
echo ============================================
echo   JERRY AI - Setup Script
echo ============================================

echo [1/4] Checking Python...
python --version || (echo Python not found! Install from python.org && pause && exit)

echo [2/4] Installing dependencies...
pip install -r requirements.txt

echo [3/4] Pulling Ollama models...
ollama pull phi4-mini
ollama pull qwen3:4b
ollama pull qwen2.5-coder:7b

echo [4/4] Setting up local git...
if not exist ".git" (
    git init
    git add .
    git commit -m "Jerry v1.0 - initial setup"
) else (
    echo Git already initialised, skipping.
)

echo.
echo ============================================
echo   Setup complete!
echo   Run Jerry: python main.py
echo   UI opens at: http://localhost:8501
echo ============================================
pause
