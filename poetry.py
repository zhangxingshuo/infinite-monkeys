'''
Poetry Generator
================
Extensible class for generating prose and and poetry
using the Natural Language Toolkit and the Carnegie 
Mellon Pronunciation Dictionary

"Given an infinite number of monkeys at an infinite number of
typewriters working for an infinite amount of time, one will
eventually produce a work worthy of Shakespeare"
                                --The Infinite Monkey Theorem

Usage:
------
    The Poet object supports composition of haikus, love poems,
    limericks, sonnets, and villanelles, with more forms of 
    poetry planned. 

    To use, create a Poet instance and call the corresponding
    print poem function. For example,

    >>> p = Poet()
    >>> p.print_haiku()

    A Nonsense Haiku
    By Poetry Bot

    Quantum dimension
    Offense guardian save bring
    Thank validation

    Composed in 0.01 seconds    
'''

import pickle

import re
import random
import time

import os
import sys

# Get the py-verse directory
path = os.path.abspath(os.path.dirname(sys.argv[0]))

class Poet(object):

    def __init__(self, filename=None):

        # Import the CMU dictionary of pronunciation and stress
        self.dict = pickle.load( open(path + '/data/cmudict.pkl', 'rb') ) 

        # Load the word list from the input corpus
        if not filename:
            self.word_list = self.load(path + '/data/english.txt')
        else:
            self.word_list = self.load(filename)

        # Try to find the rhyming dictionary file
        # If it does not exist, default to the 10,000 most common words from Google
        try:
            self.rhyme_dict = pickle.load( open(os.path.splitext(filename)[0] + '.pkl', 'rb') )
        except:
            self.rhyme_dict = pickle.load( open(path + '/data/english.pkl', 'rb') )


    ##############
    ### Poetry ###
    ##############

    def print_random(self):
        '''
        Composes a random poem from available selection
        '''

        start = time.time()

        print(self.compose_random_poem())

        end = time.time()
        print('Composed in %0.2f seconds' % (end-start))

    def compose_random_poem(self):
        '''
        Composes a random poem from the available forms of poetry.
        '''
        
        poetry_methods = [self.string_love_poem, self.string_haiku, self.string_doublet, 
        self.string_limerick, self.string_sonnet, self.string_quatrain, 
        self.string_villanelle, self.string_ballade]

        random_poem = random.choice(poetry_methods)

        return random_poem()

    def print_love_poem(self):
        '''
        Composes a love poem and prints it to console
        '''

        start = time.time()

        final_poem = self.string_love_poem()

        end = time.time()

        print(final_poem)
        print('Composed in %0.2f seconds' % (end-start))

    def string_love_poem(self):
        love_poem = self.compose_love_poem()

        # Keep generating until there is valid line
        while love_poem[-1] is None:
            love_poem = self.compose_love_poem()

        final_poem = self.format_poem(love_poem, title='A Nonsense Love Poem')
        return final_poem

    def print_haiku(self):
        '''
        Composes a haiku and prints it to console
        '''

        start = time.time()

        final_poem = self.string_haiku()

        end = time.time()

        print(final_poem)
        print('Composed in %0.2f seconds' % (end-start))

    def string_haiku(self):
        haiku = self.compose_haiku()

        final_poem = self.format_poem(haiku, title='A Nonsense Haiku')
        return final_poem

    def print_doublet(self):
        '''
        Composes a doublet and prints it to console
        '''

        start = time.time()

        final_poem = self.string_doublet()

        end = time.time()

        print(final_poem)
        print('Composed in %0.2f seconds' % (end-start))

    def string_doublet(self):
        doublet = self.compose_doublet()

        # Keep looking for valid doublets
        while doublet[-1] is None:
            doublet = self.compose_doublet()

        final_poem = self.format_poem(doublet, title='A Nonsense Doublet')
        return final_poem

    def print_limerick(self):
        '''
        Composes a limerick and prints it to console

        Note: May take longer than other poems, as limericks
        are stricter in rhyme scheme and have many lines
        '''

        start = time.time()

        final_poem = self.string_limerick()

        end = time.time()

        print(final_poem)
        print('Composed in %0.2f seconds' % (end-start))

    def string_limerick(self):
        limerick = self.compose_limerick()

        while None in limerick:
            limerick = self.compose_limerick()

        final_poem = self.format_poem(limerick, title='A Nonsense Limerick')
        return final_poem

    def print_sonnet(self):
        '''
        Composes a Shakespearean sonnet and prints it to console

        Note: Sonnects are complex, with multiple rhyming lines and
        a strict meter, so composition might take longer than others.
        '''

        start = time.time()

        final_poem = self.string_sonnet()

        end = time.time()

        print(final_poem)
        print('Composed in %0.2f seconds' % (end-start))

    def string_sonnet(self):
        sonnet = self.compose_sonnet()

        while None in sonnet:
            sonnet = self.compose_sonnet()

        title = self.generate_title(sonnet)

        final_poem = '\n"' + title + '"' + '\nA Nonsense Sonnet\nBy Poetry Bot\n\n'

        # Add the first 12 lines
        for i in range(12):
            string_to_add = ' '.join(sonnet[i])
            final_poem += string_to_add[0].upper() + string_to_add[1:] + '\n'
            if (i+1) % 4 == 0:
                final_poem += '\n'

        # Add the final two lines
        for i in range(12, 14):
            string_to_add = ' '.join(sonnet[i])

            final_poem += string_to_add[0].upper() + string_to_add[1:] + '\n'

        return final_poem

    def print_quatrain(self):
        '''
        Composes a Frostian quatrain and prints it to console
        '''

        start = time.time()

        final_poem = self.string_quatrain()

        end = time.time()

        print(final_poem)
        print('Composed in %0.2f seconds' % (end-start))

    def string_quatrain(self):
        quatrain = self.compose_quatrain()

        while None in quatrain:
            quatrain = self.compose_quatrain()

        final_poem = self.format_poem(quatrain, title='A Nonsense Quatrain')
        return final_poem

    def print_villanelle(self):
        '''
        Composes a villanelle and prints it to console

        Note that villanelles are longer and need a special method
        to handle printing
        '''

        start = time.time()

        final_poem = self.string_villanelle()

        end = time.time()

        print(final_poem)
        print('Composed in %0.2f seconds' % (end-start))

    def string_villanelle(self):
        villanelle = self.compose_villanelle()

        while None in villanelle:
            villanelle = self.compose_villanelle()

        end = time.time()

        title = self.generate_title(villanelle)

        final_poem = '\n"' + title + '"' + '\nA Nonsense Villanelle\nBy Poetry Bot\n\n'

        # Add first four tercets
        for i in range(4):
            for j in range(3):
                string_to_add = ' '.join(villanelle[3*i+j])
                final_poem += string_to_add[0].upper() + string_to_add[1:] + '\n'
            final_poem += '\n'

        # Add last stanza
        for k in range(15,19):
            string_to_add = ' '.join(villanelle[k])
            final_poem += string_to_add[0].upper() + string_to_add[1:] + '\n'

        return final_poem

    def print_ballade(self):
        '''
        Composes a ballade and prints to console

        Since this is a complex poem with multiple rhyming lines, expect
        runtime to vary
        '''

        start = time.time()

        final_poem = self.string_ballade()

        end = time.time()

        print(final_poem)
        print('Composed in %0.2f seconds' % (end-start))

    def string_ballade(self):
        ballade = self.compose_ballade()

        while None in ballade:
            ballade = self.compose_ballade()

        title = self.generate_title(ballade)

        final_poem = '\n"' + title + '"' + '\nA Nonsense Ballade\nBy Poetry Bot\n\n'

        # Add first stanza
        for i in range(8):
            string_to_add = ' '.join(ballade[i])
            final_poem += string_to_add[0].upper() + string_to_add[1:] + '\n'

        final_poem += '\n'

        # Add envoy
        for j in range(8,12):
            string_to_add = ' '.join(ballade[j])
            final_poem += string_to_add[0].upper() + string_to_add[1:] + '\n'

        return final_poem


    #########################
    ### Sentence cleaning ###
    #########################

    def tokenize(self, sentence):
        '''
        Splits a sentence into words using regular expression
        '''

        word_split_pattern = re.compile(r"\s+")
        return re.split(word_split_pattern, sentence)

    def sanitize(self, word):
        '''
        Strips word of all nonalpha characteres
        '''

        result = ''.join(letter for letter in word if letter.isalpha())
        return result.lower()

    def format_line(self, line, last=False):
        '''
        Makes first character uppercase and adds newline character to end
        for printing lines of poetry nicely
        '''

        string_line = ' '.join(line)
        if last:
            return string_line[0].upper() + string_line[1:] + '\n'
        else:
            return string_line[0].upper() + string_line[1:] + '\n'

    def format_poem(self, poem, title, author='Poetry Bot'):
        '''
        Formats a list of lines into a nice poem
        '''

        # Generate random title
        rand_title = self.generate_title(poem)

        # Format title and author lines
        string_poem = '\n"' + rand_title + '"\n' + title + '\nBy ' + author + '\n\n'

        for line in poem[:-1]:
            string_poem += self.format_line(line)
        string_poem += self.format_line(poem[-1], last=True)

        return string_poem

    def generate_title(self, poem, length=0):
        '''
        Given a poem, which is formatted as an array of string arrays,
        randomly generate a title
        '''

        # determine the length of title
        if length == 0:
            length = random.randint(1, 5)

            # short poems should have shorter titles
            length = min(length, len(poem))

        title = []

        # Get a random word from random line
        for _ in range(length):
            rand_line = random.choice(poem)
            rand_word = random.choice(rand_line)

            # Titles are capitalized
            title += [rand_word[0].upper() + rand_word[1:]]

        return ' '.join(title)


    ######################
    ### Corpus Loading ###
    ######################

    def load(self, filename):
        '''
        Load in a corpus of text and extract all unique occurrences
        of words that are in the CMU dictionary
        '''

        word_list = set()

        file = open(filename)
        raw_text = file.read().split()
        for word in raw_text:
            clean_word = self.sanitize(word)
            if clean_word in self.dict:
                word_list.update([clean_word])

        return list(word_list)

    ###############
    ### Cadence ###
    ###############

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
            return self.dict[word.lower()][0]

    def complexity(self, word):
        '''
        Returns the complexity of the input word.
        Complexity is defined as the average phoneme length across all pronunciations
        divided by the number of syllables in the word.
        '''

        # Check if word in dictionary
        if word.lower() not in self.dict:
            raise KeyError('Word not found in CMU dictionary', word)

        else:
            return self.dict[word.lower()][1]

    def nsyl(self, word):
        '''
        Returns the number of syllables in input word
        '''

        # Leverage the stress function to calculate the number
        # of syllables for us
        return len(self.stress(word))

    def cadence(self, sentence):
        '''
        Returns the cadence pattern of sentence
        Note that * denotes an indeterminate stress
        '''

        # Tokenize input
        words = self.tokenize(sentence)

        # Map the stress onto each word in sentence
        cadence = list(map(self.stress, words))

        return ''.join(cadence)

    def cadence_match(self, cad, pattern, reverse=False):
        '''
        Recursively traverses both patterns to match

        By default, the matching is done in the forward 
        direction, so returns true if the input cadence 
        matches the START of the pattern

        The reverse flag will match the input cadence from the 
        end of the pattern in reverse, so returns true if the
        input cadence matches the END of the pattern
        '''

        # Base cases: empty strings
        if len(cad) == 0:
            return True
        elif len(pattern) == 0:
            return False

        # Recursive case
        # Note: Patterns match if stresses match exactly, or the pattern is indeterminate
        # and the input cadence has no stress. We do not want a stressed syllable matching 
        # an indeterminate syllable. 
        else:
            if reverse:
                if cad[-1] == pattern[-1] or cad[-1] == '0' and pattern[-1] == '*':
                    return self.cadence_match(cad[:-1], pattern[:-1], reverse=True)
                else:
                    return False
            else:
                if cad[0] == pattern[0] or cad[0] == '0' and pattern[0] == '*':
                    return self.cadence_match(cad[1:], pattern[1:])
                else:
                    return False


    ###############
    ### Rhyming ###
    ###############

    def rhyme_set(self, input_word, restricted=set()):
        '''
        Returns the set of all words that rhyme with the 
        input word, encompassing all possible pronunciations
        '''

        if input_word not in self.rhyme_dict:
            return None

        # Get the rhymes from the pre-compiled dictionary
        rhyming_set = self.rhyme_dict[input_word]

        # Remove the restricted set
        rhyming_set.difference_update(restricted)

        return rhyming_set

    def rhyme(self, input_word, min_rhymes=1, restricted=set()):
        '''
        Given word, returns random rhyming word, or None if none exists
        '''

        if input_word.lower() not in self.dict:
            return None

        rhymes = self.rhyme_set(input_word, restricted)

        if rhymes is None:
            return None

        if len(rhymes) < min_rhymes:
            return None

        return random.sample(rhymes, 1)[0]


    #######################
    ### Line Generation ###
    #######################

    def generate_line(self, num_syl):
        '''
        Recursively generates a line with given number of syllables
        '''

        # Base case: zero syllables
        if num_syl == 0:
            return []

        # Recursive case
        else:
            word = random.choice(self.word_list)

            # Randomly get a word of the correct length and low phoneme complexity
            while self.nsyl(word) > num_syl or self.complexity(word) > 3:
                word = random.choice(self.word_list)

            return [word] + self.generate_line(num_syl - self.nsyl(word))

    def generate_stress_line(self, pattern, num_tries=500):
        '''
        Generate a line matching a given pattern

        Given that this is a stochastic process, we specify a number of
        attempts to find a matching word to fit the pattern

        If the number of tries is exceeded, the function cuts and returns
        a None where it cut off

        Note that patterns should not end in '1', as there are no one
        syllable words with primary stress
        '''

        # Base case: no pattern
        if len(pattern) == 0:
            return []

        # Recursive case
        else:
            # Copy the pattern and operate on the copy
            if pattern[-1] == '1':
                pattern_copy = pattern[:][:-1] + '*'
            else:
                pattern_copy = pattern[:]

            word = random.choice(self.word_list)

            # Try to find a matching word through random retrieval
            tries = 0
            while not self.cadence_match(self.stress(word), pattern_copy):
                word = random.choice(self.word_list)

                # Words with too many phonemes do not flow well
                while self.complexity(word) > 2.5:
                    word = random.choice(self.word_list)

                tries += 1

                # Stop if number of attempts is exceeded
                # This implies that the cadence is impossible to match
                if tries > num_tries:
                    return [None]

            return [word] + self.generate_stress_line(pattern_copy[self.nsyl(word):])

    def generate_rhyming_line(self, num_syl, last_word, num_tries=10, restricted=set()):
        '''
        Generates a line that rhymes with given word

        Again, this is a stochastic process, so we specify the maximum number
        of attempts to make.

        This is a more robust line generator than generate_stress_line, as 
        rhymes are more easy to come by.
        '''

        for _ in range(num_tries):

            # Get a rhyming word
            rhyme_word = self.rhyme(last_word, restricted=restricted)
            if rhyme_word == None or self.nsyl(rhyme_word) > num_syl:
                continue

            # Generate the rest of the words
            last_line = self.generate_line(num_syl - self.nsyl(rhyme_word))
            last_line.append(rhyme_word)

            return last_line

    def generate_matching_line(self, pattern, last_word, num_tries=10, restricted=set()):
        '''
        Generates a line that rhymes with given word and matches the given
        cadence pattern

        This is much less reliable than either generate_stress_line or 
        generate_rhyming_line, and will return None relatively frequently.

        To increase the reliability, the rhyme does not have to match
        the ending cadence.
        '''

        # Copy the pattern and perform operations on the copy
        pattern_copy = pattern[:]

        for _ in range(num_tries):

            # Get a valid rhyme
            rhyme_word = self.rhyme(last_word, restricted=restricted)
            if rhyme_word == None or self.nsyl(rhyme_word) > len(pattern):
                continue

            # Generate the rest of the line
            last_line = self.generate_stress_line(pattern_copy[:-self.nsyl(rhyme_word)])
            last_line.append(rhyme_word)

            # generate_stress_line may return a line that cut off before finishing
            # which results in a None at the end of the list
            if None in last_line:
                return None
            else:
                return last_line

    def generate_multi_line(self, pattern, last_word, num_lines):
        '''
        Generates the specified number of matching lines

        Note that this might take a long time, especially with many lines
        '''

        # Check if last_word has enough rhymes
        if self.rhyme(last_word, min_rhymes=num_lines) is None:
            return None

        lines = []

        restricted_rhymes = set()

        for line in range(num_lines):

            line_to_add = self.generate_matching_line(pattern, last_word, 
                restricted=restricted_rhymes)

            # Need valid line to add
            while line_to_add is None:
                line_to_add = self.generate_matching_line(pattern, last_word, 
                    restricted=restricted_rhymes)

            restricted_rhymes.update([line_to_add[-1]])

            lines.append(line_to_add)

        return lines


    ##############
    ### Poetry ###
    ##############

    def compose_love_poem(self):
        '''
        Generates a love poem, with the first two lines being 
        
        Roses are red,
        Violets are...
        ...
        ...

        and following the ABCB rhyme scheme.

        Note that the last line may return None, in the event that
        a rhyming line cannot be generated with such a short cadence
        '''

        poem = [None] * 4

        poem[0] = ['Roses', 'are', 'red']
        poem[1] = ['Violets', 'are']

        rhyme_word = random.choice(list(self.rhyme_dict.keys()))
        poem[1] += [rhyme_word]

        primary_cad = self.cadence(' '.join(poem[0]))

        poem[2] = self.generate_stress_line(primary_cad)

        secondary_cad = '1**' + self.stress(rhyme_word)

        poem[3] = self.generate_matching_line(secondary_cad, rhyme_word, 
            restricted=set([rhyme_word]))

        return poem


    def compose_haiku(self):
        '''
        Generates a haiku, a three-line poem with the first and 
        third lines having five syllables each, and the second
        line having seven syllables.
        '''

        lines = [None] * 3

        lines[0] = self.generate_line(5)
        lines[1] = self.generate_line(7)
        lines[2] = self.generate_line(5)

        return lines

    def compose_doublet(self):
        '''
        Generates a doublet, a pair of rhyming lines that have the 
        same cadence, each with 8 syllables
        '''
        lines = [None] * 2
        lines[0] = self.generate_line(10)

        # Last word needs valid rhymes
        while self.rhyme(lines[0][-1]) is None:
            lines[0] = self.generate_line(8)

        cadence = self.cadence(' '.join(lines[0]))

        # Generate a line matching the first line
        lines[1] = self.generate_matching_line(cadence, lines[0][-1])

        return lines

    def compose_limerick(self):
        '''
        Generates a limerick.

        The first, second, and fifth lines follow the cadence
        *1**1**1

        The third and fourth lines follow the cadence
        *1**1

        The poem has a AABBA rhyme scheme.
        '''

        # Set the limerick cadences
        primary_cad = '*1**1**1'
        secondary_cad = '*1**1'

        lines = [None] * 5
        lines[0] = self.generate_stress_line(primary_cad)

        # Last word needs valid rhymes
        while self.rhyme(lines[0][-1], min_rhymes=2) is None:
            lines[0] = self.generate_stress_line(primary_cad)

        # Should not repeat rhymes
        restricted_rhymes = set([lines[0][-1]])

        lines[1] = self.generate_matching_line(primary_cad, lines[0][-1], 
            restricted=restricted_rhymes)

        # Add the last word to restricted rhymes
        restricted_rhymes.update([lines[1][-1]])

        lines[4] = self.generate_matching_line(primary_cad, lines[0][-1], 
            restricted=restricted_rhymes)

        restricted_rhymes.update([lines[4][-1]])

        lines[2] = self.generate_stress_line(secondary_cad)

        while self.rhyme(lines[2][-1]) is None:
            lines[2] = self.generate_stress_line(secondary_cad)

        restricted_rhymes.update([lines[2][-1]])

        lines[3] = self.generate_matching_line(secondary_cad, lines[2][-1], 
            restricted=restricted_rhymes)

        return lines

    def compose_sonnet(self):
        '''
        Generates a sonnet in the style of Shakespeare

        Each line follows iambic pentameter with the cadence
        *1*1*1*1*1

        The poem has a ABAB CDCD EFEF GG rhyme scheme.
        '''

        # Set the iambic pentameter cadence
        cadence = '*1*1*1*1*1'

        # Initialize restricted rhymes
        restricted_rhymes = set()

        # Need 7 doublets matching cadence
        doublets = []
        for _ in range(7):

            first_line = self.generate_stress_line(cadence)

            # Need valid rhyme
            while self.rhyme(first_line[-1]) is None:
                first_line = self.generate_stress_line(cadence)

            second_line = self.generate_matching_line(cadence, first_line[-1])

            while second_line is None:
                second_line = self.generate_matching_line(cadence, first_line[-1])

            doublets += [[first_line, second_line]]

        lines = [None] * 14

        # Group in quadruplets
        for i in range(3):
            lines[4*i] = doublets[2*i][0]
            lines[4*i + 1] = doublets[2*i + 1][0]
            lines[4*i + 2] = doublets[2*i][1]
            lines[4*i + 3] = doublets[2*i + 1][1]

        # Add the last two rhyming lines
        lines[-1] = doublets[-1][0]
        lines[-2] = doublets[-1][1]

        return lines

    def compose_quatrain(self):
        '''
        Composes an alternating quatrain in iambic tetrameter,
        in the style of Robert Frost.

        Each line in the poem has the cadence
        *1*1*1*1

        The poem has AABA rhyme scheme.
        '''

        lines = [None] * 4

        cadence = '*1*1*1*1'

        restricted_rhymes = set()

        # Generate first triplet
        lines[0] = self.generate_stress_line(cadence)

        while self.rhyme(lines[0][-1], min_rhymes=2) is None:
            lines[0] = self.generate_stress_line(cadence)

        restricted_rhymes.update([lines[0][-1]])

        doublet = self.generate_multi_line(cadence, lines[0][-1], 2)

        lines[1] = doublet[0]
        lines[3] = doublet[1]

        # Generate the intermediate line
        lines[2] = self.generate_stress_line(cadence)

        return lines

    def compose_villanelle(self):
        '''
        Composes a villanelle with matching cadence,
        and a rhyme scheme of 
        A1 b A2 / a b A1 / a b A2
        a b A1 / a b A2 / a b A1 A2
        '''

        lines = [None] * 19

        # Generate first line 
        lines[0] = self.generate_line(8)

        # Need valid rhymes
        while self.rhyme(lines[0][-1], min_rhymes=6) is None:
            lines[0] = self.generate_line(8)

        primary_cad = self.cadence(' '.join(lines[0]))

        sextet = self.generate_multi_line(primary_cad, lines[0][-1], 6)

        # Generate secondary lines
        lines[1] = self.generate_line(8)

        # Need valid rhymes
        while self.rhyme(lines[1][-1], min_rhymes=5) is None:
            lines[1] = self.generate_line(8)

        secondary_cad = self.cadence(' '.join(lines[1]))

        quintet = self.generate_multi_line(secondary_cad, lines[1][-1], 5)

        # Compose the villanelle
        # Hard coded because there is not a recognizable pattern here
        lines[2] = sextet[0]

        lines[3] = sextet[1]
        lines[4] = quintet[0]
        lines[5] = lines[0]

        lines[6] = sextet[2]
        lines[7] = quintet[1]
        lines[8] = sextet[0]

        lines[9] = sextet[3]
        lines[10] = quintet[2]
        lines[11] = lines[0]

        lines[12] = sextet[4]
        lines[13] = quintet[3]
        lines[14] = sextet[0]

        lines[15] = sextet[5]
        lines[16] = quintet[4]
        lines[17] = lines[0]
        lines[18] = sextet[0]

        return lines

    def compose_ballade(self):
        '''
        Composes a ballade, a long-form poem, but truncated to
        one stanza and one envoy. The rhyme scheme is 
        ababbcbC / bcbC, where C is the refrain.
        '''

        a_rhymes = [None] * 2

        # Create a line with a rhyme-able word
        a_rhymes[0] = self.generate_line(8)

        while self.rhyme(a_rhymes[0][-1]) is None:
            a_rhymes[0] = self.generate_line(8)

        a_cadence = self.cadence(' '.join(a_rhymes[0]))

        a_rhymes[1] = self.generate_matching_line(a_cadence, a_rhymes[0][-1])

        while a_rhymes[1] is None:
             a_rhymes[1] = self.generate_matching_line(a_cadence, a_rhymes[0][-1])

        b_rhymes = [None] * 6

        b_rhymes[0] = self.generate_line(8)

        # b needs 6 total lines, so 5 rhymes total
        while self.rhyme(b_rhymes[0][-1], min_rhymes=5) is None:
            b_rhymes[0] = self.generate_line(8)

        b_cadence = self.cadence(' '.join(b_rhymes[0]))

        b_rhymes[1:] = self.generate_multi_line(b_cadence, b_rhymes[0][-1], 5)

        c_rhymes = [None] * 2

        c_rhymes[0] = self.generate_line(8)

        while self.rhyme(c_rhymes[0][-1], min_rhymes=2) is None:
            c_rhymes[0] = self.generate_line(8)

        c_cadence = self.cadence(' '.join(c_rhymes[0]))

        c_rhymes[1:] = self.generate_multi_line(c_cadence, c_rhymes[0][-1], 2)

        while None in c_rhymes:
            c_rhymes[1:] = self.generate_multi_line(c_cadence, c_rhymes[0][-1], 2)

        poem = [None] * 12

        poem[0] = a_rhymes[0]
        poem[1] = b_rhymes[0]
        poem[2] = a_rhymes[1]
        poem[3] = b_rhymes[1]
        poem[4] = b_rhymes[2]
        poem[5] = c_rhymes[0]
        poem[6] = b_rhymes[3]
        poem[7] = c_rhymes[1]

        poem[8] = b_rhymes[4]
        poem[9] = c_rhymes[2]
        poem[10] = b_rhymes[5]
        poem[11] = c_rhymes[1]

        return poem

if __name__ == '__main__':
    poet = Poet()
    poet.print_random()