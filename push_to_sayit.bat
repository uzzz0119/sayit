@echo off
echo === Adding remote to existing SayIt repository ===
git remote add origin https://github.com/uzzz0119/SayIt.git

echo.
echo === Fetching remote branches ===
git fetch origin

echo.
echo === Pushing to SayIt repository ===
git push -u origin master

echo.
echo === Success! Repository updated at: ===
echo https://github.com/uzzz0119/SayIt
echo.
pause

