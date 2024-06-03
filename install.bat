@echo off
title BOT SERVER CONSOLE
:start
call python -m venv C:\ambiente_virtual
call C:\ambiente_virtual\Scripts\activate
pip install selenium
pip install webdriver-manager
pip install chromedriver-binary
cls
echo Bem vindo ao comprasnet bot server console
echo Programa instalado com sucesso
echo Aperte qualquer tecla para encerrar...
pause >nul