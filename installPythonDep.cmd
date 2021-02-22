@echo off
 
set PYTHONDIR='td-python-dep'
set PYVER='3.7'
set MODULE='beautifulsoup4'
 
set TARGETDIR=%~dp0%PYTHONDIR:'=%
if not exist %TARGETDIR% mkdir %TARGETDIR%
 
py -%PYVER:'=% -m pip install --user --upgrade pip
py -%PYVER:'=% -m pip install %MODULE:'=% --target=%TARGETDIR%