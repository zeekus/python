def anagrams(word, words):
    return [x for x in words if sorted(list(x)) == sorted(list(word))]