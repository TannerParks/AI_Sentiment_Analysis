# Tanner Parks and Haofan Wang

import re
import csv
import math

class node:
    def __init__(self, name, true_true, true_false, false_true, false_false, c_true, c_false):
        self.name = name
        self.true_true = true_true      #P(vocabulary = true | classlabel = true)
        self.true_false = true_false    #P(vocabulary = true | classlabel = false)
        self.false_true = false_true    #P(vocabulary = false | classlabel = true)
        self.false_false = false_false  #P(vocabulary = false | classlabel = false)
        self.parents = 'classlabel'
        self.c_true = c_true            #p(classlabel = true)
        self.c_false = c_false          #p(classlabel = false)

def getData(fileName):
    """Turns the data from the file into a list of lists."""
    dataList = []

    with open(fileName, "r") as file:
        fileData = file.read().splitlines()
        for item in fileData:
            strip = re.sub(r'[^\w\s]', '', item).lower()    # strips punctuation and turns to lowercase
            data = strip.split()
            #print(data)
            dataList.append(data)

    return dataList


def alphabetize(reviews):
    """Alphabetizes the vocabulary"""
    vocab = []
    sentences = [sentence[:-1] for sentence in reviews] # List comprehension to remove number at end of each sentence
    words = [item for sentence in sentences for item in sentence]   # List comprehension to flatten list of lists
    [vocab.append(x) for x in words if x not in vocab]  # Get rid of duplicate words
    vocab.sort()
    vocab.append("classlabel")  # adds classlabel to end of vocab list

    return vocab


def features(vocab, sentences, fileName):
    """Turns each review into a list of features then outputs it to a file."""
    #print(vocab)
    featureList = []
    for sentence in sentences:
        feature = [0] * len(vocab)
        for word in sentence[:-1]:
            #print(word)
            if word in vocab:
                feature[vocab.index(word)] = 1
        if sentence[-1] == "1":
            feature[-1] = 1
        featureList.append(feature)

    with open(fileName, "w", newline='') as f:  # Write each line to the file
        wr = csv.writer(f)
        wr.writerow(vocab)
        wr.writerows(featureList)

    return featureList

def predict(db, test, title):
    classTrue = 0
    for a in range(len(db)):
        # print(db[a][-1])
        if db[a][-1] == 1:
            classTrue += 1
    classFalse = len(db) - classTrue
    # calculate P(classlabel = true)
    c_true = (classTrue + 1) / (len(db) + 2)

    # calculate P(classlabel = false)
    c_false = (classFalse + 1) / (len(db) + 2)

    classfier = []
    for x in range(len(title) - 1):
        # calculate P(vocabulary = true | classlabel = true)
        vtct = 0
        for a in range(len(db)):
            if db[a][x] == 1 and db[a][-1] == 1:
                vtct += 1
        true_true = (vtct + 1) / (classTrue + 2)
        # calculate P(vocabulary = true | classlabel = false)
        vtcf = 0
        for a in range(len(db)):
            if db[a][x] == 1 and db[a][-1] == 0:
                vtcf += 1
        true_false = (vtcf + 1) / (classFalse + 2)
        # calculate P(vocabulary = false | classlabel = true)
        vfct = 0
        for a in range(len(db)):
            if db[a][x] == 0 and db[a][-1] == 1:
                vfct += 1
        false_true = (vfct + 1) / (classTrue + 2)
        # calculate P(vocabulary = false | classlabel = false)
        vfcf = 0
        for a in range(len(db)):
            if db[a][x] == 0 and db[a][-1] == 0:
                vfcf += 1
        false_false = (vfcf + 1) / (classFalse + 2)

        # create a node
        newNode = node(title[x], true_true, true_false, false_true, false_false, c_true, c_false)
        classfier.append(newNode)

    # calculate the predict value for 1
    result = []
    correct = 0
    for i in range(len(test)):

        predict1 = math.log(c_true, 10)
        predict0 = math.log(c_false, 10)
        for y in range(len(title) - 1):
            if test[i][y] == 1:
                predict1 = predict1 + math.log(classfier[y].true_true, 10)
                predict0 = predict0 + math.log(classfier[y].true_false, 10)
            else:
                predict1 = predict1 + math.log(classfier[y].false_true, 10)
                predict0 = predict0 + math.log(classfier[y].false_false, 10)
        if predict1 > predict0:
            result.append(1)
            if test[i][-1] == 1:
                correct += 1
        else:
            result.append(0)
            if test[i][-1] == 0:
                correct += 1
    # print(result)
    precision = (correct / len(test)) * 100
    return precision



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    train = getData("trainingSet.txt")
    test_data = getData("testSet.txt")
    vocab = alphabetize(train)

    db = features(vocab, train, "preprocessed_train.txt")
    test = features(vocab, test_data, "preprocessed_test.txt")
    title = vocab

    precision1 = predict(db, db, title)
    precision2 = predict(db, test, title)

    print("The accuracy of using training data to predict training data is", precision1, "%")
    print("The accuracy of using training data to predict testing data is", precision2, "%")

    f = open("results.txt", "w")
    f.write("Using trainingSet.txt for training data and trainingSet.txt for testing data:\n")
    f.write("The accuracy of training data is ")
    f.write(str(precision1))
    f.write(" %\n")
    f.write("Using trainingSet.txt for training data and testSet.txt for testing data:\n")
    f.write("The accuracy of test data is ")
    f.write(str(precision2))
    f.write(" %\n")
    f.close()








