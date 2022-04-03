###############################################################################
#																			  #
# Décryptage de textes alphabétiques uniquement.							  #
# Combinaison des conversions ascii -> hexadécimal -> binaire -> morse -> txt #
#																			  #
###############################################################################

################################### CLASS ################################

class DecryptThis():

	def __init__(self, text, verbose=False):
		# Table morse
		self.morse_dict = {"a": "120000", "b": "211100", "c": "212100", "d": "211000", "e": "100000",
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
		self.text = text
		self.verbose= verbose


	def run(self):
		self.getCrypted()

		# Conversion ascii -> hexadécimal

		self.cryptedToHexa()

		# Conversion hexadécimal -> binaire

		self.hexaToBin()

		# Conversion binaire -> morse

		self.binToMorse()

		# Decryptage

		self.decodeMorse()

		# Conversion morse -> texte

		self.morseToAscii()

		if self.verbose:
			self.beVerbose()


	def beVerbose(self):

		for wordlist in [self.hexa_words, self.bin_words,
						 self.morse_words, self.decrypted_morse_words, self.words]:
			for word in wordlist:
				print(str(len(word))+" "+word)
			print("\n")
		print("Sortie : %s"%(" ".join(self.words)))


	def getCrypted(self):
		self.words = []
		word = ""

		if self.text[-1] != " ":
			self.text += " "

		for char in self.text:
			word += char
			if char == " ":
				self.words.append(word)
				word = ""


	def cryptedToHexa(self):
		self.hexa_words = []

		for word in self.words:
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

			self.hexa_words.append(hexa_word)


	def hexaToBin(self):
		self.bin_words = []

		for word in self.hexa_words:
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

			self.bin_words.append(bin_word)


	def binToMorse(self):
		self.morse_words = []

		for word in self.bin_words:
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

			self.morse_words.append(morse_word)


	def morseToAscii(self):
		self.words = []

		for word in self.morse_words:
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

				for alpha in self.morse_dict:
					if self.morse_dict[alpha] == tmp:
						tmp_word += alpha

			self.words.append(tmp_word)


	def decodeMorse(self):
		self.decrypted_morse_words = []

		for word in self.morse_words:
			new_word = word

			# Récupération des bits de cryptages
			# 1 échange entre valeurs 0 {x,y,z}/ 1 {z,x,y} / 2 {y,z,x}
			# 2 Décalage d'indice
			# 3 Détermine la cible de l'échange x du 1er bit
			# 4 Idem pour y
			# 5 Idem pour z

			bit1, bit2, bit3, bit4, bit5 = new_word[0], new_word[1], new_word[2], new_word[3], new_word[4]
			# print("Bits: "+str([bit1, bit2, bit3, bit4, bit5, 0]))

			new_word = new_word[6:] # Padding 6 bits
			# print("Start : "+new_word)

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

			# print("Decalage : "+new_word)

			# Récupération de l'échange de valeurs
			if bit1 == "0":
				dsts_change = [bit3, bit4, bit5] # bit3 -> 0, bit4 -> 1, bit5 -> 2
			elif bit1 == "1":
				dsts_change = [bit5, bit3, bit4] # bit3 -> 1, bit4 -> 2, bit5 -> 0
			else: # 2
				dsts_change = [bit4, bit5, bit3] # bit3 -> 2, bit4 -> 0, bit5 -> 1

			# print("Dsts : "+str(dsts_change))

			tmp = ""
			for char in new_word:
				if char == bit3:
					tmp += str(dsts_change.index(bit3))
				elif char == bit4:
					tmp += str(dsts_change.index(bit4))
				else: # bit5
					tmp += str(dsts_change.index(bit5))
			new_word = tmp

			# print("Change : "+new_word+"\n\n")

			self.decrypted_morse_words.append(new_word)
