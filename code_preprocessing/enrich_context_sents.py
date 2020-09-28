import csv
import ast
from collections import defaultdict
from preprocess_tatoeba import dict_to_csv
from retrieve_context_sents import load_file_as_dict


def load_selected_sents_ita_for_inflection_lookup(path):
    """
        Reads a tsv file with sentence ID in the first column and the non lemmatized Italian sentence in the second
        args:
            path of inflection file
        returns:
            dictionary with the format {ID: [word1, word2, ...]}
    """
    selected_sents_ita_infl_lookup = defaultdict(list)
    with open(path) as file:
        csv_reader = csv.reader(file, delimiter="\t")
        for row in csv_reader:
            id = int(row[0])
            sent = row[1].lower()
            sent = sent.replace(".", "").replace("?", "")\
                .replace("!", "").replace(":", "").replace(",", "")  # delete all punctuation marks
            sent = sent.replace("“", "").replace("\"", "")  # delete all quotation marks
            sent = sent.replace("'", " ")  # replace apostrophe with space symbol

            for word in sent.split():
                selected_sents_ita_infl_lookup[word].append(id)

    return selected_sents_ita_infl_lookup


def load_inflections(path_inflection_file):
    """
        Reads a tsv file with lemmas in the first column and all its inflections in the following columns
        args:
            path of inflection file
        returns:
            dictionary with the format {lemma: [inflection1, inflection2, ...]}
    """
    inflections = defaultdict(list)
    with open(path_inflection_file) as file:
        csv_reader = csv.reader(file, delimiter="\t")
        for row in csv_reader:
            lemma = row[0]
            infl_list = []
            for infl in row:
                if infl != lemma and infl != "/" and infl not in infl_list:
                    infl_list.append(infl)
            inflections[lemma] = infl_list

    return inflections


def load_verb_inflections(path_inflection_file):
    """
        Reads a tsv file with lemmas in the first column and one inflection in the 5th column.
        If an inflection consists of 2 words it is reduced to the last word (avrò preoccupato --> preoccupato)
        args:
            path of inflection file with the format:
            preoccupare	Indicativo	Futuro Anteriore	1s	avrò preoccupato
            preoccupare	Indicativo	Futuro Anteriore	2s	avrai preoccupato
            ...
        returns:
            dictionary with the format {lemma: [inflection1, inflection2, ...]}
    """
    inflections = defaultdict(list)
    with open(path_inflection_file) as file:
        csv_reader = csv.reader(file, delimiter="\t")
        for row in csv_reader:
            lemma = row[0]
            full_infl = row[4].split()
            infl = full_infl[-1]
            if infl not in inflections[lemma]:
                inflections[lemma].append(infl)

    return inflections


def find_additional_context_sents(context_sents_lists, POS_inflections,  ita_infl_id_lookup):
    """
    Creates a dict with {lemma: context_sent1, context_sent2, ...} where all context sentences are possible
    additional context sentences found with inflections of the lemma in tatoeba
        :param context_sents_lists: already existing context sentence dict (before enrichment)
        :param POS_inflections: dict of lemma + inflections
        :param ita_infl_id_lookup: dict with mapping from unlemmatized word to ID (of sentence where this form occurrs)
        :return: dict of possible additional sentences for enrichment
    """
    count = 0
    context_sents_for_enrichment = defaultdict(list)
    for lemma, id_list in context_sents_lists.items():
        if lemma in POS_inflections.keys() and len(POS_inflections[lemma]) >= 1:
            inflections_of_lemma = POS_inflections[lemma]
            #print(inflections_of_lemma)
            for infl in inflections_of_lemma:
                if infl in ita_infl_id_lookup.keys():
                    ids_enrich = ita_infl_id_lookup[infl]
                    for id in ids_enrich:
                        if id not in id_list:
                            print("-------------------------------------------------------------")
                            print("Found an ID which is not already in context_sentences_B1B2_without_A1A2_CEFR.csv")
                            print("Lemma: ", lemma)
                            print("missing ID: ", id)
                            print("found through inflected word: ", infl)
                            count += 1
                            context_sents_for_enrichment[lemma].append(id)
    print("Total cases where IDs could be added: ", count)
    return context_sents_for_enrichment


if __name__ == '__main__':


    ####################################################################################################################
    # USE THIS BLOCK TO LOAD INFLECTION LISTS AND CREATE A FILE WITH NEW CONTEXT SENTENCES THAT CAN POSSIBLY BE USED
    # TO ENRICH THE CONTEXT SENTENCES FILES WITH SENTS FROM THE UNLEMMATIZED TATOEEBA (selected_sentences_ita.csv)

    # load inflection lists
    B1_adj_inflections = load_inflections("/home/pia/Schreibtisch/CLUWLL-Project/tables/B1AdjectivesInflection.tsv")
    B1_noun_inflections = load_inflections("/home/pia/Schreibtisch/CLUWLL-Project/tables/B1NounInflection.tsv")
    B1_verb_inflections = load_verb_inflections("/home/pia/Schreibtisch/CLUWLL-Project/tables/B1VerbInflection.tsv")


    ita_infl_id_lookup = load_selected_sents_ita_for_inflection_lookup(
        "/home/pia/Schreibtisch/CLUWLL-Project/preprocessing_tatoeba/selected_sentences_ita.csv")

    # load the sentence lists for words from B1 and B2: key = lemma, value = sent. ID list containing this lemma
    context_sents_lists = load_file_as_dict("/home/pia/Schreibtisch/CLUWLL-Project/preprocessing_tatoeba/" +
                                            "output_files_with_input_B1B2_lemmas_SET_without_A1A2_CEFR/" +
                                            "context_sentences_B1B2_without_A1A2_CEFR.csv")
    context_sents_lists = {k: ast.literal_eval(v) for k, v in context_sents_lists.items()}  # make sure that dict values are evaluated as lists



    additional_context_sents_nouns = find_additional_context_sents(context_sents_lists,
                                                                   B1_noun_inflections, ita_infl_id_lookup)

    dict_to_csv(additional_context_sents_nouns, "/home/pia/Schreibtisch/CLUWLL-Project/preprocessing_tatoeba/" +
                "output_files_for_enrichment_without_A1A2_CEFR/context_sents_for_enrichment_B1Nouns.tsv")

    ####################################################################################################################


    ####################################################################################################################
    # USE THIS BLOCK TO SEE HOW MANY CRITICAL SENTNECES MIGHT BE "HEALED" THROUGH THE USE OF ADDITIONAL CONTEXT SENTENCES
    # (= ENRICHMENT) -- BEWARE THAT THE QUALITY OF THESE ADDITIONAL SENTENCES MIGHT NOT BE GOOD!!!!!!!!!!!!!!!!

    # load dicts from full sentences ita and deu for later seeing the full sentences if they are useful for enrichment
    selected_sentences_ita = load_file_as_dict(
        "/home/pia/Schreibtisch/CLUWLL-Project/preprocessing_tatoeba/selected_sentences_ita.csv")
    selected_sentences_ita = {int(k): v for k, v in selected_sentences_ita.items()}

    selected_sentences_deu = load_file_as_dict(
        "/home/pia/Schreibtisch/CLUWLL-Project/preprocessing_tatoeba/selected_sentences_deu.csv")
    selected_sentences_deu = {int(k): v for k, v in selected_sentences_deu.items()}

    links_ita_deu = load_file_as_dict("/home/pia/Schreibtisch/CLUWLL-Project/preprocessing_tatoeba/links_ita_deu.csv")
    links_ita_deu = {int(k): int(v) for k, v in links_ita_deu.items()}




    context_sents_less_than_3 = load_file_as_dict("/home/pia/Schreibtisch/CLUWLL-Project/preprocessing_tatoeba/" +
                                            "output_files_with_input_B1B2_lemmas_SET_without_A1A2_CEFR/" +
                                            "B1B2_lemmas_without_A1A2_CEFR_with_less_than_3_context_sentences_quality.csv")
    context_sents_less_than_3 = {k: ast.literal_eval(v) for k, v in context_sents_less_than_3.items()}  # make sure that dict values are evaluated as lists

    add_context_sents_verbs = load_file_as_dict("/home/pia/Schreibtisch/CLUWLL-Project/preprocessing_tatoeba/"
                                                "output_files_for_enrichment_without_A1A2_CEFR/" +
                                                "context_sents_for_enrichment_B1Verbs_quality.csv")
    add_context_sents_verbs = {k: ast.literal_eval(v) for k, v in add_context_sents_verbs.items()}

    add_context_sents_nouns = load_file_as_dict("/home/pia/Schreibtisch/CLUWLL-Project/preprocessing_tatoeba/"
                                                "output_files_for_enrichment_without_A1A2_CEFR/" +
                                                "context_sents_for_enrichment_B1Nouns_quality.csv")
    add_context_sents_nouns = {k: ast.literal_eval(v) for k, v in add_context_sents_nouns.items()}

    add_context_sents_adj = load_file_as_dict("/home/pia/Schreibtisch/CLUWLL-Project/preprocessing_tatoeba/"
                                                "output_files_for_enrichment_without_A1A2_CEFR/" +
                                                "context_sents_for_enrichment_B1Adjectives_quality.csv")
    add_context_sents_adj = {k: ast.literal_eval(v) for k, v in add_context_sents_adj.items()}

    # combine verbs, nouns and adjectives
    add_context_sents = {**add_context_sents_verbs, **add_context_sents_nouns, **add_context_sents_adj}

    count = 0
    for lemma, ids in context_sents_less_than_3.items():
        missing = 3 - len(ids)
        if lemma in add_context_sents and len(add_context_sents[lemma]) != 0:
            print("--------------------------------------------------")
            print("Lemma: \"" + lemma + "\" misses ", missing, " quality context sentences.")
            print("from possible additional context sentences for enrichment this no. of sentences is available: ",
                  len(add_context_sents[lemma]))
            print(missing - len(add_context_sents[lemma]), " sentences are then still missing.")
            if missing - len(add_context_sents[lemma]) <= 0:
                count += 1
            print("The sentences that are candidates for enrichment:")
            for i in add_context_sents[lemma]:
                italian_full = selected_sentences_ita[i]
                german_id = links_ita_deu[i]
                german_full = selected_sentences_deu[german_id]
                print("++++++++++")
                print("ID: ", i)
                print(italian_full)
                print(german_full)

    print("\n\n*************************************************************************************")
    print("IN TOTAL that reduces the critical words by: ", count)




