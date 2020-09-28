# before saving ods file as csv: replace \n with " - " and in comment section all commas with ";"

# tatoeba path: /home/pia/Schreibtisch/CLUWLL-Project/preprocessing_tatoeba/final_output_context_sents/final_context_sentences_B1B2.csv
# opensubt path: /home/pia/Schreibtisch/CLUWLL-Project/preprocessing_opensubt/openSubt_context_sents_of_lemmas_where_tatoeba_cant_provide_enough_quality-1point5mio.txt

from preprocess_tatoeba import dict_to_csv
from preprocess_opensubt_uniserver import load_file_as_dict
import ast
import csv
import pprint
from collections import defaultdict
import re
import gzip
import io

def load_dict(file, pos_key, pos_value, delimiter='\t'):
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
            key = row[pos_key]
            value = row[pos_value]
            file_as_dict[key] = value

    return file_as_dict


if __name__ == '__main__':
    # load the sentence lists for words from B1 and B2: key = lemma, value = sent. ID list containing this lemma
    tatoeba_sents = load_file_as_dict("/home/pia/cluwll/selected_sentences_ita.csv")
    tatoeba_sents = {ast.literal_eval(k): v for k, v in tatoeba_sents.items()}

    opensubt_sents = load_file_as_dict("/home/pia/cluwll/opensubt_id_it_de.txt")
    opensubt_sents = {ast.literal_eval(k): v for k, v in opensubt_sents.items()}

    # read in these files to be able to print the German translation for the tatoeba sentences
    links_ita_deu = load_file_as_dict("/home/pia/cluwll/links_ita_deu.csv")
    links_ita_deu = {int(k): int(v) for k, v in links_ita_deu.items()}
    selected_sentences_deu = load_file_as_dict("/home/pia/cluwll/selected_sentences_deu.csv")
    selected_sentences_deu = {int(k): v for k, v in selected_sentences_deu.items()}

    # read in this file to be able to print the German translation for the opensubt sentences"
    selected_sentences_deu_opensubt = load_dict("/home/pia/cluwll/opensubt_id_it_de.txt", 0, 2)
    selected_sentences_deu_opensubt = {ast.literal_eval(k): v for k, v in selected_sentences_deu_opensubt.items()}


    contexts = []

    # field 0 = lemma, 2, 4 and 6 = IDs
    with open("/home/pia/cluwll/selected_context_sent_check_Marta.csv") as f:
        csv_reader = csv.reader(f, delimiter='\t')
        for row in csv_reader:
            lemma = row[0]
            print("Lemma: ", lemma)
            pos = row[1]
            ID1 = row[2]
            asis1 = row[3]
            ID2 = row[4]
            asis2 = row[5]
            ID3 = row[6]
            asis3 = row[7]
            comment = row[8]
            enough = row[9]
            #item = [lemma, pos, ID1, asis1, ID2, asis2, ID3, asis3, comment, enough]
            #print("ITEM: ", item)
            print("Working on LEMMA: ", lemma)


            # check all 3 IDs and create string: ID = lemma for that field
            ID1_sent = "N/A"
            ID1_sent_ger = "N/A"
            if ID1.isdigit():
                ID1 = int(ID1)
                if ID1 >= 9000000:
                    ID1_sent = opensubt_sents[ID1]
                    ID1_sent_ger = selected_sentences_deu_opensubt[ID1]
                else:
                    ID1_sent = tatoeba_sents[ID1]
                    id_ger1 = links_ita_deu[ID1]
                    ID1_sent_ger = selected_sentences_deu[id_ger1]

            ID2_sent = "N/A"
            ID2_sent_ger = "N/A"
            if ID2.isdigit():
                ID2 = int(ID2)
                if ID2 >= 9000000:
                    ID2_sent = opensubt_sents[ID2]
                    ID2_sent_ger = selected_sentences_deu_opensubt[ID2]
                else:
                    ID2_sent = tatoeba_sents[ID2]
                    id_ger2 = links_ita_deu[ID2]
                    ID2_sent_ger = selected_sentences_deu[id_ger2]

            ID3_sent = "N/A"
            ID3_sent_ger = "N/A"
            if ID3.isdigit():
                ID3 = int(ID3)
                if ID3 >= 9000000:
                    ID3_sent = opensubt_sents[ID3]
                    ID3_sent_ger = selected_sentences_deu_opensubt[ID3]
                else:
                    ID3_sent = tatoeba_sents[ID3]
                    id_ger3 = links_ita_deu[ID3]
                    ID3_sent_ger = selected_sentences_deu[id_ger3]

            # when opening csv later, the commas and newlines are disturbing the csv format
            comment = '. '.join(comment.split('\n'))  # when opening csv later, the commas and newlines are disturbing the format
            comment = ''.join(comment.split(','))


            item_complete = [lemma, pos, ID1, ID1_sent, ID1_sent_ger, asis1, ID2, ID2_sent, ID2_sent_ger, asis2,
                             ID3, ID3_sent, ID3_sent_ger, asis3, comment, enough]
            #item = [lemma, pos, ID1_sent, ID2_sent, ID3_sent, comment]
            #print("ITEM: ", item)
            contexts.append(item_complete)


    print("start writing to csv file...")
    #contexts = [[",".join([str(i) for i in sub])] for sub in contexts]
    with open('/home/pia/cluwll/context_Marta.csv', 'wt') as fo:
        writer = csv.writer(fo, delimiter='\t')
        for i in contexts:
            writer.writerow(i)
    print("...finished writing to csv file!")

