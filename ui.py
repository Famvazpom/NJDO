from tkinter import Tk,Label,Button,filedialog,messagebox
from tkinter.simpledialog import askstring
from modules import search
import PyPDF2
import re


MSG_ERROR = "Error"
MSG_INFO = "Informacion"

class program:
	file = None
	codes = None
	engine = None
	widgets = {}

	def __init__(self,master):

		self.master = master
		master.title("programa")
		self.engine = search.object()
		self.ui()

	def ui(self):
		self.widgets["file_label"] = [Label(self.master,text = "Seleccione un archivo"),0,0]
		self.widgets["code_label"] = [Label(self.master,text = "Sin datos cargados"),1,0]
		self.widgets["load_button"] = [Button(self.master,text = "Escoger archivo",command=self.load),0,1]
		self.widgets["code_button"] = [Button(self.master,text="Agregar codigos a buscar",command=self.loadCodes),1,1]
		self.widgets["delcode_button"] = [Button(self.master,text="Eliminar codigo",command=self.delete),1,2]
		self.widgets["close_button"] = [Button(self.master,text="Cerrar",command=self.master.quit),2,0]
		self.widgets["search"] = [Button(self.master,text="Buscar",command=self.search),2,1]

		print(self.widgets)

		for name in self.widgets:
			widget = self.widgets[name][0]
			row = self.widgets[name][1]
			col = self.widgets[name][2]
			widget.grid(row = row, column = col,pady = 5,padx = 10)
			

	def loadCodes(self):
		
		if not self.codes:
			self.codes = []

		code = askstring('Codigo a buscar',"Inserte el codigo a buscar")
		if code and not code in self.codes:
			self.codes.append(code)
			self.UpdateCodes()

	def delete(self):

		if not self.codes or len(self.codes) < 1 :
			self.sendMessage(MSG_ERROR,"No hay codigos insertados","Error")
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
			self.sendMessage(MSG_ERROR,"No hay codigos insertados o un archivo","Error")
			return
		self.showResults(self.engine.search(self.file,self.codes))
		return

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
		self.sendMessage(MSG_INFO,msg,"Datos Encontrados")

	def sendMessage(self,messagetype,msg,title):

		if messagetype == MSG_ERROR:
			messagebox.showerror(message=msg, title=title)
		if messagetype == MSG_INFO:
			messagebox.showinfo(message=msg, title=title)
		return


def main():
	root = Tk()
	root.minsize(400,400)
	root.geometry()
	gui = program(root)
	root.mainloop()




if __name__ == "__main__":
	main()

