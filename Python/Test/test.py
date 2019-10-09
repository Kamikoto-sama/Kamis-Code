l, r = [int(i) for i in input().split()]

if r < 40:
	print(r * 2 + 40 + (l - 40) * 2)
elif r < l:
	print(40 + (l - 40) * 2 + r)
else:
	print(r * 2 + 40)