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
rename dist\main.exe "PlayListStore 4.exe"
rename dist build
del ..\..\Release\PLS4.rar
start winrar a -r ..\..\Release\PLS4 build