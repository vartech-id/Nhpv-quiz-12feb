@echo off
setlocal

set "ROOT=%~dp0"

echo Starting frontend server...
start "Frontend - bun dev" cmd /k "cd /d ""%ROOT%frontend"" && bun run dev"

echo Starting backend server...
start "Backend - uvicorn" cmd /k "cd /d ""%ROOT%backend"" && call "".venv\Scripts\activate.bat"" && uvicorn main:app --reload"

echo Both servers have been started in separate windows.
endlocal
