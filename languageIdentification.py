#!/usr/bin/python
#coding:utf-8

import random
from urllib import urlopen

class Trigram:
    """From one or more text files, the frequency of three character
    sequences is calculated.  When treated as a vector, this information
    can be compared to other trigrams, and the difference between them
    seen as an angle.  The cosine of this angle varies between 1 for
    complete similarity, and 0 for utter difference.  Since letter
    combinations are characteristic to a language, this can be used to
    determine the language of a body of text. For example:

        >>> reference_en = Trigram('/path/to/reference/text/english')
        >>> reference_de = Trigram('/path/to/reference/text/german')
        >>> unknown = Trigram('url://pointing/to/unknown/text')
        >>> unknown.similarity(reference_de)
        0.4
        >>> unknown.similarity(reference_en)
        0.95

    would indicate the unknown text is almost cetrtainly English.  As
    syntax sugar, the minus sign is overloaded to return the difference
    between texts, so the above objects would give you:

        >>> unknown - reference_de
        0.6
        >>> reference_en - unknown    # order doesn't matter.
        0.05

    As it stands, the Trigram ignores character set information, which
    means you can only accurately compare within a single encoding
    (iso-8859-1 in the examples).  A more complete implementation might
    convert to unicode first.

    As an extra bonus, there is a method to make up nonsense words in the
    style of the Trigram's text.

        >>> reference_en.makeWords(30)
        My withillonquiver and ald, by now wittlectionsurper, may sequia,
        tory, I ad my notter. Marriusbabilly She lady for rachalle spen
        hat knong al elf

    Beware when using urls: HTML won't be parsed out.

    Most methods chatter away to standard output, to let you know they're
    still there.
    """
    length = 0

    def __init__(self, fn=None,ttype='file'):
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
            print "read file from:%s" % fn

            
        elif ttype == 'text':
            f = fn.split('\n') 
            flag = True
        else:
            print "Forwarded type unknown"

        for z, line in enumerate(f):
            # if not z % 10000:
            #     print "line %s" % z
            # \n's are spurious in a prose context
            for letter in line.strip() + ' ':
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
            total += sum([ x * x for x in y.values() ])
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
    def __init__(self):
        self.en = Trigram('./english2.txt')
        # NB fr and some others have English license text.
        #   no has english excerpts.
        self.fr = Trigram('./french.txt')
        self.fi = Trigram('./Finnish.txt')
        self.no = Trigram('./Norwegian.txt')
        self.se = Trigram('./Swedish.txt')
        self.de = Trigram("./German2.txt")
        self.zh = Trigram("./Chinese2.txt")
        self.ja = Trigram("./Japanese.txt")
        self.languageProfile=[self.en,self.fr,self.fi,self.no,self.se,self.de,self.zh,self.ja]
        self.languageName= ["English","French","Finnish","Norwegian","Swedish","German","Chinese","Japanese"]

    def testInput(self,infile,ttype):
        unknown = Trigram(infile,ttype=ttype)
        similarity_scores = []
        for profile in self.languageProfile:
            similarity_scores.append(profile-unknown)
        reference_score = min(similarity_scores)
        lan = self.languageName[similarity_scores.index(reference_score)]
        if reference_score<0.2:
            print "the language of the input file is %s with confidence:%f" %(lan,1-reference_score)
        else:
            # print similarity_scores
            print "the language most likely to be %s with confidence:%f" %(lan,1-reference_score)
            # print "It may not be the following languages :%s" % "English,French,Finnish,Norwegian,Swedish,German,Chinese,Japanese"


def test():
    print "Test the language detection performance!"
    en = Trigram('./english.txt')
   #NB fr and some others have English license text.
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
    print "\nmaking up French"
    print fr.makeWords(30)


if __name__ == '__main__':
    test()
    infile = "./testFile.txt"
    testSentences = "以新西兰英语为例，也可从其它日期目录查找新西兰英语，如果日期的文件不存在 ，我们可以选择最近文章"
    lanModel = languageDetectionModel()
    lanModel.testInput(infile,"file")
    lanModel.testInput(testSentences, "text")


    
