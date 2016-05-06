#!/usr/bin/env python

import sys
from collections import Counter

orig_word = ''.join(sys.argv[1:]).lower()
orig_letters = set(orig_word)
corpus = [word.strip() for word in open('slowa.txt').readlines() if all((letter in orig_letters) for letter in word.strip())]
print corpus

result = []

# level == x  <=>  x letters are already placed when entering the call
def search(available_letters, complete_words, uncomplete_word, level):
    if level == len(orig_word) and not uncomplete_word:
        global result
        result += [complete_words]
    else:
        for (letter, count) in available_letters.items():
            if count == 0: continue
            new_word = uncomplete_word + letter
            if complete_words and new_word < complete_words[-1]: continue
            updated_letters = available_letters.copy()
            updated_letters[letter] -= 1
            if new_word in corpus:
                search(updated_letters, complete_words + [new_word], '', level + 1)
            search(updated_letters, complete_words, new_word, level + 1)

search(Counter(orig_word), [], '', 0)
result.sort()
print result

