
#include <locale.h>
#include "corpus.h"
#include <curl/curl.h>

int recuperer_contenu_site_corpus(char *recherche, char *nom_fichier_fin_sites, int nbr_source)
{
   int nbr,nbr_site=1, i=0,nombre_caract_ligne=128;
   char *balise_debut2, *debut2, * recherche2;
   char ligne [1024]; 
   int temp = nbr_site, compt = 10;
     
   nbr = floor(nbr_source / 10);  // calcul du nombre de page � r�cuperer       
   recherche = concatene(recherche,"&start=0");  //ajout de la dizaine des pages � r�cup 
   //recherche = concatene(recherche,"&lang=fr");  //ajout de la dizaine des pages � r�cup 
   wait(1);             	
   FILE * fichier_final = fopen (nom_fichier_fin_sites, "wb");      //cr�ation du fichier final
	
   if(fichier_final != NULL)
   {
	CURL *session = curl_easy_init(); 
	curl_easy_setopt(session, CURLOPT_URL,recherche);   
	curl_easy_setopt(session,  CURLOPT_WRITEDATA, fichier_final); //ligne pas fichier_final ?
	curl_easy_setopt(session,  CURLOPT_WRITEFUNCTION, fwrite);
	curl_easy_perform(session);
	fclose(fichier_final);    	
	curl_easy_cleanup(session);
        printf("Source Google %s extrait dans %s \n", recherche, nom_fichier_fin_sites);             
     
    if(nbr >1)  //si plusieurs page � r�cup => >10 sources
    {
        
        for(i=1;i<=nbr; i++)
        {
          FILE * fichier_final = fopen (nom_fichier_fin_sites, "ab");      //cr�ation du fichier final
          char lien_recup[1024]={0}; 
          sprintf(lien_recup,"%s%d",recherche,compt);  //concatener dans la m�moire le nom de fichier
          CURL *session = curl_easy_init();             
     	  curl_easy_setopt(session, CURLOPT_URL,lien_recup);
       	  curl_easy_setopt(session,  CURLOPT_WRITEDATA, fichier_final); //ligne pas fichier_final ?
    	  curl_easy_setopt(session,  CURLOPT_WRITEFUNCTION, fwrite);
          curl_easy_perform(session);            
          fclose(fichier_final); 	   	
      	  curl_easy_cleanup(session);
      	  wait(1); 
          printf("Source Google %s extrait dans %s \n", lien_recup, nom_fichier_fin_sites);                                  
          compt=compt+10;
       
       }                
                   
    } 
    wait(1); //d�lai pour �tre sur de ne rien oublier
   }      
  return 0;
}

/****************************************************************************************************/
/********fonction recuperant avec libcurl le contenues de sites stock�es dans un fichier ************/
/***************************************************************************************************/
int recuperer_contenu_site_diff(char *lien, char *nom_fichier_fin_sites)
{
   int nbr_site=1, i=0,nombre_caract_ligne=128;
   char *balise_debut,*debut, *balise_debut2, *debut3, *balise_debut3, *debut2,*balise_debut4, *debut4, *balise_debut5, *debut5,*balise_debut6, *debut6;
   char ligne [1024];
   int temp = nbr_site;   
   FILE *fichier_lien = fopen ( lien, "r" );   

   if ( fichier_lien != NULL )
   { 
     /*site a exclure*/
     balise_debut = "forum";   
     balise_debut2 = ".pdf";
     balise_debut3 = ".doc\n";
     balise_debut5 = ".RTF";
     balise_debut4 = "facebook";
     balise_debut6 = "larousse";
     while ( fgets ( ligne, sizeof ligne, fichier_lien ) != NULL ) 
     {   
         char *output = malloc(strlen(ligne)+1);
         urldecode2(output, ligne);
        // printf("\n\n %s", output);
         
       debut = strstr(ligne, balise_debut);     
      debut2 = strstr(ligne, balise_debut2);
      debut3 = strstr(ligne, balise_debut3);
      debut4 = strstr(ligne, balise_debut4);
      debut5 = strstr(ligne, balise_debut5);
      debut6 = strstr(ligne, balise_debut6);

       if(debut)
        {
               printf("-Les forums ne sont pas r�cup�r�s\n");
        }
        else if(debut2)
        {
               printf("-Les fichiers .pdf ne peuvent pas etre traites\n");
        }
        else if(debut3)
        {
               printf("-Les fichiers .doc ne peuvent pas etre traites\n");
        }
         else if(debut4)
        {
               printf("-Les sites facebook ne peuvent pas etre traites\n");
        }
         else if(debut5)
        {
               printf("-Les fichiers RTF ne peuvent pas etre traites\n");
        }
          else if(debut6)
        {
               printf("-Les fichiers provenant du site Larousse ne peuvent pas etre traites\n");
        }
        else
        {
         
            char fichier_final_nom[255]={0};                      
            CURL *session = curl_easy_init(); 
            curl_easy_setopt(session, CURLOPT_URL,output);        	
            sprintf(fichier_final_nom,"%s%d.html",nom_fichier_fin_sites,nbr_site);  //concatener dans la m�moire le nom de fichier    
            FILE * fichier_final = fopen (fichier_final_nom, "w");      //cr�ation du fichier final
	    if(fichier_final ==0) 
		 printf("erreur\n");
	    curl_easy_setopt(session,  CURLOPT_WRITEDATA, fichier_final); //ligne pas fichier_final ?
	    curl_easy_setopt(session,  CURLOPT_WRITEFUNCTION, fwrite);
	    curl_easy_perform(session);
	    fprintf(fichier_final,"\r\n"); 
	    fclose(fichier_final);    	
	    curl_easy_cleanup(session);
            printf("Site web %d extrait dans %s \n", nbr_site, fichier_final_nom);         
            wait(1); //d�lai pour �tre sur de ne rien oublier
         }
         nbr_site++;
         i++;
      }
      fclose ( fichier_lien );
   }
   else
   {
      perror ( lien ); 
   }
    
	return 0;
}



/******************************************************************************************/
/********fonction nettoyant une page google pour conserver uniquement les liens************/
/******************************************************************************************/
int conserver_lien(char * nom_fichier, char * nom_fichier_2, int nombre_source)
{
   FILE *fichier, *fichier_2;
   long taille_fichier;
   char *buffer, *taille_lien, *debut, *fin, *balise_debut, *balise_fin;       
   int compt=0;
   fichier = fopen( nom_fichier , "rb");       //ouverture du fichier pour le mettre dans le buffer
   
   if (fichier == NULL)                        //si fichier vide, erreur
      return 1;
  
   fseek (fichier, 0 , SEEK_END);              // determine la taille du fichier
   taille_fichier = ftell (fichier);
   rewind (fichier);
  
   buffer =  malloc (taille_fichier+1);   //allocation m�moire pour le buffer d
   
   if (buffer ==  NULL)                        //si buffer vide, erreur
      return 2;
 
   fread (buffer, 1, taille_fichier, fichier); // copie du fichier dans le buffer/tampon 
   
   balise_debut = "<h3 class=\"r\"><a href=\"/url?q=";    //meilleur recherche mais retirer 1000
   balise_fin = "&amp";
  
   fichier_2 = fopen(nom_fichier_2, "w");                 // fichier final contenant uniquement les liens 
   debut = strstr(buffer, balise_debut);           //recherche dans le buffer de la balise <cite> contenant les liens       
  
   while(debut)                                    // boucle pour traiter tout les liens de la page
   { 
        compt++;
        fin = strstr(debut, balise_fin);           //indication de la fin de balie pour sauvegarder le lien contenu       
        debut = debut + strlen(balise_debut)-1;    //suppression de la balise pour la retirer du lien             
        taille_lien = (char*)(fin -  debut) -1;   //calcul de la taille du lien
        if(compt<=nombre_source)
        {             
            while( taille_lien !=0)        
            { 
               taille_lien--;
               debut++;                         
               fprintf(fichier_2, "%c", *debut);      //stockage des liens dans le fichier texte
            } 
            fprintf(fichier_2, "\n");                 //saut de ligne pour chaque liens
        }     
        debut=strstr(fin,balise_debut);               //indication du nouveau d�but
	/*if(debut)
	{
	balise_debut="</html>";
	debut=strstr(fin,balise_debut);
	}*/
	
    }
    fclose(fichier_2); //fermeture du fichier
    fclose (fichier);  
    free(buffer);      // lib�ration du buffer
  
    return 3;      
}



/****************************************************************************************************/
/********fonction realisant un corpus � partir d'un fichier dictionnaire ****************************/
/***** extrait chaque ligne formant le mot clef de recherche google, recuperation des sources********/
/***************************************************************************************************/
int faire_corpus(char *fichier_dico, char *nom_rep_corpus)
{
   int nbr_site=1,nombre_caract_ligne=128;
   char ligne [1024];
   int nombre_source = 10;
   printf ("Nombre de sources par ligne du lexique � r�cup�rer : "); 
   scanf ("%d", &nombre_source);                           
  
   int recup_sites;

   supprimer_archive(nom_rep_corpus); //supprime les anciennes donn�es
   mkdir(nom_rep_corpus,0777);  
   FILE *fichier_lien = fopen ( fichier_dico, "rb" );	//ouverture du lexique expert
   unsigned char *cp_ligne=NULL;

   if ( fichier_lien != NULL )
   { 
     while ( fgets ( ligne, sizeof ligne, fichier_lien )) 
     {  
	//int taille_mot = strlen (ligne);     
	int i;
	char *aux;
	char dossier[255]={0};
	char source_google[255]={0};
	char source_lien_google[255]={0};
	char source_lien_connaissance[255]={0};
	int taille_mot=strlen(trim(ligne));
	
	cp_ligne = malloc(taille_mot);
	cp_ligne = ligne;
	//setlocale(LC_ALL,"");

        printf("\nMot du lexique des maladies de la vulve: %s \nRecuperation de %d sources pour ce mots\n\n", ligne, nombre_source);
	/*remplacement des espaces par des + conforme � une requ�te type Google*/
	for ( i = 0; i <= taille_mot; i++)
	{
	  if ((ligne[i] == ' '))
	  {
	    ligne[i] = '+';
	  }
	}
	
	//char * recherche_ajout;
	//recherche_ajout=saisie_requete();
	/*PRECISER DOMAINE DE RECHERCHE DU CORPUS ICI*/
        aux=concatene("http://www.google.fr/search?q=gyn�cologie+",ligne);
        sprintf(dossier,"./fichiers/corpus/%s",cp_ligne);        //concatener dans la m�moire le nom de fichier       
        wait(1);
        mkdir(dossier,0777);  				//cr�ation du dossier portant le nom de la ligne extraite du lexique
        sprintf(source_google,"%s/source_google.html",dossier);  //concatener dans la m�moire le nom de fichier
        recuperer_contenu_site_corpus(aux,source_google, nombre_source);   //R�cup�ration du source google
       //free(cp_ligne);
        sprintf(source_lien_google,"%s/lien_source_google.txt",dossier);  //concatener dans la m�moire le nom de fichier    
        conserver_lien(source_google, source_lien_google, nombre_source);  //extraction des liens du source google
        sprintf(source_lien_connaissance,"%s/lien_",dossier);  //concatener dans la m�moire le nom de fichier  
        recup_sites = recuperer_contenu_site_diff(source_lien_google, source_lien_connaissance); //recuperation du contenu des liens
      }
      fclose ( fichier_lien );
   }
   else
   {
      perror ( fichier_dico ); 
   }
    free(cp_ligne);
	return 0;
}




void urldecode2(char *dst, const char *src)
{
        char a, b;
        while (*src) {
                if ((*src == '%') &&
                    ((a = src[1]) && (b = src[2])) &&
                    (isxdigit(a) && isxdigit(b))) {
                        if (a >= 'a')
                                a -= 'A'-'a';
                        if (a >= 'A')
                                a -= ('A' - 10);
                        else
                                a -= '0';
                        if (b >= 'a')
                                b -= 'A'-'a';
                        if (b >= 'A')
                                b -= ('A' - 10);
                        else
                                b -= '0';
                        *dst++ = 16*a+b;
                        src+=3;
                } else {
                        *dst++ = *src++;
                }
        }
        *dst++ = '\0';
}



/*****************************************************************************************************/
/**fonction permettant de saisir une recherche et de formuler directement le lien de recherche Google*/
/**************************************************************************************************/
char * saisie_requete()
{      
    char buffer[256];
    char caractere;
 //   char * host_rech="http://www.google.fr/search?q=";
   int n;
   FILE *fichier, *fichier_fin;  
  
  
   n = read (STDIN_FILENO, buffer, sizeof buffer-1);
 
   if (n >= 0)
   {

      buffer[n] = 0; 
   }
   supprime(buffer, '\n');
   supprime(buffer, 65);              

  // fichier = fopen( fichier_mots_requete , "w");       //ouverture du fichier pour le mettre dans le buffer
  // fprintf(fichier, "%s\0", buffer);
   //fprintf(fichier, "\0");
   //fclose (fichier);  
char *domaine_saisie=NULL;
domaine_saisie=malloc(strlen(buffer)+1);                            

  domaine_saisie=buffer;
  //Creation de la requete pour le moteur de recherche Google

  // fichier_fin = fopen (requete_ini, "w");

   //fichier = fopen( fichier_mots_requete , "rw");
    

  // fprintf(fichier_fin, "%s", host_rech);

        size_t i=0;       
  // while (i<=strlen(domaine_saisie))
   for(i=0;i<=strlen(buffer);i++);

   {
      //  caractere = fgetc(fichier);        //lecture caractere par caractere du fichier
       

        if((domaine_saisie[i]==' '))
        { 
         domaine_saisie[i]='+';  

        }
       // fprintf(fichier_fin, "%c", caractere);

   }      
// domaine_saisie[i++]="+";    

  // fclose(fichier_fin);

  // fclose (fichier);  
return domaine_saisie;
}



