import os
import sys
import json


def classify():
    argv = sys.argv
    directory = argv[1]
    # output_file = argv[2]
    # directory = "dev/"
    output_file = "output.txt"

    # used during accuracy and recall calculation
    ham_file_count = 0
    spam_file_count = 0

    # No of files classified as ham or spam
    ham_classified_true = 0
    spam_classified_true = 0
    ham_classified_false = 0
    spam_classified_false = 0

    # read the json data from nbmodel.txt
    with open("per_model.txt") as data_file:
        data = json.load(data_file)

    fout = open(output_file, "w")

    for root, subdir, subfiles in os.walk(directory):
        if len(subfiles) != 0:
            for file in subfiles:
                alpha = 0
                if ".txt" in file:
                    f = open(root + "/" + file, "r", encoding="latin1")
                    words = f.read().strip().split()

                    for w in words:
                        if w in data["vocab_list"]:
                            alpha += data["vocab_list"][w]

                    alpha += data["b"]

                    if alpha > 0:
                        fout.writelines("spam " + root + "/" + file + "\n")
                        if "spam" in file:
                            spam_classified_true += 1
                            spam_file_count += 1
                        else:
                            ham_classified_false += 1
                            ham_file_count += 1
                    else:
                        fout.writelines("ham " + root + "/" + file + "\n")
                        if "ham" in file:
                            ham_classified_true += 1
                            ham_file_count += 1
                        else:
                            spam_classified_false += 1
                            spam_file_count += 1

                    f.close()

    accuracy_ham = ham_classified_true/ham_file_count
    accuracy_spam = spam_classified_true/spam_file_count

    # calculating precision for ham and spam
    precision_spam = spam_classified_true/(spam_classified_true + ham_classified_false)
    precision_ham = ham_classified_true/(ham_classified_true + spam_classified_false)

    # calculating recall for ham and spam
    recall_spam = spam_classified_true/spam_file_count
    recall_ham = ham_classified_true/ham_file_count

    # calculating f1 score for ham and spam
    f1_spam = (2 * precision_spam * recall_spam)/(precision_spam + recall_spam)
    f1_ham = (2 * precision_ham * recall_ham)/(precision_ham + recall_ham)

    print("Total ham files:" + str(ham_file_count))
    print("Total spam files:" + str(spam_file_count))
    print("Total ham classified true:" + str(ham_classified_true))
    print("Total ham classified false:" + str(ham_classified_false))
    print("Total spam classified true:" + str(spam_classified_true))
    print("Total spam classified false:" + str(spam_classified_false))
    print()
    print("ham accuracy:" + str(accuracy_ham))
    print("spam accuracy:" + str(accuracy_spam))
    print()
    print("spam precision:" + str(precision_spam))
    print("spam recall:" + str(recall_spam))
    print("spam F1 Score:" + str(f1_spam))
    print()
    print("ham precision:" + str(precision_ham))
    print("ham recall:" + str(recall_ham))
    print("ham F1 Score:" + str(f1_ham))

    fout.close()

if __name__ == "__main__": classify()