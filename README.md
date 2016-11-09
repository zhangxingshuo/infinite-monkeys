# Nonsense Poetry Generator
Poetry generation using the Natural Language Toolkit and CMU Pronouncing Dictionary

"Given an infinite number of monkeys at an infinite number of typewriters working for an infinite amount of time, one will eventually produce a work worthy of Shakespeare"

Currently generating nonsense poetry on Twitter under Infinite Typewriters [(@infinite_poetry)](https://twitter.com/infinite_poetry).

## Usage
The poetry script provides an extensible class that allows generation of haikus, love poems, limericks, sonnets, and villanelles, with more forms of poetry planned. 

```
p = Poet()

p.print_haiku()
```

will print out a random haiku, such as 

```
A Nonsense Haiku
By Poetry Bot

Quantum dimension
Offense guardian save bring
Thank validation

Composed in 0.01 seconds
```

To utilize rhymes between words in the work, a rhyming dictionary must be compiled before running the `poetry.py` script. To compile the dictionary of rhymes, run

```
python3 -i rhyme_dict.py [filename]
```

in CLI. A `.pkl` file will be created in the same directory that contains the dictionary of rhyme sets for the input corpus.

## Benchmarks
<b>NOTE:</b> The script has now been optimized to call from a pre-compiled dictionary of rhymes and stresses. The runtimes listed below, while obsolete, are a good indication of the complexity of the poetry format. The runtimes are not nearly as long though; most poems are now created almost instantly on the given specifications.

Different poetry formats have varying runtimes, depending on the complexity of the poem. For instance, haikus are simple to generate, as they only depend on syllable counts, whereas limericks are much harder, as they require rhyming, cadence, and syllable counts. 

Tests were run on a dual-core Intel i5-5200U @ 2.2 GHz.

Poem | Average | Maximum | Minimum |
|:---:|---:|---:|---:|
Love Poem | 0.83s | 0.84s | 0.83s |
Haiku | 0.00s | 0.00s | 0.00s |
Doublet | 4.33s | 7.56s | 1.69s |
Limerick | 5.08s | 8.16s | 4.17s |
Sonnet | 20.51s | 26.87s | 12.54s | 
Quatrain | 5.75s | 10.36s | 4.08s |
Villanelle | 30.15s | 59.61s | 13.33s |
Ballade | 40.28s | 64.28s | 22.05s |

## Tweeting
The file `tweet.py` contains methods that allow for the generation of short 140-character poems by randomly selecting a poetry format and brute-forcing until the poem is below 140 characters. Note that this limitation necessarily disqualifies long-format poems such as the villanelle, ballade, and sonnet.
