#!/usr/bin/python
# coding:utf-8

import random
from urllib import urlopen


class NGram(object):
    def __init__(self, fn=None, ttype='file', n=3):
        self.length = None
        self.n = n
        self.table = {}
        if fn is not None:
            # print fn,ttype
            self.parseFile(fn, ttype)
        self.calculate_length()

    def parseFile(self, fn, ttype):
        chars = ' ' * self.n  # initial sequence of spaces with length n
        flag = False
        if ttype == 'link':
            print "trying to fetch url, may take time..."
            f = urlopen(fn)
        elif ttype == 'file':
            f = open(fn)
            # print "read file from:%s" % fn

        elif ttype == 'text':
            f = fn.split('\n')
            flag = True
        else:
            print ttype       
            print "Forwarded type unknown"
            return

        for z, line in enumerate(f):
            for letter in (" ".join(line.strip().split()) + " "):
                chars = chars[1:] + letter  # append letter to sequence of length n
                self.table[chars] = self.table.get(chars, 0) + 1  # increment count
        if not flag:
            f.close()

    def calculate_length(self):
        """ Treat the N-Gram table as a vector and return its scalar magnitude
        to be used for performing a vector-based search.
        """
        self.length = sum([x * x for x in self.table.values()]) ** 0.5
        return self.length

    def __sub__(self, other):
        """ Find the difference between two NGram objects by finding the cosine
        of the angle between the two vector representations of the table of
        N-Grams. Return a float value between 0 and 1 where 0 indicates that
        the two NGrams are exactly the same.
        """
        if not isinstance(other, NGram):
            raise TypeError("Can't compare NGram with non-NGram object.")

        if self.n != other.n:
            raise TypeError("Can't compare NGram objects of different size.")

        total = 0
        for k in self.table:
            total += self.table[k] * other.table.get(k, 0)

        return 1.0 - (float(total)) / (float(self.length) * float(other.length))

    


class Trigram:
 
    length = 0

    def __init__(self, fn=None, ttype='file'):
        self.lut = {}
        if fn is not None:
            # print fn,ttype
            self.parseFile(fn, ttype)

    def parseFile(self, fn, ttype):
        pair = '  '
        flag = False
        if ttype == 'link':
            print "trying to fetch url, may take time..."
            f = urlopen(fn)
        elif ttype == 'file':
            # f = codecs.open(fn,encoding='US-ASCII')
            f = open(fn)
            # print "read file from:%s" % fn

        elif ttype == 'text':
            f = fn.split('\n')
            flag = True
        else:
            print "Forwarded type unknown"

        for z, line in enumerate(f):
            # if not z % 10000:
            #     print "line %s" % z
            # \n's are spurious in a prose context
            # to remove more space
            for letter in (" ".join(line.strip().split()) + ' '):
                d = self.lut.setdefault(pair, {})
                d[letter] = d.get(letter, 0) + 1
                pair = pair[1] + letter
        if not flag:
            f.close()
        self.measure()

    def measure(self):
        """calculates the scalar length of the trigram vector and
        stores it in self.length."""
        total = 0
        for y in self.lut.values():
            total += sum([x * x for x in y.values()])
        self.length = total ** 0.5

    def similarity(self, other):
        """returns a number between 0 and 1 indicating similarity.
        1 means an identical ratio of trigrams;
        0 means no trigrams in common.
        """
        if not isinstance(other, Trigram):
            raise TypeError("can't compare Trigram with non-Trigram")
        lut1 = self.lut
        lut2 = other.lut
        total = 0
        for k in lut1.keys():
            if k in lut2:
                a = lut1[k]
                b = lut2[k]
                for x in a:
                    if x in b:
                        total += a[x] * b[x]

        return float(total) / (self.length * other.length)

    def __sub__(self, other):
        """indicates difference between trigram sets; 1 is entirely
        different, 0 is entirely the same."""
        return 1 - self.similarity(other)

    def makeWords(self, count):
        """returns a string of made-up words based on the known text."""
        text = []
        k = '  '
        while count:
            n = self.likely(k)
            text.append(n)
            k = k[1] + n
            if n in ' \t':
                count -= 1
        return ''.join(text)

    def likely(self, k):
        """Returns a character likely to follow the given string
        two character string, or a space if nothing is found."""
        if k not in self.lut:
            return ' '
        # if you were using this a lot, caching would a good idea.
        letters = []
        for k, v in self.lut[k].items():
            letters.append(k * v)
        letters = ''.join(letters)
        return random.choice(letters)


class languageDetectionModel:
    def __init__(self,ngram):
        self.ngram = ngram
        self.en = NGram('./english2.txt', n=ngram)
        # NB fr and some others have English license text.
        #   no has english excerpts.
        self.fr = NGram('./french.txt', n=ngram)
        self.fi = NGram('./Finnish.txt', n=ngram)
        self.no = NGram('./Norwegian.txt', n=ngram)
        self.se = NGram('./Swedish.txt', n=ngram)
        self.de = NGram("./German2.txt", n=ngram)
        self.zh = NGram("./Chinese2.txt", n=ngram)
        self.ja = NGram("./Japanese.txt", n=ngram)
        self.languages = [self.en, self.fr, self.fi, self.no, self.se, self.de, self.zh, self.ja]
        self.languageName = ["English", "French", "Finnish", "Norwegian", "Swedish", "German", "Chinese", "Japanese"]

    def find_match(self, input,ttype):
        unknown = NGram(input, ttype=ttype,n=self.ngram)
        similarity_scores = []

        for profile in self.languages:
            similarity_scores.append(profile - unknown)
        reference_score = min(similarity_scores)
        lan = self.languageName[similarity_scores.index(reference_score)]
        if reference_score < 0.2:
            print "The language of input : %s \n is %s with confidence:%f" % (input,lan, 1 - reference_score)
        else:
            # print similarity_scores
            print "The language of input : %s \n most likely to be %s with confidence:%f" % (input,lan, 1 - reference_score)

        return lan,reference_score

    
def testNgram(ngram=3,testSentences="",infile=""):
    print "Test NGram class!"
    en = NGram('./english.txt', n=ngram)
    # NB fr and some others have English license text.
    #   no has english excerpts.
    fr = NGram('./french.txt', n=ngram)
    fi = NGram('./Finnish.txt', n=ngram)
    no = NGram('./Norwegian.txt', n=ngram)
    se = NGram('./Swedish.txt', n=ngram)
    no2 = NGram('./Norwegian.txt', n=ngram)
    en2 = NGram('./english2.txt', n=ngram)
    fr2 = NGram('./French2.txt', n=ngram)
    de = NGram("./German.txt", n=ngram)
    de2 = NGram("./German2.txt", n=ngram)
    zh = NGram("./Chinese.txt", n=ngram)
    zh2 = NGram("./Chinese2.txt", n=ngram)
    ja = NGram("./Japanese.txt", n=ngram)
    print "calculating difference:"
    print "English - German is %s" % (en - de)
    print "German - English is %s" % (de - en)
    print "German - German2 is %s" % (de - de2)
    print "German - Chinese is %s" % (de - zh)
    print "English - Chinese is %s" % (en - zh)
    print "Chinese - Chinese2 is %s" % (zh - zh2)
    print "Chinese - Japanese is %s" % (zh - ja)
    print "English - Japanese is %s" % (en - ja)
    print "English - French is %s" % (en - fr)
    print "English - English2 is %s" % (en - en2)
    print "English - French2 is %s" % (en - fr2)
    print "French - English2 is %s" % (fr - en2)
    print "French - French2 is %s" % (fr - fr2)
    print "French2 - English2 is %s" % (fr2 - en2)
    print "Finnish - French  is %s" % (fi - fr)
    print "Finnish - English  is %s" % (fi - en)
    print "Finnish - Swedish  is %s" % (fi - se)
    print "Norwegian - Swedish  is %s" % (no - se)
    print "English - Norwegian  is %s" % (en - no)
    print "Norwegian - Norwegian2  is %s" % (no - no2)
    print "Swedish - Norwegian2  is %s" % (se - no2)
    print "English - Norwegian2  is %s" % (en - no2)
    print "French - Norwegian2  is %s" % (fr - no2)

    lanModel = languageDetectionModel(ngram)
    if infile:
        lanModel.find_match(infile, "file")
    if testSentences:
        lanModel.find_match(testSentences, "text")





def testTrigram():
    print "Test Trigram class"
    en = Trigram('./english.txt')
    # NB fr and some others have English license text.
    #   no has english excerpts.
    fr = Trigram('./french.txt')
    fi = Trigram('./Finnish.txt')
    no = Trigram('./Norwegian.txt')
    se = Trigram('./Swedish.txt')
    no2 = Trigram('./Norwegian.txt')
    en2 = Trigram('./english2.txt')
    fr2 = Trigram('./French2.txt')
    de = Trigram("./German.txt")
    de2 = Trigram("./German2.txt")
    zh = Trigram("./Chinese.txt")
    zh2 = Trigram("./Chinese2.txt")
    ja = Trigram("./Japanese.txt")
    print "calculating difference:"
    print "en - de is %s" % (en - de)
    print "de - en is %s" % (de - en)
    print "de - de2 is %s" % (de - de2)
    print "de - zh is %s" % (de - zh)
    print "en - zh is %s" % (en - zh)
    print "zh - zh2 is %s" % (zh - zh2)
    print "zh - ja is %s" % (zh - ja)
    print "en - ja is %s" % (en - ja)
    print "en - fr is %s" % (en - fr)
    print "en - en2 is %s" % (en - en2)
    print "en - fr2 is %s" % (en - fr2)
    print "fr - en2 is %s" % (fr - en2)
    print "fr - fr2 is %s" % (fr - fr2)
    print "fr2 - en2 is %s" % (fr2 - en2)
    print "fi - fr  is %s" % (fi - fr)
    print "fi - en  is %s" % (fi - en)
    print "fi - se  is %s" % (fi - se)
    print "no - se  is %s" % (no - se)
    print "en - no  is %s" % (en - no)
    print "no - no2  is %s" % (no - no2)
    print "se - no2  is %s" % (se - no2)
    print "en - no2  is %s" % (en - no2)
    print "fr - no2  is %s" % (fr - no2)

    print "\nmaking up English"
    print en.makeWords(30)
    print "\nmaking up German"
    print de2.makeWords(30)


if __name__ == '__main__':
    # testTrigram()
    ngram=3
    testSentences = "How did you get on? Great. If you want to hear more about this topic, please visit our website bbclearningenglish.com. That's about it from the pronunciation workshop this week. Bye bye."    
    infile = "./testFile.txt"
    testNgram(ngram,testSentences,infile)