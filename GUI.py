from codeur import EncryptThis
from decodeur import DecryptThis
import tkinter as tk


class GUI():

	def __init__(self):
		self.root = tk.Tk()
		self.root.title("CODEC")

		self.type = tk.IntVar()
		self.b1 = tk.Radiobutton(self.root, text="Encrypt", variable=self.type, value=0).grid(row=1, column=1)
		self.b2 = tk.Radiobutton(self.root, text="Decrypt", variable=self.type, value=1).grid(row=1, column=2)

		self.verbose = tk.IntVar()
		self.b3 = tk.Checkbutton(self.root, text='Bavard',variable=self.verbose, onvalue=1, offvalue=0).grid(row=2, column=1)

		self.b4 = tk.Button(self.root, text="GO", command=lambda:self.run()).grid(row=2, column=2)

		self.root.mainloop()


	def run(self):
		self.type = self.type.get()

		self.root.destroy()
		self.root = tk.Tk()
		self.root.title("CODEC")

		if self.type == 1:
			pass
		elif self.type == 0:
			self.Encrypt()

		self.root.mainloop()


	def Encrypt(self):	
		self.l1 = tk.Label(self.root, text="Texte à encrypter :").grid(row=1, column=1)
		self.text = tk.StringVar()
		self.e1 = tk.Entry(self.root, textvariable=self.text).grid(row=1, column=2)
		self.b1 = tk.Button(self.root, text="GO", command=lambda:self.goEncryptThis()).grid(row=1, column=3)


	def goEncryptThis(self):
		self.root.destroy()

		objet = EncryptThis(self.text.get(), self.verbose, True)
		objet.run()


test = GUI()