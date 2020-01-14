def do(m, n):
	if n > m:
		m,n = n,m
	while r := m % n:
		m = n
		n = r
	return n

m,n = map(int, input().split())
print(do(m,n))