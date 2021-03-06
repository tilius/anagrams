#!/usr/bin/env python

import codecs, sys, time
from bisect import bisect_left
from collections import Counter

max_word_count = 2
if len(sys.argv) > 1 and sys.argv[1].isdigit():
    max_word_count = int(sys.argv[1])
    sys.argv = sys.argv[1:]
orig_word = ''.join(sys.argv[1:]).decode('utf-8').lower()
orig_letters = set(orig_word)

print 'Extracting corpus...',
corpus = [
    word.strip() for word in codecs.open('slowa.txt', 'r', encoding='utf8').readlines() \
        if all((letter in orig_letters) for letter in word.strip())
]
print len(corpus), 'words.'

calls = 0
available_letters = Counter(orig_word)
complete_words = []

# level == x  <=>  x letters are already placed when entering the call
def search(uncomplete_word, level):
    global available_letters, complete_words, calls
    calls += 1
    if level == len(orig_word) and not uncomplete_word:
        yield complete_words
    elif len(complete_words) < max_word_count:
        for letter, count in sorted(available_letters.items()):
            if count == 0: continue
            new_word = uncomplete_word + letter
            if complete_words and new_word < complete_words[-1] and not complete_words[-1].startswith(new_word): continue
            new_word_index = bisect_left(corpus, new_word)
            if new_word_index == len(corpus): continue
            if not corpus[new_word_index].startswith(new_word): continue

            available_letters[letter] -= 1
            if corpus[new_word_index] == new_word:
                complete_words += [new_word]
                for i in search('', level + 1):
                    yield i
                complete_words.pop()
            for i in search(new_word, level + 1):
                yield i
            available_letters[letter] += 1

print 'Looking for anagrams, up to', max_word_count, 'words long...'
start = time.clock()
total = 0
for seq in search('', 0):
    print ' '.join(seq)
    total += 1
t = time.clock() - start
print 'Total anagrams found:', total, 'in', calls, 'calls, in', '%.3f' % t, 'sec,', '%.3f' % (1e6*t/calls), 'us/call'

