from tkinter import Tk,Label,Button,filedialog,messagebox
from tkinter.simpledialog import askstring
import PyPDF2
import re

class program:
	file = None
	codes = None
	def __init__(self,master):

		self.master = master
		master.title("programa")

		self.label = Label(master,text = "Seleccione un archivo")
		self.code_label = Label(master,text = "Sin datos cargados")
		self.load_button = Button(master,text = "Escoger archivo",command=self.load)
		self.code_button = Button(master,text="Agregar codigos a buscar",command=self.loadCodes)
		self.delcode_button = Button(master,text="Eliminar codigo",command=self.delete)
		self.close_button = Button(master,text="Cerrar",command=master.quit)
		self.search = Button(master,text="Buscar",command=self.search)


		self.label.pack(pady=3)
		self.code_label.pack(pady=10)
		self.load_button.pack(pady=5)
		self.code_button.pack(pady=5)
		self.delcode_button.pack(pady=5)
		self.search.pack(pady=5)
		self.close_button.pack(pady=5)


	def loadCodes(self):
		
		if not self.codes:
			self.codes = []

		code = askstring('Codigo a buscar',"Inserte el codigo a buscar")
		if code and not code in self.codes:
			self.codes.append(code)
			self.UpdateCodes()

	def delete(self):

		if not self.codes or len(self.codes) < 1 :
			messagebox.showerror(message="No hay codigos insertados", title="Error")
			return


		code = askstring('Codigo a buscar',"Inserte el codigo a borrar")

		if code and code in self.codes:
			self.codes.pop(self.codes.index(code))
		print(self.codes)
		self.UpdateCodes()



	def UpdateCodes(self):

		if len(self.codes)<1:
			string = "Sin datos cargados"
			print("in")
		else:

			string = "Datos cargados:\n"
			for i in self.codes:
				string+= i + "\n"
		self.code_label.config(text = string)



	def load(self):
		self.file = filedialog.askopenfilename()
		if self.file:
			self.label.config(text = "Archivo cargado")

	def search(self):
		if not self.codes or not self.file or len(self.codes)<1:
			messagebox.showerror(message="No hay codigos insertados o un archivo", title="Error")
			return


		results = {}
		for i in self.codes:
			results[i] = []

		object = PyPDF2.PdfFileReader(self.file)
		NumPages = object.getNumPages()


		for i in range(0, NumPages):
		    PageObj = object.getPage(i)
		    Text = PageObj.extractText() 
		    for String in self.codes:
		    	ResSearch = re.search(String, Text)
		    	if ResSearch:
		    		results[String].append(str(i))
		
		self.showResults(results)

	def showResults(self,results):
		msg = "Codigo: Paginas\n"
		for i in self.codes:
			stri = str(i) + ': '
			if len(results[i]) < 1:
				stri+= "No se encontro en el archivo"
			else:
				for j in results[i]:
					stri += str(int(j)+1) + ','
			msg+=stri + '\n'
		messagebox.showinfo(message=msg, title="Datos encontrados")







root = Tk()
root.minsize(400,400)
root.geometry()
gui = program(root)
root.mainloop()