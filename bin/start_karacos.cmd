rem @echo off
cd %~dp0
cd ..
set KARACOS_DESKTOP_HOME=%CD%

set PYTHON_HOME=%KARACOS_DESKTOP_HOME%\lib\win32\Python26

set COUCHDB_HOME=%KARACOS_DESKTOP_HOME%\lib\win32\CouchDB_server

set PATH=%windir%;%windir%\system32;%windir%\System32\Wbem;%KARACOS_DESKTOP_HOME%\bin;%PYTHON_HOME%;%PYTHON_HOME%\DLLs;%COUCHDB_HOME%\bin;%COUCHDB_HOME%\erts-5.8\bin
set PYTHONPATH=%KARACOS_DESKTOP_HOME%\lib\python;%KARACOS_DESKTOP_HOME%\Lib


python %KARACOS_DESKTOP_HOME%\py\start_karacos.py

pause
