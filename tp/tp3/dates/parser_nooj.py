import subprocess

def importer_fichier_texte_avec_nooj(fichier_texte, projet_nooj):
    # Commande d'importation de fichier texte dans NooJ
    commande_nooj = ['noojcmd', '-p', projet_nooj, '-run', 'IMPORT_FILE', '-file', fichier_texte]
    
    # Exécution de la commande avec subprocess
    try:
        subprocess.run(commande_nooj, check=True)
        print("Fichier texte importé avec succès dans NooJ.")
    except subprocess.CalledProcessError as e:
        print("Erreur lors de l'importation du fichier texte dans NooJ :", e)

# Exemple d'utilisation
fichier_texte = "src/text.txt"
projet_nooj = "src"

importer_fichier_texte_avec_nooj(fichier_texte, projet_nooj)
