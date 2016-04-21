from nltk.corpus import wordnet as wn
'''
get input
scan all nouns in text -> textNounsArray
which each nouns, get all hypernym/hyponyms (6 levels max)
    --> given a word, calculate number of compounds in hypornym -> get all hypernym/hypornym -> calculate again
select all word which ratio compounds > 25%
direct hyponyms - len(target word) >=4
calculate this ratio
'''



'''
import nltk
# dog1 = wn.synset('dog.n.01')
# print dog1.hyponyms()
# print "________________"
# dog2 = wn.synset('dog.n.02')
# print dog2.hyponyms()

text = nltk.word_tokenize("Dive into NLTK: Part-of-speech tagging and POS Tagger. We have a red hat.")
print text
print nltk.pos_tag(text)
