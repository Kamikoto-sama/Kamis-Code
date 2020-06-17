from .queue import Queue

def ngram(values, n:int=2):
	currNgram = Queue(maxCount = n)
	for i in values:
		currNgram.enqueue(i)
		if len(currNgram) == n:
			yield tuple(currNgram)
	if len(currNgram) < n:
		raise ValueException()