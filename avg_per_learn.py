import sys
import os
import json
from random import shuffle

max_iter = 30


class Model():
    # serialize the data and store it in a file nbmodal.txt. This file will be used as input to nbclassify.py
    def __init__(self, vocab_list, b):
        self.vocab_list = vocab_list
        self.b = b


def learn():
    directory = sys.argv[1]
    # directory = "train/"
    # all files are contained in file_list
    file_list = []
    word_list = {}

    vocab_list = {}
    avg_vocab_list = {}
    words = []
    y = 0
    b = 0
    beta = 0
    c = 1

    # read all the files and append it a list
    for root, subdir, subfiles in os.walk(directory):
        if len(subfiles) != 0:
            for f in subfiles:
                if ".txt" in f:
                    file_list.append(os.path.join(root, f))

    for i in range(max_iter):
        # randomly select a file due to problem with standard perceptron
        # first time, there is no need to do shuffling
        if i != 0:
            shuffle(file_list)

        for file in file_list:
            alpha = 0
            y = -1 if "ham" in file else 1
            # open the file only once and save the words to word_list to save computation
            if i == 0:
                f = open(file, "r", encoding="latin1")
                words = f.read().strip().split()
                word_list[file] = words
                f.close()
            else:
                words = word_list[file]

            for w in words:
                if w not in vocab_list and w not in avg_vocab_list:
                    vocab_list[w] = 0
                    avg_vocab_list[w] = 0
                else:
                    # calculate the value using perceptron model
                    # compute activation for current file
                    alpha += vocab_list[w]

            alpha += b
            y_alpha = y * alpha

            # wrong prediction
            if y_alpha <= 0:
                for w in words:
                    vocab_list[w] += y
                    avg_vocab_list[w] += (y*c)
                # update bias value
                b += y
                # update beta value
                beta += (y*c)

            c += 1

    for w in avg_vocab_list.keys():
        avg_vocab_list[w] = vocab_list[w] - ((1/c)*avg_vocab_list[w])

    beta = b - ((1/c)*beta)

    # serializing the data
    obj = Model(avg_vocab_list, beta)
    a = json.dumps(vars(obj))
    fs = open("per_model.txt", "w")
    fs.write(a)
    fs.close()

if __name__ == "__main__": learn()