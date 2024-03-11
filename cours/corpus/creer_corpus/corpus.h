#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <locale.h>
#include <wchar.h>
#include <math.h>
#if defined (WIN32)
#include <winsock2.h>
#elif defined (linux)
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>

#define SOCKET_ERROR -1
#define closesocket(s) close (s)
typedef int SOCKET;
typedef struct sockaddr_in SOCKADDR_IN;
typedef struct adresse_socket SOCKADDR;
#endif

#include <dirent.h>

#ifndef WIN32
    #include <sys/types.h>
#endif

#define PORT 80


//liste des fonctions du projet
/*char *chemin_dossier (char *chemin);
char *nom_fichier (char *path);
int enregistre_mot_clefs(char *chaine);
*/
//etape1
/*
int recuperer_google_lib(char *lien, char *recherche  );

//etape 2
int conserver_lien(char * nom_fichier, char * nom_fichier_2,int nombre_source);
int supprimer_toute_balise(char *nom_fichier_balise, char*fichier_lien_seul_fin);
char * recuperer_requete(char *requete_ini);

//etape 3
int recuperer_contenu_site(char *lien, char *nom_fichier, int nbr_source);

//etape 4
int recherche_mots_clefs(char * fichier_traiter_mot, char * nom_fichier_2, char *recherche);
int remplace_fichiers_accent(char * nom_dossier); 
int remplace_accent_maj(char * fichier_traiter_mot);
int  recherche_fichiers_mot (char * nom_dossier, char *destination, char *recherche);
int recherche_titre(char * nom_fichier);
int recherche_web_lien(char * nom_fichier);

//questionnaire
char *initialise_recherche(char *recherche);
char * saisie_rep(char * recherche, char* mots);
char * saisir_mot(int ligne, int taille, char * fichier);
int effectuer_res(char * nom_dossier, char *destination, char * recherche);


int compter_caract_ligne(char *fichier, int ligne);


void LireChaine(char chaine[], int size);

int clear_input_buffer(void);
void saisie_requete(char * fichier_mots_requete, char *requete_ini);

void stripSpaces( char *x );
void vider_stdin(void);
void del_char(char* str, char c);

int supprimer_style_html(char * nom_fichier, char * nom_fichier_2);
int supprimer_script_html(char * nom_fichier, char * nom_fichier_2);
int nettoyer_saut_espace(char * nom_fichier, char * nom_fichier_2);
int nettoyer_saut_espace2(char * nom_fichier, char * nom_fichier_2);



char * remplace(char * entrer, char car_rech, char car_remp);
void recherche_saut_ligne(char * fichier_sans_balise );
int nettoyer_html(char * rep_convert, char * fichier_fin,char * fichier_aux);
int reorganise_texte(char * nom_fichier, char * nom_fichier_2);
int supprime_carac_spe(char * nom_fichier, char * nom_fichier_2);
int supprime_espace(char * nom_fichier, char * nom_fichier_2);
int supprimer_comment(char * nom_fichier, char * nom_fichier_2);
int cherche_corp_texte(char * nom_fichier, char * nom_fichier_2); 

int remplace_html_code(char * fichier, char * nom_fichier_2);
int supprimer_value(char * nom_fichier, char * nom_fichier_2);

int compter_mots_fichiers(char * rep_convert,char * nom_fichier_mot, char * nom_fichier_2,  char * nom_fichier_3);
int compter_mots_corpus(char * rep_convert,char * nom_fichier_mot, char * nom_fichier_2,  char * nom_fichier_3);

void urldecode2(char *dst, const char *src);
int annoter_texte(char *rep_annote, char *fichier_mots, char *fichier_resultat);

int count_entries(char * repertoire);
int nettoyer_corpus(char * rep_convert, char * fichier_resultat,char * fichier_aux);

*/
void supprime(char *texte, char x) ;
char * saisie_requete();
void wait(long sec);
char *concatene(char *str, const char *s);

static void envoyer (SOCKET socket, char const *partie);
int client (char * nom_f, char * recherche);
int recuperer_contenu_site_diff(char *lien, char *nom_fichier_fin_sites);
void supprime(char *texte, char x);
int faire_corpus(char *lien, char *nom_fichier_fin_sites);
char *trim(char *str);
int confirmer();
int menu(void);
int supprimer_archive(char const *name);
int recuperer_contenu_site_corpus(char *recherche, char *nom_fichier_fin_sites, int nbr_source);
char* en_utf8(const unsigned char pref, const unsigned char *in);

void urldecode2(char *dst, const char *src);
