'''
Word Stress Dictionary
======================
Makes a dictionary of the stress patterns of different
words using the CMU Pronunciation Dictionary. 

Note that only the primary pronunciation is considered.

Usage:
------
    python3 cmudict_parse.py

    will write the dictionary to the pickle file 'cmudict.pkl'
'''

import nltk
from nltk.corpus import cmudict
import pickle

class cmudict_parser(object):

    def __init__(self):
        self.dict = cmudict.dict()

    def stress(self, word):
        '''
        Returns syllable pattern of input word
        A '0' denotes no stress, '1' is primary stress, '2' is secondary stress
        The '*' denotes a one syllable word, i.e. indeterminate stress
        '''

        # Check if word in dictionary
        if word.lower() not in self.dict:
            raise KeyError('Word not found in CMU dictionary', word)

        else:
            # Get the primary pronunciation from CMU dictionary
            pronunciation = self.dict[word.lower()][0]

            syllables = ''
            for elem in pronunciation:
                if elem[-1] == '0' or elem[-1] == '1' or elem[-1] == '2':
                    syllables += elem[-1]

            # One syllable words are neither stressed nor unstressed
            if len(syllables) == 1:
                return '*'
            else:
                return syllables

    def write(self):
        '''
        Write to a dictionary containing the words as keys and stresses
        as values
        '''
        ret_dict = {}
        for word in self.dict:
            stress = self.stress(word)
            ret_dict[word] = stress

        pickle.dump( ret_dict, open('cmudict.pkl', 'wb') )

        return ret_dict

if __name__ == '__main__':
    parser = cmudict_parser()
    parser.write()