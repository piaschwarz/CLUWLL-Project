"""
Script to process a corpus file (like OpenSubtitles or similar) to retrieve normalized word frequency counts

The output is a csv/tsv file with the following format:
    ----------------------------------
    lemma1  normalized_frequency_count
    lemma2  normalized_frequency_count
    ...
    ----------------------------------

The following files are used:
- ...

Author: Pia Schwarz
"""

import csv
import pprint
from collections import defaultdict