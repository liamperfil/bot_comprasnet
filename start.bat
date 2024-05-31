pip install selenium
pip install webdriver-manager
pip install chromedriver-binary
cls
@echo off
title BOT SERVER CONSOLE
:start
echo Bem vindo ao comprasnet bot server console
call ambiente_virtual\Scripts\activate && echo Aperte ENTER para iniciar
pause >nul && call python bot_multi.py
