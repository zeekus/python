def anagrams(word, words):
    word=sorted(word)
    return list(filter(lambda ele: sorted(ele)==word  ,words))