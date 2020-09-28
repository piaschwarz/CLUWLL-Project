"""
    Script to create a JSON file from a text
    reads text file (tsv) with word_form, POS, Lemma:
        Il      DET:def	il
        menù	NOM	    menù
        dell’	PRE:det	del
        osteria	NOM	    osteria
    and adds an ID and boolean has_context depending if it appears in the list context_full_list.csv

    writes a JSON file of that text in this format:
    {
    "1": [
        {
            "id": "1"
            "form": "Il",
            "pos": "DET",
            "lemma": "il",
            "has_context": "false",
            "is_title": "true"
        }
    ],
    "2": [
        {
            "id": "2",
            "form": "menù",
            "pos": "NOM",
            "lemma": "menù",
            "has_context": "false",
            "is_title": "true"
        }
    ],
    "3": [
        {
            "form": "dell’",
            ...
        }
    ],
    ...
    }
"""

from preprocess_tatoeba import dict_to_csv
from preprocess_opensubt_uniserver import load_file_as_dict
import ast
import csv
import pprint
from collections import defaultdict
import re
import gzip
import io
from process_context import load_dict
import json

if __name__ == '__main__':

    context_words = dict()
    with open("/home/pia/Schreibtisch/CLUWLL-Project/context_sentences/context_full_list.csv",
              encoding="utf-8") as f:
        csv_reader = csv.reader(f, delimiter="\t")
        for row in csv_reader:
            l = row[0].strip()
            p = row[1].strip()
            if l not in context_words.keys():
                context_words[l] = [p]
            else:
                context_words[l].append(p)


    for n in range(1, 27):
        print("N: ", n)
        text_file = "/home/pia/Schreibtisch/CLUWLL-Project/learnertexts_B2/text" + str(n) + ".txt"
        print("TEXT file: ", text_file)
        json_file = "/home/pia/Schreibtisch/CLUWLL-Project/learnertexts_B2/json/text" + str(n) + ".json"
        words_text = []
        sample_text = []
        id = 1
        with open(text_file, encoding="utf-8") as f:
            csv_reader = csv.reader(f, delimiter="\t")
            for row in csv_reader:
                form = row[0].strip()
                pos = row[1].strip().split(':')[0]
                lemma = row[2].strip()

                if lemma in context_words.keys() and pos in context_words[lemma]:
                    sample_text.append([id, form, pos, lemma, "true"])
                    words_text.append({
                        'id': id,
                        'form': form,
                        'pos': pos,
                        'lemma': lemma,
                        'has_context': "true",
                        'is_title': "false"
                    })
                else:
                    sample_text.append([id, form, pos, lemma, "false"])
                    words_text.append({
                        'id': id,
                        'form': form,
                        'pos': pos,
                        'lemma': lemma,
                        'has_context': "false",
                        'is_title': "false"
                    })

                id += 1
        text = dict({"text": words_text})
        with open(json_file, 'w', encoding='utf-8') as outfile:
            json.dump(text, outfile, indent=4, ensure_ascii=False)




