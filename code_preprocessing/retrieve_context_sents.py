"""
Script to retrieve useful context sentences. A sentence is considered of good quality if
the it contains at least two content words (low frequency words) additionally to the lemma.
Then they are ranked, where sentences with the least frequent content words are ranked before
sentences with more frequent content words.

1. Collect only the sentences that contain enough content words. A word is considered a low freq. word
   if its normalized freq. count is below a certain threshold (tbd)
   The frequency of a word needs to be extracted from a corpus like OpenSubtitles.org - a csv/tsv file with
   the following format needs to be present:
    ----------------------------------
    lemma1  normalized_frequency_count
    lemma2  normalized_frequency_count
    ...
    ----------------------------------

2. rank according to the average frequency of all content words in a sentence.
   Example:
    lemma = mangiare
    [Sent_deu = "Wir werden heute Abend viel essen, daher hoffe ich, dass du nicht auf Diät bist"]
    Sent_ita = "Mangeremo molto stasera e quindi spero che tu non sia a dieta."
    Frequencies:  0.04             0.05          0.003                  0.00008
                (assuming only the freq. counts of these words are below the threshold mentioned above)
                --> Average_freq = (0.04 + 0.05 + 0.003 + 0.00008) / 3

The following files are used:
- context_sentences.csv (lists all Italian lemmas and a list of sentence IDs that contain this word (non-lemmatized) --> AVAILABLE
- frequencies.csv (lists all words (lemmatized) and their normalized frequency count from a huge corpus like OpenSubtitles --> TO DO

Author: Pia Schwarz
"""

import csv
import pprint
from collections import defaultdict