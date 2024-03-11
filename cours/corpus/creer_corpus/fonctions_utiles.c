#include "corpus.h"

#include <stdio.h>
#include <sys/types.h>
#include <dirent.h>
#include <sys/stat.h>
#include <string.h>
#include <locale.h>
#include <time.h>

int supprimer_archive(char const *chemin)
{
    DIR* rep = opendir(chemin);
    struct dirent* f = NULL;
 
    char *nouveau_chemin = NULL;
 
    while ((f = readdir(rep)) != NULL)
    {
        if(strcmp(f->d_name, ".") && strcmp(f->d_name, ".."))
        {
            nouveau_chemin = malloc(strlen(chemin)+strlen(f->d_name)+2);
            sprintf(nouveau_chemin, "%s/%s\0", chemin, f->d_name);
 
            if (strchr(f->d_name, '.') != NULL) // S'il y a un point il y a une extension -> c'est donc un fichier
                remove(nouveau_chemin); // On supprime le fichier
            else // C'est un dossier
                supprimer_archive(nouveau_chemin); // On fait un appel r�cursif
 
            free(nouveau_chemin);
        }
    }
    rmdir(chemin); // On supprime le dossier
 
    closedir(rep);
}
 
char *concatene(char *str, const char *s)
{
   int	iter;
   char	*fin;
  
   if (str == NULL)
    return (NULL);
    
   iter = -1;
   fin = malloc((strlen(str) + strlen(s) + 1) * sizeof(char));
  
   while (++iter < (signed)strlen(str))
      fin[iter] = str[iter];
    
   iter = -1;
  
   while (++iter < (signed)strlen(s))
      fin[strlen(str) + iter] = s[iter];
  
   fin[strlen(str) + iter] = '\0';
   str = fin;

  return (str);;
}

char *saisir_mot(int lign, int taille, char * fichier)
{
     char ligne[taille];
     char *mot;
     FILE *fichier_recherche = fopen ( fichier, "r" );
        
     while ( fgets ( ligne, sizeof ligne, fichier_recherche ) != NULL ) 
      {
               mot = ligne;
      }    
   
   return mot;
}

char *chemin_dossier (char *path)
{
    char *sin = path;
    char *sub = strrchr (path, '/');
    
     if (sin != NULL && *sin != 0 && sub != NULL && *sub != 0)
       {
          char *p = strstr (sin, sub);
     
          if (p != NULL)
          {
             memmove (p, p + strlen (sub), strlen (p) - strlen (sub) + 1);
          }
       }
    
       sprintf(sin,"%s/",sin);  //concatener dans la m�moire le nom de fichier avec ajout de /  
 
    return sin;
}


void wait(long sec) /* fonction wait() */
{
  long debut, actuel;  
 
  time(&debut) ;  
  time(&actuel) ;
  
  while((actuel-debut)<sec)  
      time(&actuel) ;
  
}

int confirmer()
{
    int choix = 0;

    while (choix < 1 || choix > 2)
    {
        printf("\t\t\t\t === Confirmer ? === \n");
        printf("1 : OUI\t\t\t\t\t\t\t\t\t2: NON\n");
        printf("\t\t\t\t       Choix : ");
        scanf("%d", &choix);
        if (choix == 1) { return 1;}
        if (choix == 2) { printf("Retour au programme"); return 2;}
    }

    return choix;
} 


void supprime(char *texte, char x)   // supprime x dans la chaine
{
int p ,i;
for(i=0;texte[i] != '\0';i++)
  {if (texte[i] == x)  // on a trouve
       {
        for(p=i;texte[p]!=0;p++)
        texte[p]=texte[p+1];
       }
   }
} 

#define NUL '\0'
char *trim(char *str)
{
char *ibuf = str, *obuf = str;
int i = 0, cnt = 0;
if (str)
{
for (ibuf = str; *ibuf && isspace(*ibuf); ++ibuf)
;
if (str != ibuf)
memmove(str, ibuf, ibuf - str);
while (*ibuf)
{
if (isspace(*ibuf) && cnt)
ibuf++;
else
{
if (!isspace(*ibuf))
cnt = 0;
else
{
*ibuf = ' ';
cnt = 1;
}
obuf[i++] = *ibuf++;
}
}
obuf[i] = NUL;
while (--i >= 0)
{
if (!isspace(obuf[i]))
break;
}
obuf[++i] = NUL;
}
return str;
} 
