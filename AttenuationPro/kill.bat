@echo off
:start
if exist gokill.txt (
timeout /t  1
del gokill.txt
taskkill /IM S16.exe
)
goto start
