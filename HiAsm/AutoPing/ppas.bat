@echo off
SET THEFILE=D:\My_Programs\HiAsm\AutoPing\AutoPing.exe
echo Linking %THEFILE%
ld.exe  -s --subsystem windows   -o D:\My_Programs\HiAsm\AutoPing\AutoPing.exe D:\My_Programs\HiAsm\AutoPing\link.res
if errorlevel 1 goto linkend
goto end
:asmend
echo An error occured while assembling %THEFILE%
goto end
:linkend
echo An error occured while linking %THEFILE%
:end
