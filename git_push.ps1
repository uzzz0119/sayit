# Git Push Script
Write-Host "=== Git Status ===" -ForegroundColor Cyan
git status

Write-Host "`n=== Adding All Changes ===" -ForegroundColor Cyan
git add -A

Write-Host "`n=== Creating Commit ===" -ForegroundColor Cyan
git commit -m "feat: optimize LLM punctuation restoration with validation

- Enhanced LLM prompt to add punctuation to only 10-20% of words
- Added discourse marker detection (so/but/because/however etc.)
- Implemented output validation (reject if >30% words have punctuation)
- Auto-fallback to Whisper original punctuation if LLM fails
- Added download_video function to audio.py for shadowing feature
- Restored shadowing blueprint and templates
- Micro-gap threshold set to 0.9s for natural pauses"

Write-Host "`n=== Pushing to GitHub ===" -ForegroundColor Cyan
git push origin master

Write-Host "`n=== Complete! ===" -ForegroundColor Green

