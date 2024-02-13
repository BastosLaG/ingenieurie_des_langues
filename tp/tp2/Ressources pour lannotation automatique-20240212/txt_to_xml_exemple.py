#!/usr/bin/python
# -*- coding: utf-8 -*-


    #########################################################################################
  #############################################################################################
#################################################################################################
###                                                                                           ###
### txt_to_xml.py                                                                             ###
###                                                                                           ###
### This program extracts french non grammaticals words from txt file given as argument.      ###
### Extracted words and their frequencies are outted in a xml file.                           ###
###                                                                                           ###
#################################################################################################
  #############################################################################################
    #########################################################################################


#################################################################################################
#################################################################################################
##                                                                                             ##
## Modules importation                                                                         ##
##                                                                                             ##
#################################################################################################
#################################################################################################

import re
import sys


#################################################################################################
#################################################################################################
##                                                                                             ##
## Global variables definitions                                                                ##
##                                                                                             ##
#################################################################################################
#################################################################################################

#################################################################################################
##                                                                                             ##
## Global variables used as constants                                                          ##
##                                                                                             ##
#################################################################################################

# cette chaine contient tous les caractères miniscules en français
french_chars = "abcdefghijklmnopqrstuvwxyzàâæÇçéèêëîïôœùûüÿ"

# cette liste contient des mots grammaticaux en français
grammatical_words = [
'à', 'ainsi', 'ailleurs', 'alors', 'après', 'attendu', 'au', 'aucun', 'aucune', 'aucunes',
'aucuns', 'audit', 'aujourd', 'auprès', 'auquel', 'aussi', 'autre', 'autres', 'aux', 'auxdites',
'auxdits', 'auxquelles', 'auxquels', 'avant', 'avec', 'bien', 'bientôt', 'c', 'ça', 'car', 'ce',
'ceci', 'cela', 'celui', 'celle', 'cent', 'centième', 'centièmes', 'cents', 'certain',
'certaine', 'certaines', 'certains', 'certes', 'ces', 'cet', 'cette',  'chaque', 'chez', 'ci',
'cinq', 'cinquante', 'cinquantième', 'cinquantièmes', 'cinquième', 'cinquièmes', 'combien',
'comme', 'comment', 'concernant', 'contre', 'd', 'dans', 'davantage', 'de', 'demain', 'demi',
'demie', 'demies', 'demis', 'depuis', 'dernier', 'dernière', 'dernières', 'derniers', 'derrière',
'des', 'dès', 'desdites', 'desdits', 'desquelles', 'desquels', 'deux', 'deuxième', 'deuxièmes', 
'devant', 'différentes', 'différents', 'divers', 'diverses', 'dix', 'dixième', 'dixièmes',
'donc', 'dont', 'douze', 'douzième', 'douzièmes', 'du', 'dudit', 'duquel', 'durant', 'elle',
'elles', 'en', 'encore', 'enfin', 'ensuite', 'entre', 'envers', 'ès', 'et', 'eux', 'excepté',
'faux', 'gré', 'guère', 'hier', 'hormis', 'hors', 'hui', 'huit', 'huitième', 'huitièmes', 'ici',
'il', 'ils', 'j', 'je', 'jusqu', 'jusque', 'l', 'la', 'là', 'ladite', 'laquelle', 'le', 'ledit',
'lequel', 'les','lesdites', 'lesdits', 'lesquelles', 'lesquels', 'leur', 'leurs', 'loin',
'lorsqu', 'lorsque', 'lui', 'm', 'ma', 'maint', 'mainte', 'maintenant', 'maintes', 'maints',
'mais', 'mal', 'malgré', 'me', 'même', 'mêmes', 'mes', 'mien', 'mienne', 'miennes', 'miens',
'mille', 'milliard', 'milliardième', 'milliardièmes', 'millième', 'millièmes', 'million',
'millionième', 'millionièmes', 'moi', 'moins', 'mon', 'moyennant', 'n', 'ne', 'néanmoins',
'neuf', 'neuvième', 'neuvièmes', 'ni', 'non', 'nonante', 'nonantième', 'nonantièmes',
'nonobstant', 'nos', 'notre', 'nôtre', 'nous', 'nul', 'nulle', 'nulles', 'nuls', 'octante',
'octantième', 'octantièmes', 'on', 'onze', 'onzième', 'onzièmes', 'or', 'ou', 'où', 'oui',
'outre', 'par', 'parmi', 'partout', 'pas', 'pendant', 'plus', 'plusieurs', 'pour', 'pourquoi',
'pourtant', 'premier', 'première', 'premières', 'premiers', 'près', 'puis', 'puisque', 'qu',
'quand', 'quarante', 'quarantième', 'quarantièmes', 'quart', 'quarte', 'quartes', 'quarts',
'quatorze', 'quatorzième', 'quatorzièmes', 'quatre', 'quatrième', 'quatrièmes', 'que', 'quel',
'quelconque', 'quelconques', 'quelle', 'quelles', 'quelque', 'quelques', 'quels', 'qui',
'quiconque', 'quint', 'quinte', 'quintes', 'quints', 'quinze', 'quinzième', 'quinzièmes', 'quoi',
'rien', 's', 'sa', 'sans', 'sauf', 'se', 'seize', 'seizième', 'seizièmes', 'selon', 'sept',
'septante', 'septantième', 'septantièmes', 'septième', 'septièmes', 'ses', 'seulement', 'si',
'sien', 'sienne', 'siennes','siens', 'six', 'sixième', 'sixièmes', 'sixte', 'sixtes', 'soi',
'soixante', 'soixantième', 'soixantièmes', 'son', 'sous', 'suivant', 'sur', 't', 'ta', 'tantôt',
'tard', 'te', 'tel', 'telle', 'telles', 'tels', 'tes', 'tien', 'tienne', 'tiennes', 'tiens',
'tierce', 'tiers', 'toi', 'ton', 'tôt', 'touchant', 'tous', 'tout', 'toute', 'toutes', 'treize',
'treizième', 'treizièmes', 'trente', 'trentième', 'trentièmes', 'trois', 'troisième',
'troisièmes', 'tu', 'un', 'une', 'unième', 'unièmes', 'uns', 'vers', 'via', 'vingt', 'vingtième',
'vingtièmes', 'voici', 'voilà', 'voire', 'vos', 'votre', 'vôtre', 'vous', 'vrai', 'vu', 'y',
'zéroième', 'zéroièmes', 'zérotième', 'zérotièmes']


#################################################################################################
##                                                                                             ##
## Variables globales utilisées comme variables                                                  ##
##                                                                                             ##
#################################################################################################

# This dictionary will contain all selected words as keys and their frequencies as values
frequencies = {}

# This string will be used to fill final xml file
# At the beginning it contains only the header (including DTD)
output = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n\n\
<!DOCTYPE text [\n\
\t<!ELEMENT text (sentence*)>\n\
\t<!ELEMENT sentence (word*)>\n\
\t<!ELEMENT word (#PCDATA)>\n\
\t<!ATTLIST word frequency CDATA #REQUIRED>\n\
]>\n\n\
<text>\n'

# In this string we'll have content of txt file given as argument
txt = ''


#################################################################################################
#################################################################################################
##                                                                                             ##
## Pre compiled regex                                                                          ##
##                                                                                             ##
#################################################################################################
#################################################################################################

# Sometimes some words are splitted, this regex re-merge them.
blanks_between_points = re.compile('(?<=[\!\?\.]) (?=[\!\?\.])')

# This regex will find groups of ending punctuation (!, ? or .)
# It will be used to splt text in sentences
ending_punctuation = re.compile('[\!\?\.]+')

# This regex checks that end of argument given to this program contains at least one alphanumeric
# character followed by ".txt" characters. It is use twice:
# - Argument conformity verification
# - Resulting file creation ("txt" characters of argument are replaced by "xml")
filename_end = re.compile('(?<=\w\.)txt$')

# This regex is used to replace -, ", ', ;, : & , characters (eventually grouped) by a single 
# space
intermediate_punctuation = re.compile('[\,\;\:\"\'\-]+')

# Goal of this regex is to replace groups of whites characters (\n, \r, \t, \s) by single spaces
whites = re.compile('[\n\r\t ]+')

# Sometimes some words are splitted, this regex re-merge them
word_breaks = re.compile('\-[\n\r]+')


#################################################################################################
#################################################################################################
##                                                                                             ##
## Functions definitions                                                                       ##
##                                                                                             ##
#################################################################################################
#################################################################################################


#################################################################################################
##                                                                                             ##
## This function cleans string given as argument                                               ##
##                                                                                             ##
#################################################################################################

def clean_txt(txt):
    
    # Sometimes some words are splitted, this regex re-merge them
    txt = word_breaks.sub('', txt)
    
    # All of :;,'"- characters will be replaced by a space
    txt = intermediate_punctuation.sub(' ', txt)
    
    # All whites characters groups (\n, \r, \t & \s) will be replaced by a single space
    txt = whites.sub(' ', txt)
    
    # All whites characters between ending points (!, ? or .) will be removed
    txt = blanks_between_points.sub('', txt)
    
    return txt


#################################################################################################
##                                                                                             ##
## This function constructs a list of filtered sentences.                                      ##
## Each filtered sentence is itself a list of strings.                                         ##
## Each string is a non grammatical word containing only french characters.                    ##
## In the same time a dict is built, containing selected words as keys and their frequencies   ##
## as values.                                                                                  ##
##                                                                                             ##
#################################################################################################

def filter_txt(txt):
    
    # Returned list
    filtered_txt = []
    
    # String is cleaned, then splitted in sentences by regex. Ending punctuations are removed.
    for sentence in filter(None, ending_punctuation.split(clean_txt(txt))):
        word_list = []
        
        # Sentence string is splitted into words, each word is lowered, 
        for word in filter(None, sentence.split()):
            lower_word = word.lower()
            
            # Word is checked in order to ensure that it contains only french characters and to
            # verify that it isn't a grammatical word
            if is_french_word(lower_word) and (lower_word not in grammatical_words):
                
                # Selected word is saved, and its frequency is increased
                word_list.append(lower_word)
                if lower_word in frequencies:
                    frequencies[lower_word] += 1
                else:
                    frequencies[lower_word] = 1

        # Filtered sentence is saved
        if word_list != []:
            filtered_txt.append(word_list)

    return filtered_txt


#################################################################################################
##                                                                                             ##
## This function checks that all characters in given argument are french ones                  ##
##                                                                                             ##
#################################################################################################

def is_french_word(word):
    for char in word:
        if char not in french_chars:
            return False
    return True


#################################################################################################
##                                                                                             ##
## This function prepare a string in xml format containing all selected words and their        ##
## frequencies (grouped by sentences)                                                          ##
##                                                                                             ##
#################################################################################################

def prepare_output(splitted_txt, output):
    for sentence in splitted_txt:
        output += '\t<sentence>\n'
        for word in sentence:
            output += '\t\t<word frequency="' + str(frequencies[word]) + '">' + word + '</word>\n'
        output += '\t</sentence>\n'
    return output + '</text>'


#################################################################################################
#################################################################################################
##                                                                                             ##
## Main program                                                                                ##
##                                                                                             ##
#################################################################################################
#################################################################################################

# Argument presence and its conformity are checked
if len(sys.argv) < 2 or filename_end.findall(sys.argv[1]) == []:
    exit("Usage: txt_to_xml *.txt")

# File given as argument is opened, read and then closed
with open(sys.argv[1], 'r', 0) as txt_file:
    txt = txt_file.read()

# Text is cleaned, then splitted in sentences
# Each sentence is splitted in french non grammatical words
# A xml output is prepared (formatted as a single string) containing all filtered words and
# their frequencies (grouped by sentences)
output = prepare_output(filter_txt(txt), output)

# Result file is opened, written and then closed
with open(filename_end.sub('xml', sys.argv[1]), 'w', 0) as xml_file:
    xml_file.write(output)

# End of the program
exit(0)
