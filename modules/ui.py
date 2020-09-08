import tkinter as tk
from tkinter import filedialog
from tkinter.simpledialog import askstring
from . import search
from .data import *


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
		# self.widgets["name"] = [ tk.widget,row,col,type,framename,sticky,scrollcmd ]
		
		self.widgets["file_label"] = [tk.Label(self.master,text = "Seleccione un archivo"),0,0,LBL,False,False,False,False] 
		self.widgets["code_list"] = [tk.Listbox(self.master),1,0,LSTBX,"codeframe",tk.N+tk.S+tk.E+tk.W,False,False]
		self.widgets["codescroll"] = [tk.Scrollbar(self.master),1,1,SRLL,"codeframe",tk.NW+tk.S,"code_list"]
		self.widgets["load_button"] = [tk.Button(self.master,text = "Escoger archivo",command=self.load),0,2,BTN,False,False,False]
		self.widgets["code_button"] = [tk.Button(self.master,text="Agregar codigos a buscar",command=self.loadCodes),1,2,BTN,False,False,False]
		self.widgets["delcode_button"] = [tk.Button(self.master,text="Eliminar codigo",command=self.delete),2,2,BTN,False,False,False]
		self.widgets["close_button"] = [tk.Button(self.master,text="Cerrar",command=self.master.quit),2,0,BTN,False,False,False]
		self.widgets["search"] = [tk.Button(self.master,text="Buscar",command=self.search),2,3,BTN,False,False,False]

		self.update()
			
	def update(self):
		for name in self.widgets:
				
			widget = self.widgets[name][0]
			row = self.widgets[name][1]
			col = self.widgets[name][2]
			stk = self.widgets[name][5]
			cfg = self.widgets[name][6]
			if self.widgets[name][3] == LSTBX: # Is ListBox

				widget.grid(row = row, column = col,pady = 5,padx = 10,sticky=stk)
			
			elif self.widgets[name][3] == SRLL: # Is Scroll

				widget.grid(row = row, column = col,pady = 5,padx = 10,sticky=stk)
				widget['command'] = self.widgets[cfg][0].yview
			
			else:
				widget.grid(row = row, column = col,pady = 5,padx = 10)




	def loadCodes(self):

		if not self.codes:
			self.codes = []

		code = askstring('Codigo a buscar',"Inserte el codigo a buscar")
		if not code:
			return
		
		if code in self.codes:
			self.sendMessage(MSG_ERROR,"El codigo ya existe en la lista","Error")
		else:
			self.codes.append(code)
			self.UpdateCodes()
		return

	def delete(self):

		if not self.codes or len(self.codes) < 1 :
			self.sendMessage(MSG_ERROR,"No hay codigos insertados","Error")
			return
		code = askstring('Codigo a buscar',"Inserte el codigo a borrar")

		if code and code in self.codes:
			self.codes.pop(self.codes.index(code))
		self.UpdateCodes()



	def UpdateCodes(self):
		self.widgets["code_list"][0].delete(0,tk.END)
		if len(self.codes)<1:
			self.sendMessage(MSG_WRNG,"Sin datos cargados","Advertencia")
		else:
			for i in self.codes:
				self.widgets["code_list"][0].insert(tk.END,i)

	def load(self):
		self.file = filedialog.askopenfilename()
		if self.file:
			self.editLabel("file_label","Archivo Cargado")

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
			tk.messagebox.showerror(message=msg, title=title)
		if messagetype == MSG_INFO:
			tk.messagebox.showinfo(message=msg, title=title)
		if messagetype == MSG_WRNG:
			tk.messagebox.showwarning(message=msg,title=title)
		return

	def editLabel(self,label,txt):
		try:
			self.widgets[label][0].config(text = txt)
		except AttributeError as identifier:
			self.sendMessage(MSG_ERROR,identifier,"ERROR")


def start_program():
	root = tk.Tk()
	root.minsize(400,400)
	root.geometry()
	gui = program(root)
	root.mainloop()

