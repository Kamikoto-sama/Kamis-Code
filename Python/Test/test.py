words = input(">").split()
words = list(filter(lambda w: len(w) > 2, words))
print(len(words), words)
