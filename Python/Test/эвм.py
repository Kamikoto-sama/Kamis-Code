import pyperclip

text = r"""
00      MAR := PC 
01 --> MRd 
02      CR := MDR 
03      PC := PC+1 
04      MAR := ADR 
05      MDR := Acc 
06      MWr     
"""
lines = filter(lambda s: len(s) > 0, text.split("\n"))
formated = map(lambda x: x[7:].strip(), lines)
result = "\n".join(formated)
print(result)
pyperclip.copy(result)