from math import factorial
from functools import reduce

def P(n, *args):
	return factorial(n) // reduce(lambda x, y: x * factorial(y), args, 1)

def A(n, m):
	return (factorial(n) // factorial(n - m)) if n >= m else 0

def C(n, m):
	return (A(n, m) // factorial(m)) if m <= n else 0

def C_(t, k):
	return C(t - 1 + k, k)