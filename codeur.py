###############################################################################
#																			  #
# Cryptage de textes alphabétiques uniquement.								  #
# Combinaison des conversions txt -> morse -> binaire -> hexadécimal -> ascii #
#																			  #
# 
#
############################################################################### 

from random import randrange
import re

################################### CST #####################################
# Table morse

morse_dict = {"a": "120000", "b": "211100", "c": "212100", "d": "211000", "e": "100000",
			  "f": "112100", "g": "221000", "h": "111100", "i": "110000", "j": "122200",
			  "k": "212000", "l": "121100", "m": "220000", "n": "210000", "o": "222000",
			  "p": "122100", "q": "221200", "r": "121000", "s": "111000", "t": "200000",
			  "u": "112000", "v": "111200", "w": "122000", "x": "211200", "y": "212200",
			  "z": "221100", "à": "122120", "ä": "121200", "é": "112110", "ñ": "221220",
			  "ö": "222100", "ü": "112200", "1": "122220", "2": "112220", "3": "111220",
			  "4": "111120", "5": "111110", "6": "211110", "7": "221110", "8": "222110",
			  "9": "222210", "0": "222220", ",": "221122", ".": "121212", "?": "112211",
			  '"': "121121", ":": "222111", "'": "122221", "-": "211112", "/": "211210",
			  "(": "212210", ")": "212212", " ": "000000"}

################################### FONCTION ################################
# Recupération entrée
def splitAndConvert(text):
	words = []
	word = ""

	for letter in text:
		word += letter.lower()
		if letter == " ":
			# Reset
			words.append(word)
			word = ""

	return words

# Conversion alpha->morse (6bits : a-z + 0-9 + àù... + (,?;.)... )
def strToMorse(words):
	morse_words = []

	for word in words:
		morse_word = ""

		for letter in word:
			# Conversion decimal vers string
			morse_letter = str(morse_dict[letter])
			morse_word += morse_letter

		morse_words.append(morse_word)

	return morse_words

# Conversion morse->bin
def morseToBin(morse_words):
	bin_words = []

	for word in morse_words:
		bin_word = ""
		rank, nMorse = 0, 0

		while nMorse < len(word)-1:

			for i in range(6):
				nMorse = i+rank
				morse = word[nMorse]
				
				if morse == "0":
					bin_word += "00"
				elif morse == "1":
					bin_word += "10"
				else: #2
					bin_word += "11"

			rank += 6
		bin_words.append(bin_word)

	return bin_words

# Conversion bin->hexa
def binToHexa(bin_words):
	hex_words = []

	for word in bin_words:
		hex_word = ""
		nHex, rank = 0, 0

		while nHex < len(word)-1:
			tmp_hex = ""

			for i in range(12):
				try:
					nHex = rank+i
					tmp_hex += word[nHex]
				except IndexError:
					pass

			rank += 12
			hex_number = hex(int(tmp_hex, 2)).replace("0x", "")

			while len(hex_number) < 3:
				hex_number += "0"

			hex_word += hex_number	

		hex_words.append(hex_word)

	return hex_words

# Conversion hex->ascii
def hexToAscii(hex_words):
	ascii_words = []

	for word in hex_words:
		ascii_word = ""
		nHex, rank = 0, 0

		while nHex < len(word)-1:
			tmp = ""

			for i in range(3):
				nHex = i+rank
				tmp += word[nHex]

			rank += 3
			char = chr(int(tmp, base=16)+150) # Ajout de la constante 150 pour éviter les contrôles qui ne sont pas détectables
			ascii_word += char

		ascii_words.append(ascii_word)

	return ascii_words

def cryptIt(raw):
	new_morse_words = []

	for word in raw:

		# Randomisation bits 1/2/3/4/5
		# 1 échange entre valeurs 0 {x,y,z}/ 1 {z,x,y} / 2 {y,z,x}
		# 2 Décalage d'indice
		# 3 Détermine la cible de l'échange x du 1er bit
		# 4 Idem pour y
		# 5 Idem pour z

		bit1 = randrange(0,3) # 0, 1, 2
		bit2 = randrange(0,3)
		bit3 = randrange(0,3)
		bit4 = randrange(0,3)
		bit5 = randrange(0,3)
		bit6 = 0 # Padding (%6)

		while bit3 == bit1: # Evite la redondance dans l'échange de valeurs
			bit3 = randrange(0,3)
		while bit4 == bit3:
			bit4 = randrange(0,3)
		while bit5 == bit4 or bit5 == bit3:
			bit5 = randrange(0,3)

		if bit1 == 0:
			dsts_change = [bit3, bit4, bit5]
		elif bit1 == 1:
			dsts_change = [bit5, bit3, bit4]
		else: # 2
			dsts_change = [bit4, bit5, bit3]

		new_word = ""
		for char in word:
			new_word += str(dsts_change[int(char)])

		if bit2 == 0:
			pass
		elif bit2 == 1:
			lastChar = new_word[len(new_word)-1]
			new_word = lastChar+new_word
			new_word = new_word[:-1]
		else: # 2
			firstChar = new_word[0]
			new_word = new_word+firstChar
			new_word = new_word[1:]

		new_word = str(bit1)+str(bit2)+str(bit3)+str(bit4)+str(bit5)+str(bit6)+new_word
		new_morse_words.append(new_word)

	return new_morse_words, [bit1, bit2, bit3, bit4, bit5, bit6]#, bit7, bit8]


################################### MAIN ####################################
# Récupération de l'entrée et découpage en séquence de mot

text = input("Texte à encoder\n/!\\ Peu de caractères spéciaux sont pris en charge /!\\\n: ") + " "
words = splitAndConvert(text)

for word in words:
	print(str(len(word))+" "+word)
print("\n")

# Conversion en morse

morse_words = strToMorse(words)

for word in morse_words:
	print(str(len(word))+" "+word)
print("\n")

morse_words, encryptionBits = cryptIt(morse_words)

for word in morse_words:
	print(str(len(word))+" "+word)
print("\n")

# Conversion en binaire sur 1 octet (4*2bits 5*2 si n° avec)
#	00 = pas de signal
#	10 = signal court
#	11 = signal long

bin_words = morseToBin(morse_words)

for word in bin_words:
	print(str(len(word))+" "+word)
print("\n")

# Conversion en hexadecimal par octet (de morse binaire)

hex_words = binToHexa(bin_words)
for word in hex_words:
	print(str(len(word))+" "+word)
print("\n")


# Traduction dans la table ascii
#	(à étendre utf-8 ?)

ascii_words = hexToAscii(hex_words)

for word in ascii_words:
	print(str(len(word))+" "+word)
print("\n")

# Compilation de la sortie
print("################# SORTIE #################\n")
print(" ".join(ascii_words))