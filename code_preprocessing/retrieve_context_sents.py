"""
Script to retrieve useful context sentences. A sentence is considered of good quality if
it contains at least two content words (low frequency words) additionally to the lemma.
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
from collections import defaultdict
import ast
from preprocess_tatoeba import dict_to_csv

def get_subtlex_content_word_freqs(subtlex_it_file):
    """ Retrieves the absolute frequencies of the dominant lemma form of a type from the file subtlex-it.csv
        Only considers content words, meaning verbs, adjectives and nouns
        :arg
            subtlex_it_file: path to subtlex-it.csv from http://crr.ugent.be/subtlex-it/
        :returns
            freqs: dict that contains the lemmas and their absolute frequencies of the dominant lemma form of a type
    """
    freqs = dict()
    with open(subtlex_it_file) as f:
        csv_reader = csv.reader(f, delimiter=",")
        f.readline()  # skip header line
        for row in csv_reader:
            dom_pos = row[4]
            dom_lemma = row[5]
            dom_lemma_freq = row[6]
            if dom_pos == "VER" or "ADJ" or "NOM":
                freqs[dom_lemma] = dom_lemma_freq

    return freqs


def load_file_as_dict(file, delimiter='\t'):
    """ Reads file and turns it into a dictionary with the first field being the keys and the second field being the values
        :arg
            file: path to file containing at least two fields
            delimiter: delimiter used in the file, default is tab
        :returns
            file_as_dict: dictionary with the first field being the keys and the second field being the values
    """
    file_as_dict = dict()
    with open(file) as f:
        csv_reader = csv.reader(f, delimiter=delimiter)
        for row in csv_reader:
            key = row[0]
            value = row[1]
            file_as_dict[key] = value

    return file_as_dict



if __name__ == '__main__':


    lemma_freqs = get_subtlex_content_word_freqs("/home/pia/Schreibtisch/CLUWLL-Project/subtlex-it.csv")
    lemma_freqs = {k: int(v) for k, v in lemma_freqs.items()}

    context_sents_lists = load_file_as_dict("/home/pia/Schreibtisch/CLUWLL-Project/preprocessing_tatoeba/context_sentences_B1B2.csv")
    context_sents_lists = {k: ast.literal_eval(v) for k, v in context_sents_lists.items()}

    selected_sentences_lemma_ita = load_file_as_dict("/home/pia/Schreibtisch/CLUWLL-Project/preprocessing_tatoeba/selected_sentences_lemma_ita.csv")
    selected_sentences_lemma_ita = {int(k): v for k, v in selected_sentences_lemma_ita.items()}

    """
    lemma_context_useful = defaultdict(list)  # creates a dict with a list as the value

    for key_lemma in context_sents_lists.keys():
        print("\n--------------------------- LEMMA = " + key_lemma + "----------------------------------------------------------------------------------------")
        #print("lemma: ", key_lemma, " - IDs before: ", context_sents_lists[key_lemma])
        rankings = []  # collects the tuples (ID, average_content_word_frequency)

        for id in context_sents_lists[key_lemma]:
            lemmatized_sent = selected_sentences_lemma_ita[id]
            content_word_counter = 0  # counts the amount of low frequency
            # content words in the lemmatized sentence
            content_word_freq = 0     # sums up the absolute frequency of all low frequency content words in the lemmatized sentence

            for word in lemmatized_sent.split():
                if word != key_lemma:  # ignore the lemma which is the key of the ID dict
                    # check if lemma is in the frequency dict and has a frequency low enough to count as a "low frequency content word"
                    if lemma_freqs.get(word) != None and lemma_freqs[word] <= 204981:  # maybe it is necessary to change this threshold
                        content_word_counter += 1
                        content_word_freq += lemma_freqs[word]

            if content_word_counter >= 2:
                print("sentence: ", lemmatized_sent, " -- content word amount: ", content_word_counter)
            # calculate average freq and add tuple (ID, average_freq) to ranking list
            if content_word_counter >= 2:
                average_freq = int(content_word_freq/content_word_counter)
                tup = (id, average_freq)
                rankings.append(tup)

        # sort the ranking list by the second tuple item: average_freq
        rankings.sort(key=lambda x: x[1])
        # make a pure ID list out of the tuple list
        sorted_list = []

        for t in rankings:
            sorted_list.append(t[0])

        # add the sorted list to dict lemma_context_useful with key=lemma, value=sorted list
        lemma_context_useful[key_lemma] = sorted_list
        #print("lemma: ", key_lemma, " - IDs after: ", lemma_context_useful[key_lemma])

    #dict_to_csv(lemma_context_useful, "/home/pia/Schreibtisch/CLUWLL-Project/preprocessing_tatoeba/context_sentences_B1B2_quality.csv")



    # converts dictionary to csv file - USE TO TEST FOR LEMMAS THAT HAVE FEWER THAN X CONTEXT SENTENCES
    out_file = "/home/pia/Schreibtisch/CLUWLL-Project/preprocessing_tatoeba/B1B2_lemmas_with_less_than_3_context_sentences_quality.csv"
    dictionary = lemma_context_useful
    with open(out_file, 'wt') as fo:
        csv_writer = csv.writer(fo, delimiter='\t')
        for lemma, sent_list in dictionary.items():
            if len(sent_list) < 3:
                csv_writer.writerow([lemma, sent_list])
    print("finished writing to file: ", out_file)
    """


    selected_sentences_ita = load_file_as_dict("/home/pia/Schreibtisch/CLUWLL-Project/preprocessing_tatoeba/selected_sentences_ita.csv")
    selected_sentences_ita = {int(k): v for k, v in selected_sentences_ita.items()}

    selected_sentences_deu = load_file_as_dict("/home/pia/Schreibtisch/CLUWLL-Project/preprocessing_tatoeba/selected_sentences_deu.csv")
    selected_sentences_deu = {int(k): v for k, v in selected_sentences_deu.items()}

    links_ita_deu = load_file_as_dict("/home/pia/Schreibtisch/CLUWLL-Project/preprocessing_tatoeba/links_ita_deu.csv")
    links_ita_deu = {int(k): int(v) for k, v in links_ita_deu.items()}

    quality_sents = load_file_as_dict("/home/pia/Schreibtisch/CLUWLL-Project/preprocessing_tatoeba/context_sentences_B1B2_quality.csv")
    quality_sents = {k: ast.literal_eval(v) for k, v in quality_sents.items()}

    with open("/home/pia/Schreibtisch/CLUWLL-Project/preprocessing_tatoeba/context_sentences_B1B2_quality_full.txt", 'wt') as f:
        for lemma, sent_list in quality_sents.items():
            f.write("___ LEMMA: " + lemma + " ____________________________________________________________________________________________\n")
            for i in sent_list:
                s = selected_sentences_ita[i]
                s_l = selected_sentences_lemma_ita[i]
                german_id = links_ita_deu[i]
                s_g = selected_sentences_deu[german_id]
                f.write("[ITA-ID=" + str(i) + "]\n")
                f.write("[ITA-N]: " + s + "\n")
                f.write("[ITA-L]: " + s_l + "\n")
                f.write("[GER-ID=" + str(german_id) + "]\n")
                f.write("[GER-N]: " + s_g + "\n")
                f.write("---------------------------------------------------------------------------------------------------------------\n")
            f.writelines("\n\n")




