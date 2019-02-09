python db_generator.py 0
rmdir /s /q build

pyinstaller --onefile --icon=icons\pls.ico --noconsole main.py
del main.spec
rmdir /s /q build
mkdir dist\icons dist\gui
copy style.css dist
copy data.pls dist
copy gui dist\gui
copy icons dist\icons
rename dist\main.exe PlayListStore4.exe
rename dist _build_

pyinstaller --onefile --icon=icons\updater.ico --noconsole updater.py
del updater.spec
rmdir /s /q build
move dist\\updater.exe _build_
rmdir /s /q dist
rename _build_ build

del ..\..\Release\PLS4.rar
start winrar a -r ..\..\Release\PLS4 build