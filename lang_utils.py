'''
Language Utilities
==================
Provides functionality for rhyming and cadences from the 
Natural Language Toolkit and the Carnegie Mellon University
Pronunciation Dictionary

All rhymes are pulled from Google's 10,000 most common 
English words.

Usage:
------
    python3 -i lang_utils.py
'''

import nltk
from nltk.corpus import cmudict
import sys
import os

path = os.getcwd()

########################
### Helper Functions ###
########################

def sanitize(word):
    '''
    Strips word of all nonalpha characteres
    '''

    result = ''.join(letter for letter in word if letter.isalpha())
    return result.lower()

def load(filename):
    '''
    Overwrites the 10,000 most common English words with a new
    set of words generated from a corpus of text
    '''
    word_list = set()

    file = open(path + '/' + filename)
    raw_text = file.read().split()
    for word in raw_text:
        clean_word = sanitize(word)
        if clean_word in p_dict:
            word_list.update([clean_word])

    return word_list

########################
### Language Methods ###
########################

p_dict = cmudict.dict()
word_list = load('data/english.txt')

def rhyme_set(input_word, level):
    '''
    Returns set of all words that rhyme with the input word at given level,
    i.e. the number of element matches in the pronunciation
    '''

    # Get the pronunciation of the word
    raw_syllables = p_dict[input_word]

    # Discard stresses
    syllables = []
    for syllable in raw_syllables:
        syllables += [list(map(sanitize, syllable))]

    total_rhymes = set()

    # Find all matching pronunciations, i.e. rhymes, of word
    for syllable in syllables:
        rhymes = []
        for word in word_list:
            for raw_pron in p_dict[word]:
                # Discard stresses
                pron = list(map(sanitize, raw_pron))
                if pron[-level:] == syllable[-level:] and pron != syllable:
                    rhymes += [word]

        rhyming_set = set(rhymes)
        total_rhymes.update(rhyming_set)

    return total_rhymes

def rhyme(word):
    '''
    Determines the optimal rhyme level for a word and returns the 
    corresponding rhyme set
    '''
    num_elements = len(p_dict[word][0])
    if num_elements < 4:
        rhyme_level = num_elements
    else:
        rhyme_level = num_elements - 1

    # Get the rhyming set
    return rhyme_set(word, rhyme_level)

def stress(word):
    '''
    Returns syllable pattern of input word
    A '0' denotes no stress, '1' is primary stress, '2' is secondary stress
    The '*' denotes a one syllable word, i.e. indeterminate stress
    '''

    # Check if word in dictionary
    if word.lower() not in p_dict:
        raise KeyError('Word not found in CMU dictionary', word)

    else:
        # Get the primary pronunciation from CMU dictionary
        pronunciation = p_dict[word.lower()][0]

        syllables = ''
        for elem in pronunciation:
            if elem[-1] == '0' or elem[-1] == '1' or elem[-1] == '2':
                syllables += elem[-1]

        # One syllable words are neither stressed nor unstressed
        if len(syllables) == 1:
            return '*'
        else:
            return syllables

def syllables(word):
    '''
    Groups phonemes into syllable clusters
    '''

    # Get the phonemes
    phonemes = p_dict[word][0]

    # Initialize list to hold syllables and running syllable list
    syls = []
    syl = []

    for i in range(len(phonemes)):

        # Add phoneme to the running string
        syl += [phonemes[i]]

        # If phoneme is vowel, add to list and reset running string
        if '0' in phonemes[i] or '1' in phonemes[i] or '2' in phonemes[i]:
            syls.append(syl)
            syl = []

    # If last phoneme sequence does not contain vowel, append to last syllable
    if syl != '' and len(syls) > 0:
        syls[-1].extend(syl)
    else:
        syls.append(syl)

    return syls

def complexity(self, word):
    '''
    Stoel-Gammon's Word Complexity Measure

    C. Stoel-Gammon. 2010. The Word Complexity Measure: Description and 
    application to developmental phonology and disorders. Clinical
    Linguistics and Phonetics 24(4-5): 271-282.
    '''
    phonemes = p_dict[word][0]
    stress_pattern = stress(word)
    syllables = syllables(word)

    # Constant phoneme classses
    VELARS = set("K G NG".split())
    LIQUIDS = set("L R".split())
    VOICED_AF = set("V DH Z ZH".split())
    AF = set("F TH S SH CH".split()) | VOICED_AF

    score = 0

    # WORD PATTERNS
    # (1) More that one syllable receives 1 point
    if len(stress_pattern) > 2:
        score += 1

    # (2) Stress on syllable after first receives 1 point
    if '1' in stress_pattern[1:] or '2' in stress_pattern[1:]:
        score += 1

    # SYLLABLE STRUCTURE
    # (1) End with a word-final consonant receives 1 point
    if phonemes[-1][-1] != '0' or phonemes[-1][-1] != '1' or phonemes[-1][-1] != '2':
        score += 1

    # (2) Syllable clusters, i.e. syllable with more than two consonants, receive
    # one point for each cluster
    for syl in syllables:
        if len(syl) > 2:
            score += 1

    # SOUND CLASSES
    # (1) Velar consonants receive 1 point for each velar
    score += sum(ph in VELARS for ph in phonemes)

    # (2) Liquid, syllabic liquid, or rhotic vowel receive 1 point each
    score += sum(ph in LIQUIDS for ph in phonemes)

    # (3) Voiced fricatives or affricates receive 1 point each
    score += sum(ph in VOICED_AF for ph in phonemes)

    # (4) Fricatives and affricates receive an additional point each
    score += sum(ph in AF for ph in phonemes)

    # Normalize the score to the number of syllables
    try:
        return score / len(stress_pattern)

    # Some words have no syllables
    except:
        return 100.0