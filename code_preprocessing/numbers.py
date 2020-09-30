def numbers_out():
    f_input=open("B2_list_Pia.txt")
    contents=f_input.readlines()


    f_input_2=open("numbers.txt")
    contents2=f_input_2.readlines()

    #go through the lemmas from the B1 list
    line_arr = []
    for line in contents:
        line_arr = line.split("\t")
        lemma = line_arr[0]
        if (("cento" in lemma) or ("mille" in lemma) or ("mila" in lemma) or ("milion" in lemma)):
            print(lemma)

        

        for num in contents2:
            num = num[0:-1]
            if (num == lemma):
                print(lemma)


if __name__== "__main__":
    numbers_out()
