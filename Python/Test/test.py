from re import fullmatch

def validate(number: str):
	# number = prepare(number, "+() \t-", "")
	pattern = r"((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}"
	result = fullmatch(pattern, number)
	if	result is None:
		return False
	# return f"+7 ({result.group(2)}) {result.group(3)}-{result.group(4)}-{result.group(5)}"
	return True

def prepare(sourceString, olds, new):
	for i in olds:
		sourceString = sourceString.replace(i, new)
	return sourceString

def test():
	numbers = map(lambda x: x.strip(), open("numbers.txt").readlines())
	for i in numbers:
		print(i, "=", validate(i))
		
test()