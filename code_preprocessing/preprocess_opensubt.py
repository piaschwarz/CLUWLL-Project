"""
Script to preprocess sentences from http://opus.nlpl.eu/OpenSubtitles-v2018.php
This is necessary as we don't have enough quality context sentences from tatoeba only
Uses the tmx.gz file de-it.tmx.gz from OpenSubtitles (link see above)
Author: Pia Schwarz
"""

import csv
import pprint
from collections import defaultdict
import re
from translate.storage.tmx import tmxfile
import gzip
import io
from preprocess_tatoeba import find_only_whole_word, dict_to_csv
import ast

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


def get_subtlex_content_word_freqs(subtlex_it_file):
    """ Retrieves the absolute frequencies of the dominant lemma form of a type from the file subtlex-it.csv
        Only considers content words, meaning nouns, verbs, adjectives and adverbs
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
            if dom_pos == "VER" or "ADJ" or "NOM" or "ADV":
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


    ####################################################################################################################
    # USE THIS BLOCK TO PREPROCESS THE RAW tmx-files AND CREATE THIS FILE: ID \t italianSent \t germanSent

    opensub_it_de = dict()
    ID = 9000000  # the starting ID - this was chosen as all sentence IDs from tatoeba do NOT exceed 9,000,000
                  # this way opensubtitle senences are identifiable by an ID <= 9,000,000
    in_path = "/home/pia/cluwll/de-it.tmx"
    with open(in_path, 'rb') as fin:
        tmx_file = tmxfile(fin, 'de', 'it')
    for node in tmx_file.unit_iter():
        opensub_it_de[ID] = [node.gettarget(), node.getsource()]
        ID += 1
    print(len(opensub_it_de))
    print("done reading tmx - dict was generated")


    out_path = "/home/pia/cluwll/opensubt_id_it_de.txt"
    with open(out_path, 'wt') as fo:
        csv_writer = csv.writer(fo, delimiter='\t')
        for id, sent in opensub_it_de.items():
            csv_writer.writerow([id, sent[0], sent[1]])
    print("finished writing to file: ", out_path)
    ####################################################################################################################



    ####################################################################################################################
    # USE THIS BLOCK TO EXTRACT SENTENCES THAT CONTAIN A LEMMA WHICH DOES NOT HAVE ENOUGH QUALITY CONTEXT SENTS
    # FROM TATOEBA (around 900 lemmas) - THE UNLEMMATIZED SENTENCES FROM OPENSUBT ARE USED

    # read in opensubt_id_it_de.txt as two dictionaries: ID - italianSentenc and ID - germanSentence
    openSubt_sents_ita = dict()
    openSubt_sents_deu = dict()
    with open("/home/pia/cluwll/opensubt_id_it_de.txt") as f:
        csv_reader = csv.reader(f, delimiter="\t")
        for row in csv_reader:
            key = int(row[0])
            value_ita = row[1]
            value_deu = row[2]
            openSubt_sents_ita[key] = value_ita
            openSubt_sents_deu[key] = value_deu

    print("read in german and italian dicts")


    lemmas = []  # all lemmas that do not have enough quality context sents from tatoeba only (around 900 lemmas)
    context_sents_from_openSubt = defaultdict(list)
    with open("lemmas_for_opensubt.tsv") as f:
        csv_reader = csv.reader(f, delimiter='\t')
        for row in csv_reader:
            lemma = row[0]
            lemmas.append(lemma)
            context_sents_from_openSubt[lemma] = list()

    print("read in ", len(lemmas), " lemmas that lack quality context sentences")


    # iterate all sentences of openSubt_sents_ita and see if they contain one of the lemmas -> if yes: add to new dict
    for id, sent_ita in openSubt_sents_ita.items():
        if id > 10500000:
            break
        print("processing sentence ID ", id)
        for l in lemmas:
            if find_only_whole_word(l, sent_ita):
                context_sents_from_openSubt[l].append(int(id))

    dict_to_csv(context_sents_from_openSubt, "openSubt_context_sents_of_lemmas_where_tatoeba_cant_provide_enough_quality-1point5mio.txt")
    ####################################################################################################################



    ####################################################################################################################
    # USE THIS BLOCK TO GET QUALITY CONTEXT SENTENCES FOR THE TARGET WORDS: MISSING CONTEXT SENTENCES
    # (as tatoeba cannot provide engough)

    # retrieve absolute content word frequencies from the subtlex-it corpus and store them into dict:
    # key = lemma, value = frequency
    lemma_freqs = get_subtlex_content_word_freqs("/home/pia/cluwll/subtlex-it.csv")
    lemma_freqs = {k: int(v) for k, v in lemma_freqs.items()}  # type cast dict keys to integers

    # load the sentence lists for words from B1 and B2: key = lemma, value = sent. ID list containing this lemma
    context_sents_lists = load_file_as_dict("/home/pia/cluwll/" +
                                            "openSubt_context_sents_of_lemmas_where_tatoeba_cant_provide_enough_quality-1point5mio.txt")
    context_sents_lists = {k: ast.literal_eval(v) for k, v in
                           context_sents_lists.items()}  # make sure that dict values are evaluated as lists

    # load the lemmatized Italian sentences (called 'selected' because they have German translations available):
    # key = ID, value = lemmatized Italian sentence
    selected_sentences_lemma_ita = load_file_as_dict("/home/pia/cluwll/opensubt_sents_ita_lemma.csv")
    selected_sentences_lemma_ita = {int(k): v for k, v in
                                    selected_sentences_lemma_ita.items()}  # type cast dict keys to integers

    # read in A1-B2 Italian words (CEFR) as a list which will be used to see how many content words are of these levels
    A1toB2_words = []
    with open("/home/pia/cluwll/CEFR_A1_A2_B1_B2.tsv") as f:
        csv_reader = csv.reader(f, delimiter='\t')
        for row in csv_reader:
            A1toB2_words.append(row[0])

    # create a dict with key = lemma and value = list that will contain the IDs of the sentences that are considered
    # quality sentences (have enough content words: target word + two content words)
    lemma_context_useful = defaultdict(list)

    for key_lemma in context_sents_lists.keys():

        print("\n--------------------------- LEMMA = " + key_lemma + "-------------------------------------------")
        if not context_sents_lists[key_lemma]:  # check if the list is empty
            print("lemma: ", key_lemma, " has empty list: ", context_sents_lists[key_lemma])
            lemma_context_useful[key_lemma] = []

        rankings = []  # collects the tuples (ID, average_content_word_frequency)

        for id in context_sents_lists[key_lemma]:  # iterate through all sent. IDs assigned to the lemma
            if id not in selected_sentences_lemma_ita.keys():  #added this line
                continue
            lemmatized_sent = selected_sentences_lemma_ita[id]  # get single lemmatized sentence
            content_word_counter = 0  # counts the amount of low frequency content words in the lemmatized sentence
            content_word_freq = 0  # sums up the absolute frequency of all low frequency content words in the lemmatized sentence
            count_A1toB2 = 0

            for word in lemmatized_sent.split():
                if word != key_lemma:  # ignore the lemma which is the key of the ID dict
                    # check if lemma is in the frequency dict and has a frequency low enough to count as a "low frequency content word"
                    # the threshold of 204981 was set after manually checking the subtlex-it frequency list, it might be changed
                    if lemma_freqs.get(word) != None and lemma_freqs[word] <= 204981:  # threshold might be changed
                        content_word_counter += 1
                        content_word_freq += lemma_freqs[word]

                        # check if the content word is of level A1 to B2
                        if word in A1toB2_words:
                            count_A1toB2 += 1

            if content_word_counter >= 2:  # only consider sentences with enough content words

                # check if less than 65% of the content words are in level A1-B2 -> then mark the ID as potentially disqualified
                qualification_percentage = count_A1toB2 / content_word_counter
                if qualification_percentage >= 0.65:
                    # HOW TO MARK IT so it can be restored? convert all disqualified sentence IDs to float and leave
                    # qualified ones as integers
                    id = int(id)
                else:
                    id = float(id)

                # calculate average freq of all content words in a sentence
                average_freq = int(content_word_freq / content_word_counter)
                tup = (id, average_freq, content_word_counter)
                rankings.append(tup)

            # sort the rankings so we get the sentences with the most content words at the beginning of the list and if
            # there are sentences with the same amount of content words, sort them by their average content word frequency:
            rankings.sort(key=lambda x: x[1])  # first sort by the second tuple item: average content word frequency ...
            rankings.sort(key=lambda x: x[2],
                          reverse=True)  # ... then reverse sort by the third tuple item: amount of content word

            sorted_list = []  # make a pure ID list out of the list containing both, ID and average frequency
            for t in rankings:
                sorted_list.append(
                    t[0])  # t[0] selects only the ID from the tuples (ID, average_freq, content_word_counter)

            # add the sorted list to dict lemma_context_useful with: key = lemma, value = sorted list
            lemma_context_useful[key_lemma] = sorted_list

    print("length of dict lemma_context_useful, should be around 1160: ", len(lemma_context_useful))

    dict_to_csv(lemma_context_useful, "/home/pia/cluwll/final_context_sentences_missingLemmas_quality.csv")
    ####################################################################################################################



    ####################################################################################################################
    # USE THIS BLOCK TO PRINT THE OPEN_SUBTITLES QUALITY CONTEXT SENTENCES IN ITALIAN (LEMMATIZED & NON-LEMMATIZED)
    # ON UNI SERVER

    sents_id_ita_deu = defaultdict(list)
    with open("/home/pia/cluwll/opensubt_id_it_de.txt") as f:
        csv_reader = csv.reader(f, delimiter='\t')
        for row in csv_reader:
            key = int(row[0])
            value_ita = str(row[1])
            value_deu = str(row[2])
            sents_id_ita_deu[key] = [value_ita, value_deu]

    with open("/home/pia/cluwll/openSubt_context_sents_quality_missingLemmas_quality_full.txt", 'wt') as f:
        for lemma, sent_list in lemma_context_useful.items():
            f.write(
                "___ LEMMA: " + lemma + " ____________________________________________________________________________________________\n")
            for i in sent_list:
                s = sents_id_ita_deu[i][0]
                s_l = selected_sentences_lemma_ita[i]
                ger = sents_id_ita_deu[i][1]
                f.write("[ITA-ID=" + str(i) + "]\n")
                f.write("[ITA-N]: " + s + "\n")
                f.write("[ITA-L]: " + s_l + "\n")
                f.write("[DEU-N]: " + ger + "\n")
                f.write(
                    "---------------------------------------------------------------------------------------------------------------\n")
            f.writelines("\n\n")

    print("finished writing to file: /home/pia/cluwll/openSubt_context_sents_quality_missingLemmas_quality_full.txt")
    ####################################################################################################################

