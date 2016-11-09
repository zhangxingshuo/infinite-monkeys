'''
Markov Chain Text Generation
============================
Takes an input corpus of text and generates new text based on a 
seed word.

Additional functionality for higher order Markov chaining.

Note that this produces a Markov chain in REVERSE; that is, it 
traverses in the opposite order. Given an input seed, it looks
at preceding words until it reaches the beginning of a sentence.

Usage:
------
    python3 markov.py [<filename>] ...
'''

import random
import re
import sys

from split import *

# Set flags for sentence beginning and end
BEGIN = '<BEGIN>'
END = '<END>'

class Markov(object):

    def __init__(self, filename, order=2):
        '''
        Creates Markov object based on corpus. Default order is 2.
        '''
        self.model = {}
        self.order = order

        # Read in the corpus text
        self.text = open(filename).read()

        # Generate list of lists
        # Outer list is list of sentences in text
        # Inner list is list of words in each sentence
        self.original_corpus = self.generate_corpus()

        self.corpus = []
        for sentence in self.original_corpus[::-1]:
            self.corpus.append(sentence[::-1])

        # Generate the Markov dictionary
        self.create_dictionary()

    def filter_sentence(self, sentence):
        '''
        Sentence filter to eliminate weird punctuation
        '''
        reject_pat = re.compile(r"(^')|('$)|\s'|'\s|[\"(\(\)\[\])]")
        # Decode unicode, mainly to normalize fancy quotation marks
        if sentence.__class__.__name__ == "str":
            decoded = sentence
        else:
            decoded = unidecode(sentence)
        # Sentence shouldn't contain problematic characters
        if re.search(reject_pat, decoded): 
            return False
        return True

    def generate_corpus(self):
        '''
        Generates list of sentences, where each sentence is a list of words
        '''
        sentences = split_into_sentences(self.text)
        filtered_sentences = list(filter(self.filter_sentence, sentences))
        words = list(map(split_into_words, filtered_sentences))
        return words

    def create_dictionary(self):
        '''
        Creates the Markov dictionary
        '''
        for sentence in self.corpus:
            item = ( [BEGIN] * self.order ) + sentence + [END]
            for i in range(len(sentence) + 1):
                state = tuple(item[i:i+self.order])
                follow = item[i+self.order]

                if state not in self.model:
                    self.model[state] = {}
                if follow not in self.model[state]:
                    self.model[state][follow] = 0

                self.model[state][follow] += 1

    def move(self, state):
        '''
        Move to next word
        '''
        choices, weights = zip(*self.model[state].items())
        totals = []
        running_total = 0

        # accumulate weights
        for weight in weights:
            running_total += weight
            totals.append(running_total)

        rnd = random.random() * running_total

        # find and return the index
        for i, total in enumerate(totals):
            if rnd < total:
                return choices[i]

    def get_overlap(self, string):
        '''
        Get length of maximum string overlap
        '''
        sanitized_corpus = re.sub(r'\W+', '', self.text).lower()
        sanitized_string = re.sub(r'\W+', '', string).lower()
        max_overlap = 0
        for start in range(len(sanitized_string) - 1):
            for end in range(start, len(sanitized_string)):
                substring = sanitized_string[start:end]
                if end - start > max_overlap:
                    if substring in sanitized_corpus:
                        max_overlap = end - start
        return max_overlap/len(sanitized_string)

    def generate_text(self, min_length=20, max_overlap_ratio=0.7, max_length=140, num_tries=10):
        '''
        Generates random text based on dictionary. Text must not overlap original text by more
        than 70%, and text must be greater than 20 chars and less than 140 chars (default).
        '''
        for _ in range(num_tries):

            state = (BEGIN,) * self.order
            next_word = self.move(state)
            text = ''
            while next_word != END:
                text += next_word + ' '
                state = tuple(state[1:]) + (next_word,)
                next_word = self.move(state)

            result = text[:-1]
            if len(result) <= max_length and len(result) > min_length:
                if self.get_overlap(result) < max_overlap_ratio:
                    return result
                    
        return None
