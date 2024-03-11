CC=gcc
CFLAGS = -W -g
PRG=creer_corpus
OBJ=main.o fonctions_utiles.o source_connaissances.o corpus.h

LFLAGS= 
LIBS= -L/usr/lib/x86_64-linux-gnu -lcurl -lm

all:	$(PRG)

source_connaissance.o :	source_connaissance.c corpus.h
	$(CC) $(LFLAGS) $(LIBS) -c source_connaissance.c corpus.h


fonctions_utiles.o : fonctions_utiles.c corpus.h
	$(CC) $(LFLAGS) $(LIBS) -c fonctions_utiles.c corpus.h

main.o : main.c corpus.h
	$(CC) $(LFLAGS) $(LIBS) -c main.c corpus.h

creer_corpus: $(OBJ)
	$(CC) -o creer_corpus  $(OBJ) $(LFLAGS) $(LIBS)

clean:
	rm -f *.o creer_corpus
