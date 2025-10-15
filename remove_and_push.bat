@echo off
echo ========================================
echo   Cleaning and Pushing to GitHub
echo ========================================
echo.

echo === Step 1: Removing unused React component ===
if exist App.tsx (
    git rm App.tsx
    echo App.tsx removed from Git
) else (
    echo App.tsx not found, skipping...
)
echo.

echo === Step 2: Checking Git Status ===
git status --short
echo.

echo === Step 3: Adding All Files ===
git add -A
echo.

echo === Step 4: Creating Commit ===
git commit -m "chore: remove unused React component and update project

- Remove App.tsx (switched to Flask templates)
- Update README.md with comprehensive documentation
- Include all backend routes and services
- Include Faster-Whisper integration
- Include LLM punctuation restoration
- Include shadowing feature
- Include all utility modules and templates"

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
    echo Trying alternative: push to 'main' branch...
    git branch -M main
    git push -u origin main
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

