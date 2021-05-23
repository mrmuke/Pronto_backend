from nltk.corpus import wordnet

syns = wordnet.synsets("historic")

print([syn.name() for syn in syns[0].lemmas()])