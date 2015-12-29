rem SET PATH=%PATH%;D:\Daten\Repositories\LearnGit\SimpleGame\SimpleGame\PythonEnv\Scripts
SET PATH=%PATH%;..\PythonEnv\Scripts

rem pyinstaller --onefile --debug ..\Src\Game.py
pyinstaller Game.spec
pause
