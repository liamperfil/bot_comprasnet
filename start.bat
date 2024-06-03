@echo off
title BOT SERVER CONSOLE
:start
echo Bem vindo ao comprasnet bot server console
call C:\ambiente_virtual\Scripts\activate
echo Aperte ENTER para iniciar
pause >nul && call python bot_one.py