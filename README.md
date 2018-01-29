## Language identification using character trigrams  
This technique make use of statistics of particular combination of bytes that likely to be appear in a language (and encoding).

The Trigram class can be used to compare blocks of text based on their local structure, which is a good indicator of the language used.  The languageDetectionModel can be a good example to train a language identification model with small corpus. You can use this model to identify whether the input text is one of the following languages: English, French, Finnish, Norwegian, Swedish, German, Chinese, Japanese.

More details can be learned from the literature: Ramisch C. N-gram models for language detection[J]. 2008. 

- Requirment :

  Python2.7+

