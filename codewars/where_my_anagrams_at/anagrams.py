def anagrams(word, words):
    target_word=''.join(sorted(word))
    anagrams=[]
    for word in words:
      sorted_word=''.join(sorted(word))
      if target_word == sorted_word: 
        anagrams.append(word)
    return anagrams