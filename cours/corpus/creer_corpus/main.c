#include "corpus.h"

int main (int argc, char *argv[])
{
    int choix;
    printf("\n      *|       Création corpus HTML        |*\n                ________________________\n");   
	while(1)
	{            
		switch(choix=menu())
		{        		
			case 1:
			{
				printf("\n*****************************************\n Réalisation du corpus \n*****************************************\n\n");
				char fichier_dictionnaire[150]="./dictionnaires/lexique_corpus_sans_doublons.txt";
				char rep_fin[150]="./fichiers/corpus/";
				// if(confirmer()==1)
				{
					
					faire_corpus(fichier_dictionnaire,rep_fin);
				}                                        
				break;
			}		
			default:
			{
				puts("choix incorrect");
			}
		} 
	}    	
  return 0;
}

/*************************************************************/
/*MENU*/
/*************************************************************/
int menu(void)
{
	int reponse;
	printf("\n\n\n*****************************************\n CHOIX FONCTIONALITES\n*****************************************\n\n");
	puts(" 1 Realisation corpus (100 res par mot du lexique maladie vulve)   -> OK");
	puts(" 0 Quitter le programme");
	printf("\n Choix : ");
	scanf("%d", &reponse);
	printf("\n");
	return reponse;	
}
