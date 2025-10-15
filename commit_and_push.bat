@echo off
echo === Adding README.md ===
git add README.md

echo.
echo === Committing changes ===
git commit -m "docs: update README with all new features

- Faster-Whisper integration with word-level timestamps
- LLM intelligent punctuation restoration
- Output quality validation (reject >30%% punctuation rate)
- Silence block and micro-gap optimization
- Shadowing feature restoration
- Complete technical stack and project structure
- Usage guide and configuration details"

echo.
echo === Adding remote (if not exists) ===
git remote add origin https://github.com/uzzz0119/SayIt.git 2>nul
if errorlevel 1 (
    echo Remote already exists, skipping...
)

echo.
echo === Pushing to GitHub ===
git push -u origin master

echo.
echo === Success! Repository updated at: ===
echo https://github.com/uzzz0119/SayIt
echo.
pause

