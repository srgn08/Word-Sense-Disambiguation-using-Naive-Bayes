from stemmer import PorterStemmer
import sys


def calculate_probability(word_dictionary,tag_dictionary,x,k,temp,tag4,lex):
    flag = temp in word_dictionary[lex][x[k]]
    if flag == False:
        total = 1
    else:
        total = word_dictionary[lex][x[k]][temp]

    flag = tag4 in tag_dictionary[lex][x[k]]["+1"]
    if flag == False:
        total2 = 1
    else:
        total2 = tag_dictionary[lex][x[k]]["+1"][tag4]

    return total*total2



def calculate_tag(word):
    control = 0
    x = ""
    temp2 = ""
    for i in range(len(word)):
        if control == 0 and word[i] == '"':
            control = 1
        elif control == 1 and word[i] == '"':
            break
        elif control == 1 and word[i] != '"':
            temp2 = temp2 + word[i]
    return temp2




def read_input(array,p):
    word_dictionary = {}
    tag_dictionary = {}
    control=0
    context=""
    lex=""
    count = {}

    for i in range(len(array)):
        if "<lexelt item=" in array[i]:
            lex=calculate_tag(array[i])
            if lex not in word_dictionary:
                word_dictionary[lex] = {}
                tag_dictionary[lex] = {}
                count[lex] = {}

        elif "<answer instance=" in array[i]:
            temp=array[i]
            length=len(array[i])
            sense_id=temp[length-9:length-3]
            if sense_id not in word_dictionary[lex]:
                word_dictionary[lex][sense_id] = {}
                tag_dictionary[lex][sense_id] = {"-3" : {},"-2" : {},"-1" : {},"+1" : {},"+2" : {},"+3" : {}}
                count[lex][sense_id] = 0
        elif "<context>" in array[i]:
            control=1
        elif "</context>" in array[i]:
            result = context.split(" ")
            for i in range(len(result)):
                if "<head>" in result[i]:
                    tag1 = calculate_tag(result[i-5])
                    tag2 = calculate_tag(result[i-3])
                    tag3 = calculate_tag(result[i-1])

                    for j in range(-3,3):
                        if j != 0:
                            if len(result) > i + 2*j + 1:
                                count[lex][sense_id] += 1
                                word = p.stem(result[i + 2*j], 0, len(result[i + 2*j]) - 1)

                                if word in word_dictionary[lex][sense_id]:
                                    word_dictionary[lex][sense_id][word] += 1
                                else:
                                    word_dictionary[lex][sense_id][word] = 1


                    if tag3 in tag_dictionary[lex][sense_id]["-1"]:
                        tag_dictionary[lex][sense_id]["-1"][tag3] += 1
                    else:
                        tag_dictionary[lex][sense_id]["-1"][tag3] = 1

                    if tag2 in tag_dictionary[lex][sense_id]["-2"]:
                        tag_dictionary[lex][sense_id]["-2"][tag2] += 1
                    else:
                        tag_dictionary[lex][sense_id]["-2"][tag2] = 1

                    if tag1 in tag_dictionary[lex][sense_id]["-3"]:
                        tag_dictionary[lex][sense_id]["-3"][tag1] += 1
                    else:
                        tag_dictionary[lex][sense_id]["-3"][tag1] = 1

                    if len(result)>i+3:
                        tag4 = calculate_tag(result[i+3])
                        if tag4 in tag_dictionary[lex][sense_id]["+1"]:
                            tag_dictionary[lex][sense_id]["+1"][tag4] += 1
                        else:
                            tag_dictionary[lex][sense_id]["+1"][tag4] = 1

                    if len(result)> i + 5:
                        tag5 = calculate_tag(result[i+5])
                        if tag5 in tag_dictionary[lex][sense_id]["+2"]:
                            tag_dictionary[lex][sense_id]["+2"][tag5] += 1
                        else:
                            tag_dictionary[lex][sense_id]["+2"][tag5] = 1

                    if len(result)> i + 7:
                        tag6 = calculate_tag(result[i+7])
                        if tag6 in tag_dictionary[lex][sense_id]["+3"]:
                            tag_dictionary[lex][sense_id]["+3"][tag6] += 1
                        else:
                            tag_dictionary[lex][sense_id]["+3"][tag6] = 1

                    break

            context=""
            control=0
        elif control==1:
            context=context+array[i]

    return word_dictionary,tag_dictionary,count




def read_test_data(array,word_dictionary,tag_dictionary,count):
    control=0
    context=""
    file = open(sys.argv[3], "w")
    for i in range(len(array)):
        if "<lexelt item=" in array[i]:
            lex=calculate_tag(array[i])

        elif "<instance id=" in array[i]:
            id=calculate_tag(array[i])


        elif "<context>" in array[i]:
            control=1
        elif "</context>" in array[i]:
            result = context.split(" ")
            for i in range(len(result)):
                if "<head>" in result[i]:
                    tag1 = calculate_tag(result[i-5])
                    tag2 = calculate_tag(result[i-3])
                    tag3 = calculate_tag(result[i-1])
                    if len(result) > i + 2:
                        tag4=  calculate_tag(result[i+1])
                        temp = result[i+2]
                    else:
                        tag4=""
                        temp=""
                    if len(result) > i + 4:
                        tag5=  calculate_tag(result[i+3])
                        temp2=result[i+4]
                    else:
                        tag5=""
                        temp2 = ""
                    if len(result) > i + 6:
                        tag6 = calculate_tag(result[i+5])
                        temp3=result[i+6]
                    else:
                        tag6=""
                        temp3 = ""

                    x = word_dictionary[lex].keys()
                    x=list(x)
                    min = -1
                    index=0
                    for k in range(len(word_dictionary[lex])):
                        total=1
                        total=  total * calculate_probability(word_dictionary, tag_dictionary, x, k, temp,  tag4, lex)
                        total = total * calculate_probability(word_dictionary, tag_dictionary, x, k, temp2, tag5, lex)
                        total = total * calculate_probability(word_dictionary, tag_dictionary, x, k, temp3, tag6, lex)
                        total = total * calculate_probability(word_dictionary, tag_dictionary, x, k, result[i-6], tag1, lex)
                        total = total * calculate_probability(word_dictionary, tag_dictionary, x, k, result[i-4], tag2, lex)
                        total = total * calculate_probability(word_dictionary, tag_dictionary, x, k, result[i-2], tag3, lex)
                        total=total/count[lex][x[k]]
                        if min<total:
                            min=total
                            index=k

                    file.write(id+" "+x[index])
                    file.write("\n")

                    break

            context=""
            control=0
        elif control==1:
            context=context+array[i]




def main():
    array=[]
    array2 = []
    p = PorterStemmer()
    with open(sys.argv[1]) as f:
        for line in f:
            if len(line)>1:
                array.append(line[0:len(line) - 1])
        word_dictionary, tag_dictionary,count =read_input(array,p)

    with open(sys.argv[2]) as f:
        for line in f:
            if len(line)>1:
                array2.append(line[0:len(line) - 1])
    read_test_data(array2,word_dictionary,tag_dictionary,count)




main()