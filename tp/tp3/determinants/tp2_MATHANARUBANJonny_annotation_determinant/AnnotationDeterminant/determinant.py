import nltk
import re
import glob

# Téléchargement des données nltk
nltk.download('punkt')

# Fonction pour segmenter le texte en phrases
def segmenter_phrases(texte):
    phrases = nltk.sent_tokenize(texte)
    phrases_propres = [phrase.replace('\n', ' ') for phrase in phrases]
    return [f"<p> {phrase} </p>" for phrase in phrases_propres]

# Fonction pour annoter les déterminants dans une phrase
def annoter_determinant(phrase):
    determinants = ['le', 'la', 'l\'', 'les']
    pronoms = ['je', 'tu', 'il', 'elle', 'nous', 'vous', 'ils', 'elles']
    prepositions = ['chez', 'dans', 'de', 'entre', 'jusque', 'hors', 'par', 'pour', 'sans', 'vers']
    
    # Vérification des pronoms avec déterminants
    for pronom in pronoms:
        for determinant in determinants:
            pattern = re.compile(rf"\b{pronom}\b \b{determinant}\b", re.IGNORECASE)
            if pattern.search(phrase):
                return f"Phrase : {phrase}\nPronom personnel : {pronom} || Déterminant : {determinant}"

    # Vérification des prépositions avec déterminants
    for preposition in prepositions:
        for determinant in determinants:
            pattern = re.compile(rf"\b{preposition}\b \b{determinant}\b", re.IGNORECASE)
            if pattern.search(phrase):
                return f"Phrase : {phrase}\nPréposition : {preposition} || Déterminant : {determinant}"
    return None

# Fonction principale pour annoter les fichiers
def annoter_fichiers():
    for filename in glob.glob("*.txt"):
        print(f"{filename} :")
        with open(filename, 'r') as file:
            fichier = file.read()
        phrases = segmenter_phrases(fichier)
        for phrase in phrases:
            result = annoter_determinant(phrase)
            if result:
                print(result)

if __name__ == "__main__":
    annoter_fichiers()
