#include <stdio.h>

int verif (FILE * fichier, int n, int caractere)
{
	int i, c;
	int res;
	for (i = 0; i < n; i++)
	{
		c = fgetc(fichier);
		if(c == caractere)
			res = 1;
		else
		{
			fseek(fichier, -i-1, SEEK_CUR);
			return 0;
		}
	}
	return res;
}

void lire (FILE* fichier_s, FILE* fichier_d)
{
	int c, c_next, c_prec, var, phrase, boolean, dial;
	c = c_next = c_prec = var = phrase = boolean = dial = 0;

	fprintf(fichier_d, "<?xml version=\"1.0\" encoding=\"ISO-8859-1\"?>");
	fprintf(fichier_d, "<?xml-stylesheet href=\"/tel.xsl\" type=\"text/xsl\" ?>\n");
	fprintf(fichier_d, "<!DOCTYPE html PUBLIC \"-//W3C//DTD HTML 4.01//EN\" \"http://www.w3.org/TR/html4/strict.dtd\">\n\n\n");
	
	while((c = fgetc(fichier_s)) != -1)
	{
		switch(var)
		{
			case 0:
			//Debut d'une phrase
				if (phrase == 0)
				{
					fprintf(fichier_d, "<PHRASE>");
					phrase = -1;
					boolean = 1;
				}
				var = -1;
				break;
			case 1:
			//Debut ligne CHAPITRE
				fprintf(fichier_d, "<CHAPITRE>");
				var = 2;
				break;
			case 2:
			//Cloturer la fin du chapitre
				break;
			case 3:
			//Fin dialogue
				dial = 1;
				break;
			case 4:
				fprintf(fichier_d, "<PHRASE>");
				phrase = -1;
				var = -1;
				boolean = 1;
				break;
			case -1:
				break;
			default:
				var = 0;
				break;
		}
		switch(c)
		{
			case '.':
				if ((c_next = fgetc(fichier_s)) != -1 && c_next == '.')
				{
					if(dial == 1)
					{
						dial = 0;
						fprintf(fichier_d, "%c%c%c</DIALOGUE> </PHRASE>\n", c, c_next, c_next);
					}
					else
						fprintf(fichier_d, "%c%c%c</PHRASE>\n", c, c_next, c_next);
					fseek(fichier_s, 3, SEEK_CUR);
					phrase = 1;
					boolean = 0;
				}
				else 
					fseek(fichier_s, -1, SEEK_CUR);
				if((c_next = fgetc(fichier_s)) != -1 && c_next == ' ' && c_prec != 'M')
				{
					if(dial == 1)
					{
						dial = 0;
						fprintf(fichier_d, "%c</DIALOGUE> </PHRASE>\n", c);
					}
					else
						fprintf(fichier_d, "%c</PHRASE>\n", c);
					phrase = 1;
					boolean = 0;
				}
				else
					fseek(fichier_s, -1, SEEK_CUR);
				/*
				if ((c_next = fgetc(fichier_s)) != -1 && c_next == '\n')
				{
					phrase = 2; // Fin de phrase puis retour
				}
				*/
				break;
			case '!':
				if(dial == 1)
				{
					dial = 0;
					fprintf(fichier_d, "%c</DIALOGUE> </PHRASE>\n", c);
				}
				else
					fprintf(fichier_d, "%c</PHRASE>\n", c);
				phrase = 1;
				boolean = 0;
				break;
			case '?':
				if(dial == 1)
				{
					dial = 0;
					fprintf(fichier_d, "%c</DIALOGUE> </PHRASE>\n", c);
				}
				else
					fprintf(fichier_d, "%c</PHRASE>\n", c);
				phrase = 1;
				boolean = 0;
				break;
			case ':':
				if(dial == 1)
				{
					dial = 0;
					fprintf(fichier_d, "%c</DIALOGUE> </PHRASE>\n", c);
				}
				else
					fprintf(fichier_d, "%c</PHRASE>\n", c);
				phrase = 1;
				boolean = 0;
				break;
			case '-':
				if((c_next = fgetc(fichier_s) == '-'))
				{
					fprintf(fichier_d, "<DIALOGUE>%c", c);
					var = 3;
				}
				else
					fseek(fichier_s, -1, SEEK_CUR);
				break;
			case '\n':
				if(var == 2)
					fprintf(fichier_d, "</CHAPITRE>");
				if (verif(fichier_s, 4, '\n') > 0)
					var = 1;
				else
					var = 0;
				break;
			default:
				break;
		}

		if (phrase == 1)
			var = 4;
		else if (boolean == 1 && c == '\n')
			fprintf(fichier_d, " ");
		else
			fprintf(fichier_d, "%c", c);
		if(c_next == '\n' && phrase == 1)
		{
			fprintf(fichier_d, "\n<PHRASE>");
			phrase = -1;
			var = -1;
			boolean = 0;
		}
		c_prec = c;
	}
	fprintf(fichier_d, "</PHRASE>");
}

int main (int argc, char *argv[])
{
	if(argc != 3)
		fprintf(stderr, "pas le bon argument : progname filesource filedest\n");
	else
	{
		FILE* fichier_s = NULL;
    	fichier_s = fopen(argv[1], "r+");
    	FILE* fichier_d = NULL;
    	fichier_d = fopen(argv[2], "w+");
    	if (fichier_s != NULL)
    	{
    		lire(fichier_s, fichier_d);
    	}
    	else if (fichier_d == NULL)
    		printf("Impossible de créer le fichier %s", argv[2]);
    	else
    	    printf("Impossible d'ouvrir le fichier %s", argv[1]);
		printf("Operation reussi.\n");
		return 0;
	}
}
