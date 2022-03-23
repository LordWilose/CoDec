###############################################################################
#																			  #
# Décryptage de textes alphabétiques uniquement.							  #
# Combinaison des conversions ascii -> hexadécimal -> binaire -> morse -> txt #
#																			  #
###############################################################################

################################### CST #####################################
# Table morse

morse_dict = {"a": "1200", "b": "2111", "c": "2121", "d": "2110", "e": "1000", "f": "1121",
			  "g": "2210", "h": "1111", "i": "1100", "j": "1222", "k": "2120", "l": "1211",
			  "m": "2200", "n": "2100", "o": "2220", "p": "1221", "q": "2212", "r": "1210",
			  "s": "1110", "t": "2000", "u": "1120", "v": "1112", "w": "1220", "x": "2112",
			  "y": "2122", "z": "2211", " ": "0000"}

################################### FONCTION ################################

def getCrypted(crypted):
	words = []
	word = ""

	for char in crypted:
		word += char
		if char == " ":
			words.append(word)
			word = ""

	return words

def cryptedToHexa(crypted):
	hexa_words = []

	for word in words:
		hexa_word = ""

		for char in word:
			if char == " ": # Si espace, mise manuelle de la valeur (bug sinon)
				hexa_word += "0"
			else:
				hexa = hex(ord(char)-150)
				hexa_word += str(hexa).replace("0x", "")

		hexa_words.append(hexa_word)

	return hexa_words

def hexaToBin(hexa_words):
	bin_words = []

	for word in hexa_words:
		bin_word = ""
		nBin, rank = 0, 0

		while nBin < len(word)-1:
			tmp_hexa = ""

			for i in range(2):
				nBin = rank+i
				tmp_hexa += word[nBin]

			rank += 2
			tmp_bin = bin(int(tmp_hexa, base=16)).replace("0b", "")

			while len(tmp_bin) < 8: # Correction du manque possible de digits
				tmp_bin += "0"

			bin_word += tmp_bin

		bin_words.append(bin_word)

	return bin_words

def binToMorse(bin_words):
	morse_words = []

	for word in bin_words:
		morse_word = ""
		rank, nBin = 0, 0

		while nBin+1 < len(word)-1:
			i = 0

			while i < 4:
				nBin = i+rank
				binary = word[nBin]+word[nBin+1]

				if binary == "00":
					morse_word += "0"
				elif binary == "10":
					morse_word += "1"
				else: #11
					morse_word += "2"

				i += 2

			rank += 4

		morse_words.append(morse_word)

	return morse_words

################################### MAIN ####################################
# Récupération du texte crypté

text = input("Texte à décoder\n: ")

words = getCrypted(text)

for word in words:
	print(str(len(word))+" "+word)	
print("\n")

# Conversion ascii -> hexadécimal

hexa_words = cryptedToHexa(words)

for word in hexa_words:
	print(str(len(word))+" "+word)	
print("\n")

# Conversion hexadécimal -> binaire

bin_words = hexaToBin(hexa_words)

for word in bin_words:
	print(str(len(word))+" "+word)
print("\n")

# Conversion binaire -> morse

morse_words = binToMorse(bin_words)

for word in morse_words:
	print(str(len(word))+" "+word)
print("\n")

# Conversion morse -> texte

words = []

for word in morse_words:
	tmp_word = ""
	nMorse = 0

	while nMorse+3 < len(word)-1:
		tmp = ""

		try:
			morse = word[nMorse]+word[nMorse+1]+word[nMorse+2]+word[nMorse+3]
			nMorse += 4
			tmp += morse
		except IndexError:
			pass

		for alpha in morse_dict:
			if morse_dict[alpha] == tmp:
				tmp_word += alpha

	words.append(tmp_word)

for word in words:
	print(str(len(word))+" "+word)
print("\n")

# Compilation de la sortie

print("################# SORTIE #################\n")
print(" ".join(words))