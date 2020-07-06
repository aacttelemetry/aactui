@echo off
set /p name="Enter filename (excluding '.ui'): "
pyuic5 %name%.ui -o %name%.py