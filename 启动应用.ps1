# PowerShell 启动脚本
# 设置环境变量并启动应用

$env:OPENAI_API_KEY="sk-tR6dFiOeAz50xBLbsazmp0kcRddklaWNpfjhqPTrtYfFyf7Z"
$env:OPENAI_BASE_URL="https://api.videocaptioner.cn/v1"

Write-Host "环境变量已设置：" -ForegroundColor Green
Write-Host "OPENAI_API_KEY = $($env:OPENAI_API_KEY.Substring(0,20))..."
Write-Host "OPENAI_BASE_URL = $env:OPENAI_BASE_URL"
Write-Host ""
Write-Host "正在启动应用..." -ForegroundColor Cyan

python run.py

