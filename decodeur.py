###############################################################################
#																			  #
# Décryptage de textes alphabétiques uniquement.							  #
# Combinaison des conversions ascii -> hexadécimal -> binaire -> morse -> txt #
#																			  #
###############################################################################

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
				# hexa_word += "0"
				continue
			else:
				hexa = hex(ord(char)-150).replace("0x", "")

				while len(hexa) < 3:
					hexa = "0"+hexa
				hexa_word += hexa

		hexa_words.append(hexa_word)

	return hexa_words

def hexaToBin(hexa_words):
	bin_words = []

	for word in hexa_words:
		bin_word = ""
		nBin, rank = 0, 0

		while nBin < len(word)-1:
			tmp_hexa = ""

			for i in range(3):
				nBin = rank+i
				tmp_hexa += word[nBin]

			rank += 3
			tmp_bin = bin(int(tmp_hexa, base=16)).replace("0b", "")

			while len(tmp_bin) < 12: # Correction du manque possible de digits
				tmp_bin = "0"+tmp_bin

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

			while i < 6:
				nBin = i+rank
				binary = word[nBin]+word[nBin+1]

				if binary == "00":
					morse_word += "0"
				elif binary == "10":
					morse_word += "1"
				else: #11
					morse_word += "2"

				i += 2

			rank += 6

		morse_words.append(morse_word)

	return morse_words

def morseToAscii(morse_words):
	words = []

	for word in morse_words:
		tmp_word = ""
		nMorse = 0

		while nMorse+5 < len(word)-1:
			tmp = ""

			try:
				morse = word[nMorse]+word[nMorse+1]+word[nMorse+2]+word[nMorse+3]+word[nMorse+4]+word[nMorse+5]
				nMorse += 6
				tmp += morse
			except IndexError:
				pass

			for alpha in morse_dict:
				if morse_dict[alpha] == tmp:
					tmp_word += alpha

		words.append(tmp_word)

	return words

def decodeMorse(morse_words):
	new_morse_words = []

	for word in morse_words:
		new_word = word

		# Récupération des bits de cryptages
		# 1 échange entre valeurs 0 {x,y,z}/ 1 {z,x,y} / 2 {y,z,x}
		# 2 Décalage d'indice
		# 3 Détermine la cible de l'échange x du 1er bit
		# 4 Idem pour y
		# 5 Idem pour z

		bit1, bit2, bit3, bit4, bit5 = new_word[0], new_word[1], new_word[2], new_word[3], new_word[4]
		new_word = new_word[6:] # Padding 6 bits

		# Récupération du décalage
		if bit2 == "0":
			pass
		elif bit2 == "1":
			firstChar = new_word[0]
			new_word = new_word+firstChar
			new_word = new_word[1:]
		else: # 2
			lastChar = new_word[len(new_word)-1]
			new_word = lastChar+new_word
			new_word = new_word[:-1]

		# Récupération de l'échange de valeurs
		if bit1 == "0":
			dsts_change = [0, 1, 2]
		elif bit1 == "1":
			dsts_change = [2, 0, 1]
		else: # 2
			dsts_change = [1, 2, 0]

		tmp = ""
		for char in new_word:
			if dsts_change.index(int(char)) == 0:
				tmp += str(dsts_change[int(bit3)])
			elif dsts_change.index(int(char)) == 1:
				tmp += str(dsts_change[int(bit4)])
			else: # 2
				tmp += str(dsts_change[int(bit5)])
		new_word = tmp

		new_morse_words.append(new_word)

	return new_morse_words

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

new_morse_words = decodeMorse(morse_words)


for word in new_morse_words:
	print(str(len(word))+" "+word)
print("\n")

# Conversion morse -> texte

words = morseToAscii(new_morse_words)

for word in words:
	print(str(len(word))+" "+word)
print("\n")

# Compilation de la sortie

print("################# SORTIE #################\n")
print(" ".join(words))