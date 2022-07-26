def anagrams(word, words):
    return [trial for trial in words if sorted(trial) == sorted(word)]