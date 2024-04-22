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
    file_out = 'database/label_avis.csv'
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
    debug = False
    total = 0
    nb_erreurs = 0
    filename_noise = "database/jeux_avis_populaire.csv"
    vectorizer, modele = train_model(filename_noise)

    # Exemple d'utilisation de la fonction
    jeux_video_df = generate_dataset()
    print(jeux_video_df.head())
    for _, row in jeux_video_df.iterrows():
        total += 1
        prediction = predict_sentiment(vectorizer, modele, row['Avis'])
        if prediction != row['Sentiment']:
            nb_erreurs += 1
        if debug :print(f"Le sentiment du texte est {prediction}. Étiquette réelle : {row['Sentiment']}")

    pourcentage_erreurs = (nb_erreurs / total) * 100
    print(f"Pourcentage de réussite : {pourcentage_erreurs}%")

    ###################################################################################################
    ################################### Exemple hors jeu de test ######################################
    # prediction = predict_sentiment(vectorizer, modele, "Echecs, Reverso, jeu de cartes, dames et tellement d'autres condensés dans un seul titre, tous jouables en ligne. Tabletop Simulator aurait pu se contenter d'être une compilation de jeux de société (ce qui aurait été déjà sympathique) mais c'était sans compter sur une ambition immensément plus grande : la liberté. Libre de leurs mouvements, les joueurs peuvent faire ce qu'ils veulent dans l'ordre qu'ils entendent. Grâce à une physique assez bien foutue on déplace nos pions et jetons façon réalité simulée. Tous les outils et éléments de jeu sont mis à notre disposition pour en faire absolument ce que l'on veut. Au diable le poker et vive le président, le pouilleux et le menteur ! Le revers de la médaille est que l'excès de liberté peut malheureusement parfois tourner à la roue libre. Dégommer toutes les pièces, jeter violemment son cavalier contre sa tour, renverser la table...tous les excès de violence sont possibles et il faudra ainsi s'entourer d'amis qui savent se tenir pour profiter pleinement d'une partie. Sans discipline le carnage n'est pas loin. C'est alors qu'on a envie de voir les baffes pleuvoir. Comme en vrai.La prise en main assez délicate au premier contact, une fois adoucie par un petit tour de didacticiel, devient d'une parfaite intuitivité passée l'heure de jeu. L'aspect technique dépouillé et les arrière-plans ♥♥♥♥♥♥♥♥♥♥♥♥♥ se font très vite oublier pour se plonger tête la première dans l'ambiance de chaque partie. Le contenu (personnalisable) est potentiellement infini ; à vous de piocher dans les règles pré-établies ou d'utiliser les plateaux et les dés pour jouer à vos jeux favoris. D'une partie de Uno à un Monopoly spécial gangs de Marseille crossover Futurama, le champs du possible déjà extrêmement large promet de s'élargir encore plus grâce au modding et au workshop. Instable à l'heure de son early access, Tabletop Simulator est déjà une franche réussite pleine de promesses, un concentré de fous-rires pour peu que l'on s'entoure des bonnes personnes. Sinon il reste les curly. Si le trailer vous donne envie alors foncez : c'est exactement ce que vend et vaut le jeu.")
    # print(f"Le sentiment du texte est {prediction}. Étiquette réelle : +")

    # prediction = predict_sentiment(vectorizer, modele, "Tu achètes 4000 jeux de sociétés pour le prix de 1. Tu ajoutes du fun en plus. Tu ajoutes aussi des amis. Et pouf, ç a fait un ♥♥♥♥♥♥ de super jeu.")
    # print(f"Le sentiment du texte est {prediction}. Étiquette réelle : +")

    # prediction = predict_sentiment(vectorizer, modele, "je pige que dalle , encore un achat pour rien , marre !")
    # print(f"Le sentiment du texte est {prediction}. Étiquette réelle : -")

    # prediction = predict_sentiment(vectorizer, modele, "Table top simulator est ni plus ni moins qu'une coquille vide composée d'un moteur codé a la va vite, il ne vit que par le travail bénévole des moddeurs qui proposent des adaptations de jeu protégés par la propriété intellectuelle. Je ne vous parle même pas des freeze incessants, des crash et des bugg sur un PC pouvant faire tourner les derniers triple A en ultra. La décence voudrait que ce jeu soit gratuit, ou du moins ne pas dépasser les 5€.")
    # print(f"Le sentiment du texte est {prediction}. Étiquette réelle : -")
    ###################################################################################################

    # Partie utilisateur
    user_avis = ""
    while user_avis.lower() not in ['q', 'quit']:
        print("\nEntrez votre avis sur un jeu vidéo (ou tapez 'q' ou 'quit' pour quitter) : ")
        user_avis = input().strip()
        if user_avis.lower() not in ['q', 'quit']:
            print("\nEntrez le sentiment associé à votre avis (positif ou négatif) : ")
            user_sentiment = input().strip()

            prediction = predict_sentiment(vectorizer, modele, user_avis)
            print(f"\nLe sentiment prédit pour votre avis est : {prediction}")

            if prediction == user_sentiment:
                print("La prédiction a réussi !")
            else:
                print("La prédiction a échoué...")
        else:
            print("Au revoir !")

if __name__ == "__main__":
    main()
