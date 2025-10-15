@echo off
echo ========================================
echo   Pushing All Code to GitHub
echo ========================================
echo.

echo === Step 1: Checking Git Status ===
git status --short
echo.

echo === Step 2: Adding All Files ===
git add -A
echo.

echo === Step 3: Showing Staged Files ===
git diff --cached --name-only
echo.

echo === Step 4: Creating Commit ===
git commit -m "docs: update README and prepare for GitHub push

- Updated README.md with comprehensive feature documentation
- Faster-Whisper integration details
- LLM punctuation restoration explanation
- Complete usage guide and technical stack
- Project structure and configuration details
- All backend routes and services
- Frontend templates (Flask-based)
- Utility modules for caption, AI, audio processing
- Requirements and documentation files"

echo.
echo === Step 5: Adding Remote Repository ===
git remote add origin https://github.com/uzzz0119/SayIt.git 2>nul
if errorlevel 1 (
    echo Remote 'origin' already exists, continuing...
) else (
    echo Remote 'origin' added successfully!
)
echo.

echo === Step 6: Verifying Remote ===
git remote -v
echo.

echo === Step 7: Pushing to GitHub ===
git push -u origin master
echo.

if errorlevel 1 (
    echo.
    echo ========================================
    echo   ERROR: Push failed!
    echo ========================================
    echo.
    echo Possible reasons:
    echo 1. Remote already has different commits - try: git pull origin master --rebase
    echo 2. Authentication required - make sure you're logged in to GitHub
    echo 3. Branch name mismatch - remote might use 'main' instead of 'master'
    echo.
    echo To force push (CAUTION - overwrites remote):
    echo git push -f origin master
    echo.
) else (
    echo.
    echo ========================================
    echo   SUCCESS! Code pushed to GitHub
    echo ========================================
    echo.
    echo Repository: https://github.com/uzzz0119/SayIt
    echo.
)

pause

