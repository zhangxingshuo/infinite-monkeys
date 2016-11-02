'''
Rhyming Dictionary
==================
Given a word list, creates a dictionary of rhyming pairs within 
the word list.

Usage:
------
    python3 rhyme_dict.py [<filename>]

    will write the rhyming dictionary to the file [<filename>].pkl
'''

import nltk
from nltk.corpus import cmudict
import sys
import pickle

import os
path = os.getcwd()

# Print iterations progress
def printProgress (iteration, total, prefix = '', suffix = '', decimals = 1, barLength = 100):
    '''
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        barLength   - Optional  : character length of bar (Int)
    
    Credit: http://stackoverflow.com/a/34325723
    '''
    formatStr       = "{0:." + str(decimals) + "f}"
    percents        = formatStr.format(100 * (iteration / float(total)))
    filledLength    = int(round(barLength * iteration / float(total)))
    bar             = '█' * filledLength + '-' * (barLength - filledLength)
    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),
    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()

class rhymer(object):

    def __init__(self, filename):
        self.dict = cmudict.dict()
        self.entries = cmudict.entries()

        self.filename = filename

        # Sanitize and check word is in CMU dictionary
        self.word_list = self.load(filename)

    def sanitize(self, word):
        '''
        Strips word of all nonalpha characteres
        '''

        result = ''.join(letter for letter in word if letter.isalpha())
        return result.lower()

    def load(self, filename):
        '''
        Overwrites the 10,000 most common English words with a new
        set of words generated from a corpus of text
        '''
        word_list = set()

        file = open(path + '/' + filename)
        raw_text = file.read().split()
        for word in raw_text:
            clean_word = self.sanitize(word)
            if clean_word in self.dict:
                word_list.update([clean_word])

        return word_list

    def rhyme_set(self, input_word, level):
        '''
        Returns set of all words that rhyme with the input word at given level,
        i.e. the number of element matches in the pronunciation
        
        Supports restricting restricting the rhyme set to eliminate repeat rhymes.
        '''

        # Get the pronunciation of the word
        syllable = self.dict[input_word][0]

        # Find all matching pronunciations, i.e. rhymes, of word
        rhymes = [word for word in self.word_list if self.dict[word][0][-level:] == syllable[-level:]]

        # Remove the rhymes from restricted set
        rhyming_set = set(rhymes)

        # The input does not rhyme with itself
        rhyming_set.remove(input_word)

        return rhyming_set

    def write(self):
        '''
        Writes a rhyming dictionary to a binary file that can be loaded later for 
        rapid rhyme retrieval
        '''

        # Initialize rhyming dictionary
        ret_dict = {}
        count = 0

        # Intialize progress bar
        out_file = os.path.splitext(path + '/' + self.filename)[0] + '.pkl'
        print('Writing to %s...' % out_file)
        printProgress(count, len(self.word_list), prefix = 'Progress:', suffix = 'Complete', barLength = 50)

        for word in self.word_list:

            # Shorter words need higher rhyme levels to sound better
            num_elements = len(self.dict[word][0])
            if num_elements < 4:
                rhyme_level = num_elements
            else:
                rhyme_level = num_elements - 1

            # Get the rhyming set
            rhyme_s = self.rhyme_set(word, rhyme_level)
            if len(rhyme_s) > 0:
                ret_dict[word] = rhyme_s

            # Show progress
            count += 1
            printProgress(count, len(self.word_list), prefix = 'Progress:', suffix = 'Complete', barLength = 50)

        # Dump the dictionary in the file "[<filename>].pkl"
        pickle.dump( ret_dict, open(out_file, 'wb') )
        return ret_dict

if __name__ == '__main__':
    filename = sys.argv[1]
    rhyme = rhymer(filename)
    rhyme.write()