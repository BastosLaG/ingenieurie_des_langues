import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import random

def generate_dataset():
    # Listes d'avis factices
    avis_positifs = [
        "Ce jeu est incroyable, je ne peux pas m'arrêter d'y jouer !",
        "Des heures de plaisir garanties avec ce jeu.",
        "Les développeurs ont vraiment fait du bon travail avec ce jeu.",
        "Je recommande ce jeu à tous mes amis, c'est un vrai bijou !",
        "Une expérience de jeu immersive et captivante.",
        "Ce jeu est incroyable !",
        "J'ai adoré ce jeu, les graphismes sont superbes.",
        "Très bon gameplay, je recommande vivement !",
        "Un must-have pour tous les fans de jeux vidéo.",
        "Excellente histoire et personnages bien développés."
    ]

    avis_negatifs = [
        "Évitez ce jeu à tout prix, c'est une véritable catastrophe.",
        "Je me suis ennuyé dès les premières minutes de jeu.",
        "Les bugs et les problèmes de performance rendent ce jeu injouable.",
        "Un gaspillage d'argent complet, je regrette mon achat.",
        "Ce jeu est tellement mauvais que je l'ai désinstallé après quelques minutes.",
        "Je suis très déçu par ce jeu, il est ennuyeux.",
        "Les contrôles sont médiocres, je ne recommande pas.",
        "Graphismes décevants, le jeu est daté.",
        "J'ai trouvé ce jeu très frustrant et mal conçu.",
        "Une grosse déception, je regrette mon achat."
    ]

    # Création du jeu de données
    avis = []
    labels = []

    # Ajout d'avis positifs
    for _ in range(50):
        avis.append(random.choice(avis_positifs))
        labels.append('+')

    # Ajout d'avis négatifs
    for _ in range(50):
        avis.append(random.choice(avis_negatifs))
        labels.append('-')

    # Mélange des données
    data = list(zip(avis, labels))
    random.shuffle(data)

    # Création du DataFrame pandas
    df = pd.DataFrame(data, columns=['Avis', 'Sentiment'])

    return df

def del_useless_info(filename: str) -> str:
    """_summary_
    Args:
        filename (str): database originel
    """
    file_out = 'database/new_test.csv'
    df = pd.read_csv(filename)
    if 'Test' not in df.columns:
        df['Test'] = ''
    
    df = df[['Note', 'Test', 'Avis' ]]
    df['Avis'] = df['Avis'].str.lower()
    df['Note'] = df['Note'].str[:2]

    df['Note'] = df['Note'].str.replace('/', '')
    df = df[~df['Note'].isin(['[]', ''])]
    df['Note'] = df['Note'].astype(int)
    df = df[(df['Note'] <= 5) | (df['Note'] >= 15)]
    
    df['Test'] = df['Note'].apply(lambda x: '-' if x <= 5 else '+')
    df = df[['Test', 'Avis']]

    df.to_csv(file_out, index=False)
    return file_out

def train_model(filename):
    filename = del_useless_info(filename)

    df = pd.read_csv(filename)

    X_train, X_test, y_train, y_test = train_test_split(df['Avis'], df['Test'], test_size=0.2, random_state=42)

    vectorizer = TfidfVectorizer()
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)

    modele = LogisticRegression()
    modele.fit(X_train_tfidf, y_train)

    predictions = modele.predict(X_test_tfidf)
    print(classification_report(y_test, predictions))

    return vectorizer, modele

def predict_sentiment(vectorizer, modele, texte):
    texte_tfidf = vectorizer.transform([texte])
    prediction = modele.predict(texte_tfidf)

    if prediction[0] == '+':
        return "positif"
    else:
        return "négatif"

def main():
    total = 0
    nb_erreurs = 0
    filename_noise = "database/jeux_avis_populaire.csv"
    vectorizer, modele = train_model(filename_noise)

    exemple_texte = "Ce jeu est incroyable, j'ai adoré !"
    sentiment = predict_sentiment(vectorizer, modele, exemple_texte)

    print(f"Le sentiment du texte est {sentiment}.")

    # Exemple d'utilisation de la fonction
    jeux_video_df = generate_dataset()
    print(jeux_video_df.head())
    for _, row in jeux_video_df.iterrows():
        total += 1
        prediction = predict_sentiment(vectorizer, modele, row['Avis'])
        if prediction != row['Sentiment']:
            nb_erreurs += 1
        print(f"Le sentiment du texte est {prediction}. Étiquette réelle : {row['Sentiment']}")

    pourcentage_erreurs = (nb_erreurs / total) * 100
    print(f"Pourcentage de réussite : {pourcentage_erreurs}%")

if __name__ == "__main__":
    main()
