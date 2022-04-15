###############################################################################
#																			  #
# Décryptage de textes alphabétiques uniquement.							  #
# Combinaison des conversions ascii -> hexadécimal -> binaire -> morse -> txt #
#																			  #
###############################################################################

################################### FONCTION ################################

from decodeur_Funct import *

################################### MAIN ####################################
# Récupération du texte crypté

text = input("Texte à décoder\n: ")
beVerbose = input("Bavard ? (y/N) : ")
if beVerbose in ("y", "Y", "yes", "Yes", "YES", "ye", "Ye", "YE"):
	beVerbose = True
else:
	beVerbose = False

words = getCrypted(text)

if beVerbose:
	for word in words:
		print(str(len(word))+" "+word)	
	print("\n")

# Conversion ascii -> hexadécimal

hexa_words = cryptedToHexa(words)

if beVerbose:
	for word in hexa_words:
		print(str(len(word))+" "+word)	
	print("\n")

# Conversion hexadécimal -> binaire

bin_words = hexaToBin(hexa_words)

if beVerbose:
	for word in bin_words:
		print(str(len(word))+" "+word)
	print("\n")

# Conversion binaire -> morse

morse_words = binToMorse(bin_words)

if beVerbose:
	for word in morse_words:
		print(str(len(word))+" "+word)
	print("\n")

new_morse_words = decodeMorse(morse_words, beVerbose)

if beVerbose:
	for word in new_morse_words:
		print(str(len(word))+" "+word)
	print("\n")

# Conversion morse -> texte

words = morseToAscii(new_morse_words)

if beVerbose:
	for word in words:
		print(str(len(word))+" "+word)
	print("\n")

# Compilation de la sortie

print("\n\n################# SORTIE #################\n")
print(" ".join(words))