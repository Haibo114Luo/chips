@echo off
cd /d %~dp0

REM 获取本机 IPv4 地址
for /f "tokens=1,2 delims=:" %%a in ('ipconfig ^| findstr "IPv4 地址"') do (
    set ip=%%b
)
for /f "tokens=* delims= " %%i in ("%ip%") do (
    set ip=%%i
)

REM 如果 config.json 已存在，先删除
if exist config.json del config.json

REM 生成 config.json 文件
(
  echo {
  echo     "ip": "%ip%"
  echo }
) > config.json

echo config.json is already generated：
type config.json

echo Your local server address: http://%ip%:8000

REM 启动两个服务
start python -m http.server 8000
start python data.py
start python proxy.py

pause
