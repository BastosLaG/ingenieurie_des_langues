#découpage en phrase avec utilisation de nltk

import nltk
from nltk.tokenize import sent_tokenize, word_tokenize

nltk.download('punkt')


texte = "Il arrivera possible que mon travail fera naître à d'autres personnes l'envie de porter la chose plus loin. Tant s'en faut que cette matière soit épuisée, qu'il reste encore plus de fables à mettre en vers que je n'en ai mis."

sentences = sent_tokenize(texte)
phrases = ["<p>" + sentence + "</p>" for sentence in sentences]
print(phrases)
