import _json
import treetaggerwrapper
import nltk
nltk.download('stopwords')
import spacy




def lemmatization():
    tagger = treetaggerwrapper.TreeTagger(TAGLANG="it", TAGDIR='/home/marta/TreeTagger')

    f_input=open("B2_texts_updated.txt", "r")
    contents=f_input.read()
    #print(contents)


    f_output_tagged_texts= open("B2_tagged_texts_updated_PROVA.txt", "w")
    tagged_text = tagger.tag_text(contents)
    for slot in tagged_text:
        f_output_tagged_texts.write(slot + "\n")
    print(tagged_text)

    # #create files for list of lemmas, of stopwords and of capitalized words
    # f_output_lemmas= open("B1_lemmas_list_updated_PROVA.txt", "w")
    # f_output_stopwords= open("B1_stopwords_list_updated_PROVA.txt", "w")
    # f_output_capitalized= open("B1_capitalized_list_updated_PROVA.txt", "w")
    #
    # #set for unique lemmas, capitalized lemmas, stopwords
    # lemmas_set= set()
    # capitalized_lemmas_set=set()
    # stopwords_set= set()
    #
    # for tagged_word in tagged_text:
    #     tags_list=tagged_word.split("\t")
    #     if len(tags_list)<3:
    #         print(tagged_word)
    #
    #     pos_tag= tags_list[1]
    #     lemma=tags_list[2]
    #
    #
    #     if lemma[0].islower():
    #         #if it has the pos_tag of a stopword, add it to stopwords list
    #         if (pos_tag == "ABR") or (pos_tag == "INT") or (pos_tag == "PRO") or (pos_tag == "CON") or (pos_tag == "DET:def") or (pos_tag == "DET:indef") or (pos_tag == "LS") or (pos_tag == "NUM") or (pos_tag == "PON") or (pos_tag == "PRE") or (pos_tag == "PRE:det") or (pos_tag == "SENT") or (pos_tag == "SYM") or (pos_tag == "FW"):
    #             stopwords_set.add(lemma)
    #         #otherwise add to list of lemmas
    #         else:
    #             lemmas_set.add(lemma + "\t" + pos_tag)
    #
    #     elif (lemma[0].isupper()) or (pos_tag == "NPR"):
    #         capitalized_lemmas_set.add(lemma)
    #
    #
    # #iterate through the sets and print content to file
    # for x in lemmas_set:
    #     f_output_lemmas.write(x + "\n")
    #
    # for y in stopwords_set:
    #     f_output_stopwords.write(y + "\n")
    #
    # for z in capitalized_lemmas_set:
    #     f_output_capitalized.write(z + "\n")

    #print(lemmas_set)
    #print(capitalized_lemmas_set)
    #print(stopwords_set)















#lemmatize text
#put lemmas into a list (if you

if __name__== "__main__":
    lemmatization()
