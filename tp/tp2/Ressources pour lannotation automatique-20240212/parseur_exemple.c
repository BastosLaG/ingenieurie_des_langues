//***********************exemple parseur en C
//****** $gcc parseur.c

// ***** $./a.out mon_text.txt sortie.xml




#include <stdio.h>
#include <stdlib.h>
#include <string.h>


int main(int argc, char* argv[]){
char tp[9000];
char tq[9000];
char gnom;
FILE* ent = fopen(argv[1], "r");
FILE* sortie = fopen(argv[2], "w+");	
int T = 0;
int bu = 0;

   fputs("<?xml version=\"1.0\" encoding=\"ISO-8859-1\"?>", sortie);
   fputs("<text>", sortie);

while ((gnom = fgetc(ent)) != EOF ){	
   if ((int)gnom == 10||(int) gnom == 13) {	
     gnom = ' ';
     T++;
     tp[T-1] = gnom; 
}

if ( (int)gnom == 46 && (int)tp[T-1] == 77) {	
   T++;
   tp[T-1] = gnom; 
}
//***********************************		
else if ((int)gnom == 63 || (int) gnom == 33 || (int)gnom == 46 ){

   fputs("<p>", sortie);
   int i;
   for (i = 0; i < T; i++){		
   fputc(tp[i], sortie);
}		
   fputc(gnom, sortie);
   fputs("</p>", sortie); 
   strncpy(tq, tp, T);
   bu = T;
   T = 0;
}

//*********************************************		
else {			
  T++;
  tp[T-1] = gnom;
  }

}

  fputs("</text>", sortie);
  fclose(ent);
  fclose(sortie);	

return 0;}
