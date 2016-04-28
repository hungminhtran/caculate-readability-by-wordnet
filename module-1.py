from nltk.corpus import wordnet as wn
import nltk
import re

def standanizeNoun(noun):
    #standardize noun
    tnoun = noun.replace(' ', '_')
    tnoun = wn.morphy(tnoun, wn.NOUN)
    return tnoun

#compound ration of a word / hyponym
#input: noun
#output: (cpd, hyponym, total_hyponym_len)
def cpdRatio(SynsetNoun, level, hypernymName):
    #maximum is recurse 6 level
    if (level > 6):
        return 0, 0, 0
    if (not SynsetNoun):
        return 0, 0, 0
#    print level,SynsetNoun.name()
    cpd = 0
    hyponym = 0
    total_lens = 0
    allHyponyms = SynsetNoun.hyponyms() #why we choose this?
    if (allHyponyms == []):
        return 0, 0, 0
    for synset in allHyponyms:
        for lemma in synset.lemmas():
            hyponym = hyponym + 1
            if re.search(hypernymName, lemma.name()): #noun in cpd hyponym, don't care whole word???
                cpd = cpd + 1
            total_lens = total_lens + len(lemma.name())
#            print level, SynsetNoun.hyponyms()[0].name(), lemma.name()
            if synset.name().find('_'):
                total_lens = total_lens -1 #remove space from len counter
        if synset.lemmas()[0]:
            tmp1, tmp2, tmp3 = cpdRatio(synset, level+1, hypernymName)
            cpd = cpd + tmp1
            hyponym = hyponym + tmp2
            total_lens = total_lens + tmp3
    #return result
    return cpd, hyponym, total_lens

# testNoun = ['guitar', 'apples', 'piano', 'drum', 'peach', 'grape', 'hammer', 'saw', 'screwdriver', 'pants', 'paper']
# for noun in testNoun:
#     noun = standanizeNoun(noun)
#     print noun, cpdRatio(wn.synsets(noun)[0],1, noun)
