import math
import argparse
import codecs
from collections import defaultdict
import random
import numpy
"""
This file is part of the computer assignments for the course DD1418/DD2418 Language engineering at KTH.
Created 2018 by Johan Boye and Patrik Jonell.
"""

class Generator(object) :
    """
    This class generates words from a language model.
    """
    def __init__(self):
    
        # The mapping from words to identifiers. 
        self.index = {}

        # The mapping from identifiers to words.
        self.word = {}

        # An array holding the unigram counts.
        self.unigram_count = {}

        # The bigram log-probabilities.
        self.bigram_prob = defaultdict(dict)

        # Number of unique words (word forms) in the training corpus.
        self.unique_words = 0

        # The total number of words in the training corpus.
        self.total_words = 0

        # The average log-probability (= the estimation of the entropy) of the test corpus.
        # Important that it is named self.logProb for the --check flag to work
        self.logProb = 0

        # The identifier of the previous word processed in the test corpus. Is -1 if the last word was unknown.
        self.last_index = -1

        # The fraction of the probability mass given to unknown words.
        self.lambda3 = 0.000001

        # The fraction of the probability mass given to unigram probabilities.
        self.lambda2 = 0.01 - self.lambda3

        # The fraction of the probability mass given to bigram probabilities.
        self.lambda1 = 0.99

        # The number of words processed in the test corpus.
        self.test_words_processed = 0


    def read_model(self,filename):
        """
        Reads the contents of the language model file into the appropriate data structures.

        :param filename: The name of the language model file.
        :return: <code>true</code> if the entire file could be processed, false otherwise.
        """

        try:
            with codecs.open(filename, 'r', 'utf-8') as f:
                self.unique_words, self.total_words = map(int, f.readline().strip().split(' '))
                i = 0
                while True:
                    if i<self.unique_words:

                        row = f.readline().strip().split(' ')
                        self.index[row[1]]=row[0]
                        self.word[row[0]]=row[1]
                        self.unigram_count[row[0]]=int(row[2])/self.total_words
                        i += 1
                    else:
                        row = f.readline().strip().split(' ')
                        if int(row[0])== -1:
                            break

                        self.bigram_prob[row[0]][row[1]] = row[2]
                return True
        except IOError:
            print("Couldn't find bigram probabilities file {}".format(filename))
            return False

    def generate(self, w, n):
        """
        Generates and prints n words, starting with the word w, and following the distribution
        of the language model.
        """ 


        self.last_index = self.index[w]
        words_to_print = []
        words_to_print.append(w)

        for i in range(n):
            rand = random.random()
            prob_lim = 0

            if self.last_index != -1 or self.bigram_prob[self.last_index] == {}:
                for word in self.bigram_prob[self.last_index].keys():
                    log_prob = float(self.bigram_prob[self.last_index][word])
                    prob_lim += numpy.exp(float(log_prob))
                    if rand <= prob_lim:
                        words_to_print.append(self.word[word])
                        self.last_index = word
                        break
            else:
                for word in self.unigram_count.keys():
                    prob_lim += self.unigram_count[word]
                    if rand <= prob_lim:
                        words_to_print.append(self.word[word])
                        self.last_index = word
                        break

        for word in words_to_print:
            print(word + ' ')
        #print(words_to_print)
        #print(len(words_to_print))



def main():
    """
    Parse command line arguments
    """
    

    # parser = argparse.ArgumentParser(description='BigramTester')
    # parser.add_argument('--file', '-f', type=str,  required=True, help='file with language model')
    # parser.add_argument('--start', '-s', type=str, required=True, help='starting word')
    # parser.add_argument('--number_of_words', '-n', type=int, default=100)

    # arguments = parser.parse_args()

    # generator = Generator()
    # generator.read_model(arguments.file)
    # generator.generate(arguments.start,arguments.number_of_words)
    


    generator = Generator()
    generator.read_model("kafka_model.txt")
    generator.generate("franz",50)
    

if __name__ == "__main__":
    main()
