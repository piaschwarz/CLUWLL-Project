"""
Script to preprocess sentences from Tatoeba.org
Uses the two csv files sentences.csv and links.csv, both downloadable here: https://tatoeba.org/eng/downloads
Author: Pia Schwarz
"""

import csv
import pprint
import treetaggerwrapper
from collections import defaultdict
import re


def get_sentences(sentence_file):
    """ Retrieves all sentences with an Italian or German ISO code to two separate dictionaries.
        :arg
            sentence_file: path to sentences.csv from https://tatoeba.org/eng/downloads
        :returns
            two dicts: sentences_ita contains all Italian ID - sentence paris
                       sentences_deu contains all German ID - sentence pairs
    """
    count_ita, count_deu = 0, 0
    sentences_ita = dict()
    sentences_deu = dict()
    with open(sentence_file) as fs:
        csv_reader = csv.reader(fs, delimiter="\t")
        for row in csv_reader:
            if row[1] == "ita":
                sentences_ita[row[0]] = row[2]
                count_ita += 1
            if row[1] == "deu":
                sentences_deu[row[0]] = row[2]
                count_deu += 1
    print("Amount of sentences in Italian: ", count_ita, "  ---  Amount of sentences in German: ", count_deu)
    return sentences_ita, sentences_deu


# converts dictionary to csv file
def dict_to_csv(dictionary, out_file):
    """ Converts a dictionary to csv file.
        :arg
            dictionary: the dict to convert
            out_file: file path
    """
    with open(out_file, 'wt') as fo:
        csv_writer = csv.writer(fo, delimiter='\t')
        for id, sent in dictionary.items():
            csv_writer.writerow([id, sent])
    print("finished writing to file: ", out_file)


def get_links(links_file, dict_sents_ita, dict_sents_deu):
    """ Retrieves all IDs of sentences that have a corresponding translation.
        :arg
            links_file: path to links.csv from https://tatoeba.org/eng/downloads
            dict_sents_ita: dict of Italian ID - sentence pairs
            dict_sents_deu: dict of German ID - sentence pairs
        :returns
            links_ita_deu: dict that contains pairs of corresponding {Italian sentence ID - German sentence ID}
    """
    count = 0
    links_ita_deu = dict()
    with open(links_file) as fl:
        csv_reader = csv.reader(fl, delimiter="\t")
        for row in csv_reader:
            # if it is an Italian sentence that has a German translation
            if row[0] in dict_sents_ita.keys() and row[1] in dict_sents_deu.keys():
                links_ita_deu[row[0]] = row[1]
                count += 1

    print("Amount of sentences in Italian with German translation: ", count)
    return links_ita_deu


def lemmatize(sentence, tagger):
    """ Lemmatizes a single Italian sentence string and returns it as a string.
        :arg
            sentence: sentence to lemmatize
            tagger: TreeTagger object (for more information see: https://treetaggerwrapper.readthedocs.io/en/latest/)
        :returns
            the lemmatized sentece
    """
    tags = tagger.tag_text(sentence)
    tag_lemmas = []
    for t in tags:
        if '\t' not in t:  # that can happen with a URL occurrence like in the sentence: "Ho ordinato un libro da Amazon.com."
            tag_lemmas.append("<placeholder>")  # there are only two URL occurrences so this can be "repaired" manually in the csv file
            continue
        else:
            tag_lemmas.append(t[t.rindex('\t') + 1:])

    return " ".join(tag_lemmas)


def find_only_whole_word(search_string, input_string):
    """ tests for a full word match in a sentence
        :arg
            search_string: string to test for
            input_string: sentence where search_string is searched
        :returns
            True: if the search_string was found in the input_string
            False: if the search_string was not found in the input_string
    """
    raw_search_string = r"\b" + search_string + r"\b"  # create a raw string with word boundaries
    match_output = re.search(raw_search_string, input_string)
    no_match_was_found = (match_output is None)
    if no_match_was_found:
        return False
    else:
        return True



if __name__ == '__main__':

    # build a treetagger wrapper
    tagger = treetaggerwrapper.TreeTagger(TAGLANG='it', TAGDIR='/home/pia/Downloads')


    # retrieve two dicts: {ID: italian_sentence} and {ID: german_sentence}
    all_sents_ita, all_sents_deu = get_sentences("/home/pia/Schreibtisch/CLUWLL-Project/preprocessing_tatoeba/sentences.csv")

    #dict_to_csv(all_sents_ita, "/home/pia/Schreibtisch/CLUWLL-Project/preprocessing_tatoeba/all_sentences_ita.csv")
    #dict_to_csv(all_sents_deu, "/home/pia/Schreibtisch/CLUWLL-Project/preprocessing_tatoeba/all_sentences_deu.csv")


    # retrieve a dict that contains the ID of the Italian sentence and
    # the corresponding ID of the translated sentence in German
    translation_links = get_links("/home/pia/Schreibtisch/CLUWLL-Project/preprocessing_tatoeba/links.csv", all_sents_ita, all_sents_deu)

    #dict_to_csv(translation_links, "/home/pia/Schreibtisch/CLUWLL-Project/preprocessing_tatoeba/links_ita_deu.csv")


    # create new dict of all_sents_ita that contains only the items that have a corresponding German translation
    selected_sents_ita = dict()
    # create a corresponding italian lemmatized dict
    selected_sents_ita_lemma = dict()
    # create new dict of all_sents_deu that contains only the items that have a corresponding Italian translation
    selected_sents_deu = dict()

    for ID_ita, ID_deu in translation_links.items():
        selected_sents_ita[ID_ita] = all_sents_ita[ID_ita]
        selected_sents_deu[ID_deu] = all_sents_deu[ID_deu]

    # write dict of selected sentences to csv files (Italian and German)
    #dict_to_csv(selected_sents_ita, "/home/pia/Schreibtisch/CLUWLL-Project/preprocessing_tatoeba/selected_sentences_ita.csv")
    #dict_to_csv(selected_sents_deu, "/home/pia/Schreibtisch/CLUWLL-Project/preprocessing_tatoeba/selected_sentences_deu.csv")
    


    # lemmatize the file selected_sentences_ita.csv and write result to selected_sentences_lemma_ita.csv
    # read from file (and not from existing dict) as there were some manual changes:
    selected_sents_ita_lemma = dict()
    with open("/home/pia/Schreibtisch/CLUWLL-Project/preprocessing_tatoeba/selected_sentences_ita.csv") as ita_file:
        csv_reader = csv.reader(ita_file, delimiter="\t")
        for row in csv_reader:
            ID = row[0]
            sent = row[1]
            sent_lemma = lemmatize(sent, tagger)
            selected_sents_ita_lemma[ID] = sent_lemma

    #dict_to_csv(selected_sents_ita_lemma, "/home/pia/Schreibtisch/CLUWLL-Project/preprocessing_tatoeba/selected_sentences_lemma_ita.csv")



    # load unique lemmatized word list (generated by Marta from 50-100 texts) and create a dict with the format:
    # {lemma: [sent_ID1, sent_ID2, sent_ID3, ...]}
    lemma_context = defaultdict(list)  # creates a dict with a list as the value
    with open("/home/pia/Schreibtisch/CLUWLL-Project/B1B2_lemmas_final_SET.txt") as lemma_file:
        csv_reader = csv.reader(lemma_file, delimiter="\t")
        for row in csv_reader:
            unique_lemma = row[0]
            found = False
            for id_sent, sent_lemmatized in selected_sents_ita_lemma.items():
                if find_only_whole_word(unique_lemma, sent_lemmatized):
                    lemma_context[unique_lemma].append(int(id_sent))
                    found = True
            if not found:
                lemma_context[unique_lemma] = []

    dict_to_csv(lemma_context, "/home/pia/Schreibtisch/CLUWLL-Project/preprocessing_tatoeba/" +
                               "final_output_context_sents/final_context_sentences_B1B2.csv")



    # converts dictionary to csv file - USE TO TEST FOR LEMMAS THAT HAVE FEWER THAN X CONTEXT SENTENCES
    out_file = "/home/pia/Schreibtisch/CLUWLL-Project/preprocessing_tatoeba/" +\
               "final_output_context_sents/final_B1B2_lemmas_with_less_than_3_context_sentences.csv"
    dictionary = lemma_context
    with open(out_file, 'wt') as fo:
        csv_writer = csv.writer(fo, delimiter='\t')
        for lemma, sent_list in dictionary.items():
            if len(sent_list) < 3:
                csv_writer.writerow([lemma, sent_list])
    print("finished writing to file: ", out_file)

