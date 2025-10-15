@echo off
echo === Adding GitHub remote ===
git remote add origin https://github.com/uzzz0119/V0_SayIt.git

echo.
echo === Renaming local branch to main ===
git branch -M main

echo.
echo === Pushing to GitHub ===
git push -u origin main

echo.
echo === Success! Repository available at: ===
echo https://github.com/uzzz0119/V0_SayIt
echo.
pause

