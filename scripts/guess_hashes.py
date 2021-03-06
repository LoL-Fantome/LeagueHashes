#!/bin/env python3
import sys
import json

def fnv1a(s):
    h = 0x811c9dc5
    for b in s.encode('ascii').lower():
        h = ((h ^ b) * 0x01000193) & 0xFF_FF_FF_FF
    return h

def read_hash_set(listname):
    with open(listname) as inf:
        return { 
            int(line, 16) for line in inf.readlines() if line
        }

def read_hash_set_json(jsonname):
    with open(jsonname) as inf:
        return set(json.load(inf))

def read_hash_dict(listname):
    with open(listname) as inf:
        return { 
            int(line[:8], 16) : line[9:].rstrip() for line in inf.readlines() if line.rstrip()
        }

def read_word_list(listname):
    with open(listname) as inf:
        return [
            line.rstrip() for line in inf.readlines() if line
        ]

def mutate(word):
    if word.startswith('__') or word.startswith('m_') or word.startswith('ar'):
        word = word[2:]
    elif word.startswith('I') or word.startswith('m') or word.startswith('_') or word.startswith('b'):
        word = word[1:]
    if word.endswith('_'):
        word = word[:-1]
    yield word
    yield word + 'Instance'
    yield word + 'Definition'
    yield word + 'Tra'
    yield 'I' + word
    yield 'm' + word
    yield 'm_' + word

    return None

def guess(all_set, known_dict, words_list):
    result = set()
    for orgword in words_list:
        for word in mutate(orgword):
            h = fnv1a(word)
            if h in all_set and not h in known_dict:
                result.add((f"{h:08X}", word))
    return sorted(list(result), key=lambda x: (x[1].lower(), x[1], x[0]))

all_set_filename = sys.argv[1]
known_dict_filename = sys.argv[2]
words_list_filename = sys.argv[3]

all_hashes = read_hash_set_json(all_set_filename) if all_set_filename.endswith(".json") else read_hash_set(all_set_filename)
known_hashes = read_hash_dict(known_dict_filename)
words_list = read_word_list(words_list_filename)

guessed = guess(all_hashes, known_hashes, words_list)

for h, w in guessed:
    print(f"{h} {w}")
