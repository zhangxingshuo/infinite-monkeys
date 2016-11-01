# Nonsense Poetry Generator
Poetry generation using the Natural Language Toolkit and CMU Pronouncing Dictionary

"Given an infinite number of monkeys at an infinite number of typewriters working for an infinite amount of time, one will eventually produce a work worthy of Shakespeare"

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

## Benchmarks
Different poetry formats have varying runtimes, depending on the complexity of the poem. For instance, haikus are simple to generate, as they only depend on syllable counts, whereas limericks are much harder, as they require rhyming, cadence, and syllable counts. 
