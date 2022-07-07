# Class Bag of Words. 
# 
# This class is implemented with the aim of validate if any regular expression defined in there, 
# is content on a given text

import re 
import os


class bagOfWords:

    basedir = os.path.abspath(os.path.dirname(__file__))

    def __init__(self):
        self.words= []
        print(os.getcwd()) 
        with open(os.path.join(self.basedir, 'bow.txt')) as f:
            for w in f:
                self.words.extend(w.split(","))


    def normalizeText(self, text):
        return text.lower()

    def findRegex(self, text):

        for w in self.words:
            if re.search(w, text):
                return True
        return False

    def relevance(self, text):
        count=0
        for w in self.words:
            count+=len(re.findall(w, text))
        return count
