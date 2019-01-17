python db_generator.py 0
pyinstaller --onefile --icon=icons\pls.ico --noconsole main.py
del main.spec
rmdir /s /q build
mkdir dist\icons dist\gui
copy style.css dist
copy data.pls dist
copy gui dist\gui
copy icons dist\icons
rename dist build