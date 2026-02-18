@echo off
cd /d %~dp0

REM =================================================================
REM 1. 检查 Python 是否在环境变量中
REM =================================================================
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not found in your system PATH.
    echo Please install Python and check "Add Python to PATH" during installation.
    pause
    exit
)

REM =================================================================
REM 2. 获取本机 IP 并去除所有空格
REM =================================================================
set ip=
REM 查找 IPv4 地址行
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /i "IPv4"') do (
    set ip=%%a
)

REM 【关键】将变量 ip 中的所有空格替换为空
set ip=%ip: =%

if "%ip%"=="" (
    echo Error: Could not find IP address.
    pause
    exit
)

REM =================================================================
REM 3. 生成配置文件 config.json
REM =================================================================
if exist config.json del config.json
(
  echo {
  echo     "ip": "%ip%"
  echo }
) > config.json

echo.
echo Configuration generated.
echo Local Server IP: %ip%
echo.
echo ============================================================
echo Please open this URL in your browser:
echo http://%ip%:8000
echo ============================================================
echo.

REM =================================================================
REM 4. 启动三个服务
REM 直接调用 python，假设其已在全局 PATH 中
REM =================================================================

echo Starting Web Server...
start "Web Server" cmd /k "python -m http.server 8000"

echo Starting Game Backend...
start "Game Backend" cmd /k "python data.py"

echo Starting Proxy Server...
start "Proxy Server" cmd /k "python proxy.py"

echo.
echo All services started. Do not close the new windows.
pause