import os
# Грузим из файла HTML шаблон с формой
f=open(os.getcwd()+'/template/index.html','r', encoding="UTF-8")
s=f.read()
f.close()
# Обязательно сперва выводим "Content-type: text/html\n"
print("Content-type: text/html\n")
# Выводим HTML шаблон
print(s)
