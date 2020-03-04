# CLUWLL-Project

directories:
- propsal and project report incl. screenshots etc.
- code typescript
- code Java Servlets
- code preprocessing
- resources (tables, images, etc)
- ...?

Date: March 4, 2020
|Workpackage|Description|Responsible|Comment|
|---|---|---|---|
|3. provide unique lemma list & find frequency information|<ul><li>clean up the Italian unique lemma list</li><li>find out where we can get frequency information from (OpenSubtitles Corpus? Didn't Dellert want to provide us with something?)</li></ul>|Marta| |
|3. retrieve useful context sentences|<ul><li>select sentences that have at least 3 context words (incl. the queried word)</li><li>pseudo code how to include content word frequency information and maybe rank the potential context sentences</li></ul>|Pia| |


Date: Feb 22nd, 2020
|Workpackage|Description|Responsible|Comment|
|---|---|---|---|
|1. collect texts|50-100 texts in B1/B2 Italian (DONE)|Marta|  |
|2. retrieve context sentences - unique words|<ul><li>lemmatize all texts (DONE)</li><li>collect all unique words form all lemmatized texts (DONE)</li><li>kick out all stop words (extra list) (DONE)</li><li>retrieve all capitalized words & check if they are proper names and kick them out (extra list) (PARTLY DONE)</ul>|Marta| |
|2. retrieve context sentences - tatoeba retrieval and preprocessing|<ul><li>retrieve all sentences from tatoeba in IT and DE (csv files)</li><li>make 4 tsv lists (key value pairs):</li><li>ID-ItalianSentence</li><li>ID-GermanSentence</li><li>ID_GER-ID_IT</li><li>ID-ItalianLemmatizedSentence</li><li>Lemma-ContextSentences</li></ul>|Pia|done, except for generating the list Lemma-ContextSent with the real lemmas from the learner texts|

