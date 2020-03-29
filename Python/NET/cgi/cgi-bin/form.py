import cgi
import os
import subprocess

# Получаем GET параметр nick переданный из HTML формы
form = cgi.FieldStorage()
nick = form.getfirst("nick", "test")

# Открываем на запись scan.txt куда выведем результаты работы скрипта sherlock
fileout = open(os.getcwd()+'/cgi-bin/sherlock/scan.txt', 'w')
# Запускаем внешний скрипт sherlock.py и передаем ему nick, результат работы скрипта идет
# в файл scan.txt
theproc = subprocess.Popen(os.getcwd()+"/cgi-bin/sherlock/sherlock.py "+nick, stdout=fileout, shell = True)
theproc.communicate()
fileout.close()

# Снова открываем файл с результатами и читаем его в переменную r
f=open(os.getcwd()+'/cgi-bin/sherlock/scan.txt','r', encoding="UTF-8")
r=f.read()
f.close()

# Открываем HTML шаблон странички с результатами
f=open(os.getcwd()+'/template/form.html','r', encoding="UTF-8")
htmltemplate=f.read()
f.close()
# Заменяем в HTML шаблоне %result% на переменную r с результатами Шерлока
htmltemplate=htmltemplate.replace('%result%', r)

# Выводим в браузер
print("Content-type: text/html\n")
print(htmltemplate)

