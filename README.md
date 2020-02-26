# CLUWLL-Project

directories:
- propsal and project report incl. screenshots etc.
- code typescript
- code Java Servlets
- code preprocessing
- resources (tables, images, etc)
- ...?


|Workpackage|Description|Responsible|
|---|---|---|
|1. collect texts|50-100 texts in B1/B2 Italian|Marta|
|2. retrieve context sentences - unique words|<ul><li>lemmatize all texts</li><li>collect all unique words form all lemmatized texts</li><li>kick out all stop words (extra list)</li><li>retrieve all capitalized words & check if they are proper names and kick them out (extra list)</li><li>create a list of all unique words that will be used to query the retrieval from tatoeba (unique = appears at least once in the texts)</li></ul>|Marta|
|2. retrieve context sentences - tatoeba retrieval and preprocessing|<ul><li>retrieve all sentences from tatoeba in IT and DE (csv files)</li><li>make 4 lists:</li><li>ID-ItalianSentence</li><li>ID-GermanSentence</li><li>ID_GER-ID_IT</li><li>ID-ItalianLemmatizedSentence</li></ul>|Pia| 

