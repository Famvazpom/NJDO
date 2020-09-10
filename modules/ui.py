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
	frames = {}

	def __init__(self,master):

		self.master = master
		master.title("programa")
		self.engine = search.object()
		self.ui()

	def ui(self):

		# self.frames["name"] = [ tk.Frame, side, fill, expand ]
		self.frames["top_frame"] = [ tk.Frame(self.master), "top","x",True]
		self.frames["middle_frame"] = [ tk.Frame(self.master),"top","both",True ]
		self.frames["left_frame"] = [ tk.Frame(self.frames["middle_frame"][0]), 0,0]
		self.frames["right_frame"] = [ tk.Frame(self.frames["middle_frame"][0]), 0,1]

		
		# self.widgets["name"] = [ tk.widget,row,col,type,framename,sticky,scrollcmd ]
		self.widgets["file_label"] = [tk.Label(self.frames["top_frame"][0],text = "Seleccione un archivo"),0,0,LBL,False,False,False,False] 
		self.widgets["load_button"] = [tk.Button(self.frames["top_frame"][0],text = "Escoger archivo",command=self.load),0,1,BTN,False,False,False]
		
		self.widgets["code_list"] = [tk.Listbox(self.frames["left_frame"][0]),1,0,LSTBX,"codeframe",tk.N+tk.S+tk.E+tk.W,False,False]
		self.widgets["codescroll"] = [tk.Scrollbar(self.frames["left_frame"][0]),1,1,SRLL,"codeframe",tk.NW+tk.S,"code_list"]
		
		self.widgets["code_button"] = [tk.Button(self.frames["right_frame"][0],text="Agregar codigo",command=self.loadCodes),0,0,BTN,False,False,False]
		self.widgets["delcode_button"] = [tk.Button(self.frames["right_frame"][0],text="Eliminar codigo",command=self.delete),1,0,BTN,False,False,False]
		self.widgets["clean_button"] = [tk.Button(self.frames["right_frame"][0],text="Limpiar codigos",command=self.cleanCodes),2,0,BTN,False,False,False ]
		self.widgets["search_button"] = [tk.Button(self.frames["right_frame"][0],text="Buscar",command=self.search),3,0,BTN,False,False,False]

		self.update()
	
	def update_frames(self,frame,isContained=False):

		frameObj = self.frames[frame][0]
		if isContained:
			frameObj.grid(row=self.frames[frame][1],column=self.frames[frame][2])
		else:
			frameObj.pack(side=self.frames[frame][1],fill=self.frames[frame][2],expand=self.frames[frame][3],pady=5)

	def update(self):
		
		self.update_frames("top_frame")
		self.update_frames("middle_frame")
		self.update_frames("left_frame",True)
		self.update_frames("right_frame",True)

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

	def cleanCodes(self):
		if self.codes:
			self.codes.clear()
			self.UpdateCodes()
			self.sendMessage(MSG_INFO,"Lista limpiada exitosamente","Informacion")

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

	def delete(self):

		if not self.codes or len(self.codes) < 1 :
			self.sendMessage(MSG_ERROR,"No hay codigos insertados","Error")
			return
		
		selection = self.widgets["code_list"][0].curselection()
		if selection:
			self.codes.pop(selection[0])
		else:
			code = askstring('Codigo a buscar',"Inserte el codigo a borrar")
			if not code:
				self.sendMessage(MSG_ERROR,"No se inserto un codigo","Error")
			elif code not in self.codes:
				self.sendMessage(MSG_ERROR,"No se encuentra el codigo","Error")
			else:
				self.codes.pop(self.codes.index(code))
		self.UpdateCodes()

	def UpdateCodes(self):
		self.codes.sort()
		self.widgets["code_list"][0].delete(0,tk.END)
		if self.codes:
			for i in self.codes:
				self.widgets["code_list"][0].insert(tk.END,i)

	def load(self):
		self.file = filedialog.askopenfilename()
		if self.file:
			self.editLabel("file_label","Archivo Cargado")

	def search(self):
		if not self.file:
			self.sendMessage(MSG_ERROR,"No hay un archivo seleccionado","Error")
		elif not self.codes:
			self.sendMessage(MSG_ERROR,"No hay codigos insertados","Error")
		else:
			self.showResults(self.engine.search(self.file,self.codes))

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
	root.geometry()
	gui = program(root)
	root.mainloop()

