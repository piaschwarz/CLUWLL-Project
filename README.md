# CLUWLL-Project

CURRENT PROBLEMS
- quality of lemmatizer not so good: some context sentences might be incorrect due to incorrect lemma
- quality of lemmatizer not so good: list of unique lemmas that don't have enough context sentences is around 500
					> workaround: preprocess obensubtitles corpus to find more context sentences
					> manual workaround: manually find context sentences in tatoeba browser interface

- wrong translation of sentences -> 3 different Italian sentences are translated with the same German sentence,
	see also: https://tatoeba.org/eng/sentences/search?from=ita&to=deu&query=Non+%C3%A8+stato+Tom+che+ha+scaricato+della+spazzatura
	example:

LEMMA: scaricare
ITA-ID=3102946
ITA-N: Non è stato Tom che ha scaricato della spazzatura nel tuo giardino.
ITA-L: non essere essere|stare Tom che avere scaricare del spazzatura nel tuo giardino .
GER-ID=1907164
GER-N: Es war nicht Tom derjenige, der Müll in unserem Vorgarten abgeladen hat.

ITA-ID=3102947
ITA-N: Non è stato Tom che ha scaricato della spazzatura nel suo giardino.
ITA-L: non essere essere|stare Tom che avere scaricare del spazzatura nel suo giardino .
GER-ID=1907164
GER-N: Es war nicht Tom derjenige, der Müll in unserem Vorgarten abgeladen hat.

ITA-ID=3102945
ITA-N: Non è stato Tom che ha scaricato della spazzatura nel vostro giardino.
ITA-L: non essere essere|stare Tom che avere scaricare del spazzatura nel vostro giardino .
GER-ID=1907164
GER-N: Es war nicht Tom derjenige, der Müll in unserem Vorgarten abgeladen hat.



PROJECT STEPS
- have useful context sentences for all Italian B1 and B2 lemmas available

- get translation of context sentences and word alignment

- populate SQL database 
- think of useful formats for these tables:
- context sentences per lemma (and some sort of translation mapping?)
- vocab piles: Bootstrap pile (A1/A2 words with translation)
- All learned words (vocab the user has encountered anywhere in the app
- Most difficult words (n most difficult words for user)
- Most frequent Italian words (n most freq. words from the pile of all learned words)

- think of architecture for frontend and backend (data structures + user interface)

- implement Java Servlets + Angular App




|Workpackage<br>March 4, 2020|Description|Responsible|Related Git Files|Comment|
|---|---|---|---|---|
|3. provide unique lemma list & find frequency information|<ul><li>clean up the Italian unique lemma list</li><li>find out where we can get frequency information from (OpenSubtitles Corpus? Didn't Dellert want to provide us with something?)</li></ul>|Marta| | |
|3. retrieve useful context sentences|<ul><li>select sentences that have at least 3 context words (incl. the queried word)</li><li>pseudo code how to include content word frequency information and maybe rank the potential context sentences</li></ul>|Pia| | |



|Workpackage<br>Feb 22nd, 2020|Description|Responsible|Related Git Files|Comment|
|---|---|---|---|---|
|1. collect texts|50-100 texts in B1/B2 Italian (DONE)|Marta|<ul><li>dir B1</li><li>dir B2</li></ul>| |
|2. retrieve context sentences - unique words|<ul><li>lemmatize all texts (DONE)</li><li>collect all unique words form all lemmatized texts (DONE)</li><li>kick out all stop words (extra list) (DONE)</li><li>retrieve all capitalized words & check if they are proper names and kick them out (extra list) (PARTLY DONE)</ul>|Marta|<ul><li>dir B1</li><li>dir B2</li><li>code_preprocessing -> lemmatizer.py</li></ul>| |
|2. retrieve context sentences - tatoeba retrieval and preprocessing|<ul><li>retrieve all sentences from tatoeba in IT and DE (csv files)</li><li>make 4 tsv lists (key value pairs):</li><li>ID-ItalianSentence</li><li>ID-GermanSentence</li><li>ID_GER-ID_IT</li><li>ID-ItalianLemmatizedSentence</li><li>Lemma-ContextSentences</li></ul>|Pia|<ul><li>dir preprocessing_tatoeba</li><li>code_preprocessing -> preprocess_tatoeba.py</li></ul>|done, except for generating the list Lemma-ContextSent with the real lemmas from the learner texts|

