@echo off
echo === Adding all changes ===
git add -A

echo.
echo === Committing changes ===
git commit -m "feat: optimize LLM punctuation restoration with validation and restore shadowing feature"

echo.
echo === Pushing to GitHub ===
git push origin master

echo.
echo === Done! ===
pause

