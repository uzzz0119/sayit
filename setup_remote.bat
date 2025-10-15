@echo off
echo === Current Git Remote Configuration ===
git remote -v

echo.
echo === Please provide your GitHub repository information ===
echo Example: https://github.com/yourusername/V0_SayIt.git
echo.
set /p REPO_URL="Enter your GitHub repository URL: "

echo.
echo === Adding remote origin ===
git remote add origin %REPO_URL%

echo.
echo === Verifying remote ===
git remote -v

echo.
echo === Pushing to GitHub ===
git push -u origin master

echo.
echo === Done! ===
pause

