##########################################################################################
#																			 			 #
# Cryptage de textes alphabétiques uniquement.								  			 #
# Combinaison des conversions txt -> morse (cryptage) -> binaire -> hexadécimal -> ascii #
#																			 			 #
# Chiffrement aléatoire sur 6bits											 			 #
#																			 			 #
##########################################################################################

################################### FONCTION ################################
from codeur_Funct import *

################################### MAIN ####################################
# Récupération de l'entrée et découpage en séquence de mot

text = input("Texte à encoder\n/!\\ Peu de caractères spéciaux sont pris en charge /!\\\n: ") + " "

beVerbose = input("Bavard ? (y/N) : ")
if beVerbose in ("y", "Y", "yes", "Yes", "YES", "ye", "Ye", "YE"):
	beVerbose = True
else:
	beVerbose = False

words = splitAndConvert(text)

if beVerbose:
	for word in words:
		print(str(len(word))+" "+word)
	print("\n")

# Conversion en morse

morse_words = strToMorse(words)

if beVerbose:
	for word in morse_words:
		print(str(len(word))+" "+word)
	print("\n")

morse_words, encryptionBits = cryptIt(morse_words, beVerbose)

if beVerbose:
	for word in morse_words:
		print(str(len(word))+" "+word)
	print("\n")

# Conversion en binaire sur 1 octet (4*2bits 5*2 si n° avec)
#	00 = pas de signal
#	10 = signal court
#	11 = signal long

bin_words = morseToBin(morse_words)

if beVerbose:
	for word in bin_words:
		print(str(len(word))+" "+word)
	print("\n")

# Conversion en hexadecimal par octet (de morse binaire)

hex_words = binToHexa(bin_words)

if beVerbose:
	for word in hex_words:
		print(str(len(word))+" "+word)
	print("\n")


# Traduction dans la table ascii
#	(à étendre utf-8 ?)

ascii_words = hexToAscii(hex_words)

if beVerbose:
	for word in ascii_words:
		print(str(len(word))+" "+word)
	print("\n")

# Compilation de la sortie
print("################# SORTIE #################\n")
print(" ".join(ascii_words))