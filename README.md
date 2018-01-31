## Language identification using n-gram model  

This technique makes use of statistics of particular combination of bytes that likely to be appear in a language (and encoding).

- Requirement :

  Python2.7+

- Usage:

  Pass the text, file or link to the NGram class to build a n-gram language model.

  . >>>  ref_en = NGram(fn="./path to reference text in English", ttype="file", n=3)

  .>>>   ref_zh = NGram(fn="./path to reference text in Chinese", ttype="file", n=3)

  .>>>   ref_en - ref_zh 

  0.994491469601

  .>>>    lanModel = languageDetectionModel(ngram=3)

  .>>>   lanModel.find_match("./path to unknown text", "file")

  predicted language, confidence score


- Methods:

  The NGram class can be used to compare blocks of text based on their local structure, which is a good indicator of the language used. You can designate the parameter of "n" in NGram class, such as 1,2,3, to get unigram, bigram, trigram model etc. The results show that trigram model is enough to compute a discriminating score to identify languages.  

  At first, compute the frequency of n-gram. Take trigram as an example, count the number of occurrences that one character following two given characters, that is, $$count(c|a,b)=n$$. Or compute the frequency of three characters, $$count(abc)=n$$. 

  When the statistical data of a language is treated as a vector, the difference of two languages can be seen as an angle between two vectors. The cosine of this angle varies between 1 for complete similarity, and 0 for utter difference.  Since letter combinations are characteristic to a language, this can be used to determine the language of a body of text.

  The languageDetectionModel class can be easily used to train a language identification model with given corpus. You can use this model to identify that whether the input text is one of the following languages: English, French, Finnish, Norwegian, Swedish, German, Chinese, Japanese.

- Experiments:

  - the corpus is obtained from the website or [electronic book](http://www.gutenberg.org/wiki/Category:Bookshelf)
  - More corpus can get better performance.
  - The accuracy on the random select test text in 8 languages is more than 99%. The score that represents the difference of two languages is accurate. For example, the score of two different languages is often larger than 0.5, and the score of the same language with sizable corpus is less than 0.1. 

- More details can be learned from the literature: Ramisch C. N-gram models for language detection[J]. 2008. 

  ​