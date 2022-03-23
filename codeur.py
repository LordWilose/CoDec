###############################################################################
#																			  #
# Cryptage de textes alphabétiques uniquement.								  #
# Combinaison des conversions txt -> morse -> binaire -> hexadécimal -> ascii #
#																			
############################################################################### 

################################### CST #####################################
# Table morse

morse_dict = {"a": "1200", "b": "2111", "c": "2121", "d": "2110", "e": "1000", "f": "1121",
			  "g": "2210", "h": "1111", "i": "1100", "j": "1222", "k": "2120", "l": "1211",
			  "m": "2200", "n": "2100", "o": "2220", "p": "1221", "q": "2212", "r": "1210",
			  "s": "1110", "t": "2000", "u": "1120", "v": "1112", "w": "1220", "x": "2112",
			  "y": "2122", "z": "2211", " ": "0000"}

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

# Conversion alpha->morse
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

			for i in range(4):
				nMorse = i+rank
				morse = word[nMorse]
				if morse == "0":
					bin_word += "00"
				elif morse == "1":
					bin_word += "10"
				else: #2
					bin_word += "11"

			rank += 4
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

			for i in range(8):
				try:
					nHex = rank+i
					tmp_hex += word[nHex]
				except IndexError:
					pass

			rank += 8
			hex_number = hex(int(tmp_hex, 2)).replace("0x", "")

			while len(hex_number) < 2:
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

			for i in range(2):
				nHex = i+rank
				tmp += word[nHex]

			rank += 2
			char = chr(int(tmp, base=16)+150) # Ajout de la constante 150 pour éviter les contrôles qui ne sont pas détectables
			ascii_word += char

		ascii_words.append(ascii_word)

	return ascii_words

################################### MAIN ####################################
# Récupération de l'entrée et découpage en séquence de mot

text = input("Texte à encoder\n/!\\ PAS d'UTF-8 : Pas d'accents, de ponctuaction ou de caractères spéciaux /!\\\n: ") + " "
words = splitAndConvert(text)

for word in words:
	print(str(len(word))+" "+word)
print("\n")

# Conversion en morse

morse_words = strToMorse(words)

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