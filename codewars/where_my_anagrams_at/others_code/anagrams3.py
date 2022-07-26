def anagrams(word, words):
    return list(filter(lambda x: sorted(x) == sorted(word), words))