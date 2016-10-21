import os
import sys
import json


def classify():
    argv = sys.argv
    # directory = argv[1]
    # output_file = argv[2]
    directory = "dev/"
    output_file = "output.txt"

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
                    else:
                        fout.writelines("ham " + root + "/" + file + "\n")

                    f.close()

    fout.close()

if __name__ == "__main__": classify()