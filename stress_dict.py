'''
Word Stress Dictionary
======================
Makes a dictionary of the stress patterns of different
words using the CMU Pronunciation Dictionary. 

Note that only the primary pronunciation is considered.

Also supports grouping phonemes into syllable clusters,
as well as the Stoel-Gammon Word Complexity Measure (WCM)

Usage:
------
    python3 cmudict_parse.py

    will write the dictionary to the pickle file 'cmudict.pkl'
'''

import nltk
from nltk.corpus import cmudict
import pickle
import sys

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

    def complexity(self, word):
        '''
        Stoel-Gammon's Word Complexity Measure

        C. Stoel-Gammon. 2010. The Word Complexity Measure: Description and 
        application to developmental phonology and disorders. Clinical
        Linguistics and Phonetics 24(4-5): 271-282.
        '''
        phonemes = self.dict[word][0]
        stress_pattern = self.stress(word)
        syllables = self.syllables(word)

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

    def syllables(self, word):
        '''
        Groups phonemes into syllable clusters
        '''

        # Get the phonemes
        phonemes = self.dict[word][0]

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
        if syl != '' and len(syls) > 1:
            syls[-1].extend(syl)
        else:
            syls.append(syl)

        return syls

    def write(self):
        '''
        Write to a dictionary containing the words as keys and stresses
        as values
        '''
        ret_dict = {}

        print("Writing to " + path + "/data/cmudict.pkl...")
        count = 0
        printProgress(count, len(self.dict), prefix = 'Progress:', suffix = 'Complete', barLength = 50)

        for word in self.dict:
            stress = self.stress(word)
            ret_dict[word] = (stress, self.complexity(word))
            count += 1
            printProgress(count, len(self.dict), prefix = 'Progress:', suffix = 'Complete', barLength = 50)

        pickle.dump( ret_dict, open(path + '/data/cmudict.pkl', 'wb') )

        return ret_dict

if __name__ == '__main__':
    parser = cmudict_parser()
    parser.write()