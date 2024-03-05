@echo off
title BOT SERVER CONSOLE
:start
echo Bem vindo ao comprasnet bot server console
call venv\Scripts\activate && echo Aperte ENTER para iniciar
pause >nul && call python main.py