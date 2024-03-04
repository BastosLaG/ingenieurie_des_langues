import nltk
import re
import glob
import os

# Téléchargement des données nltk
nltk.download('punkt')

# Fonction pour segmenter le texte en phrases
def segmenter_phrases(texte):
    phrases = nltk.sent_tokenize(texte)
    phrases_propres = [phrase.replace('\n', ' ') for phrase in phrases]
    return phrases_propres

def determiner_fonction(mot_precedent):
    pronoms = ['je', 'tu', 'il', 'elle', 'nous', 'vous', 'ils', 'elles']
    prepositions = ['chez', 'dans', 'de', 'entre', 'jusque', 'hors', 'par', 'pour', 'sans', 'vers']
    if mot_precedent in prepositions:
        return "Article_Défini"
    elif mot_precedent in pronoms:
        return "Pronom_Personnel"
    else:
        return "Article_Défini"

# Fonction pour annoter les fichiers et écrire les résultats annotés dans un nouveau fichier XML
def annoter_fichiers(filename):
    occurrences_articles = {}
    occurrences_pronoms = {}

    with open(filename, 'r') as file:
        fichier = file.read()
    phrases = segmenter_phrases(fichier)
          
    output_filename = os.path.join("output", os.path.basename(filename).replace(".txt", "_annotated.txt"))
    with open(output_filename, 'w') as output_file:

        for phrase in phrases:
            pattern = r"(\w+)\s+(le|la|l'|les)\s+(\w+)"
            matches = re.findall(pattern, phrase, re.IGNORECASE)
            
            for match in matches:
                mot_precedent, determinant, mot_suivant = match
                fonction = determiner_fonction(mot_precedent.lower())
                
                if fonction == "Article_Défini":
                    determinant = "<article_def>" + determinant + "</article_def>"
                    if determinant in occurrences_articles:
                        occurrences_articles[determinant.lower()] += 1
                    else:
                        occurrences_articles[determinant.lower()] = 1
                elif fonction == "Pronom_Personnel":
                    determinant = "<pronom>" + determinant + "</pronom>"
                    if determinant in occurrences_pronoms:
                        occurrences_pronoms[determinant.lower()] += 1
                    else:
                        occurrences_pronoms[determinant.lower()] = 1
                        
        for article, occurrence in occurrences_articles.items():
            output_file.write(f"<Article_def>{article}</Article_def>\n")
        for pronom, occurrence in occurrences_pronoms.items():
            output_file.write(f"<Pronom>{pronom}</Pronom>\n")
    
    print(f"Annotations terminées pour {filename}. Résultats enregistrés dans {output_filename}.")

if __name__ == "__main__":
    if not os.path.exists("output"):
        os.makedirs("output")
        
    for filename in glob.glob("src/*.txt"):
        annoter_fichiers(filename)
