from tkinter import *
from tkinter import messagebox  
import csv

class Calculator:
	def __init__(self, master):
		self.master = master
		self.total = 0
		self.current_number = 0
		self.index = 0
		master.title("PyNotes")
		with open("note.csv", "a+", newline="") as csvfile: # Create csv file
			pass

		self.note_heading = Label(master, text="New Note")
		self.note_title = Label(master, text="Title:")
		self.note_text = Label(master, text="Note:")
		self.note_textbox = Text(master, bd=3)
		self.title_entry = Entry(master, bd=3, width=63)
		self.add_button = Button(master, text="Add Note", command=self.add_note, width=16)
		self.clear_button = Button(master, text="Clear", command=self.clear, width = 16)

		self.my_notes_title = Label(master, text="My notes")
		self.notes_list_scrollbar = Scrollbar(master)
		self.notes_list = Listbox(master, height=24, yscrollcommand=self.notes_list_scrollbar.set)
		self.notes_list.bind('<Double-1>', lambda x: self.show_note_button.invoke())
		self.delete_note_button = Button(master, text="Delete Note", command= self.delete_note)
		self.show_note_button = Button(master, text="Show", command= self.show_note)
		self.notes_list_scrollbar.config(command=self.notes_list.yview)
		

		self.update_notes_list() # update notes from csv

		# Layout
		self.my_notes_title.grid(row=0, column=0)
		self.notes_list.grid(row = 1, column = 0, rowspan=2, sticky=N)
		self.notes_list_scrollbar.grid(row = 1, column=2, rowspan=2, sticky=N+S)
		self.delete_note_button.grid(row = 2, sticky=S+W)
		self.show_note_button.grid(row=2, column=0, sticky=S+E)

		self.note_heading.grid(row = 0, columnspan=3, column = 3)
		self.note_title.grid(row=1, column=3)
		self.title_entry.grid(row=1, columnspan=2, column=4, sticky=W)

		self.note_text.grid(row=2, column=3, sticky=N)
		self.note_textbox.grid(rowspan=1, row=2, columnspan=2, column=4)
		self.add_button.grid(row=1, column=5)
		self.clear_button.grid(row=1, column=5, sticky=E)

		
	def add_note(self):
		data = [self.title_entry.get(), self.note_textbox.get(1.0, END).rstrip()]
		if not data[0]:
			messagebox.showerror("Error", "Note has no title")
		elif not data[1]:
			messagebox.showerror("Error", "Note has no text")
		else:
			with open("note.csv", "a+", newline="") as csvfile:
				csvwriter = csv.writer(csvfile, delimiter=",")
				csvwriter.writerow(data)
			print(self.title_entry.get())
			print(self.note_textbox.get(1.0, END))
			self.title_entry.delete(0, END)
			self.note_textbox.delete(1.0, END)
			self.update_notes_list()
	def update_notes_list(self):
		self.notes_list.delete(0, END)
		with open("note.csv", "r") as csvfile:
			csvreader = csv.reader(csvfile, delimiter=",")
			index = 1
			for row in csvreader:
				self.notes_list.insert(index, row[0])
				index += 1
				print(row)
	def delete_note(self):
		data = []
		with open("note.csv", "r") as csvfile:
			csvreader = csv.reader(csvfile, delimiter=",")
			for row in csvreader:
				data.append(row)
			index = self.notes_list.curselection()
			if index:
				del data[index[0]]
		with open("note.csv", "w", newline="") as csvfile:
			csvwriter = csv.writer(csvfile, delimiter=",")
			for note in data:
				csvwriter.writerow(note)
		self.update_notes_list()
		self.clear()
	def show_note(self):
		data = []
		self.title_entry.delete(0, END)
		self.note_textbox.delete(1.0, END)
		with open("note.csv", "r") as csvfile:
			csvreader = csv.reader(csvfile, delimiter=",")
			for row in csvreader:
				data.append(row)
			self.index = self.notes_list.curselection()
			self.title_entry.insert(0, data[self.index[0]][0])
			self.note_textbox.insert(1.0, data[self.index[0]][1])
			self.note_heading.config(text=data[self.index[0]][0])
		self.add_button.config(command=self.update_note, text="Update")

	def update_note(self):
		data = []
		with open("note.csv", "r") as csvfile:
			csvreader = csv.reader(csvfile, delimiter=",")
			for row in csvreader:
				data.append(row)

		data[self.index[0]][0] = self.title_entry.get()
		data[self.index[0]][1] = self.note_textbox.get(1.0, END)

		with open("note.csv", "w", newline="") as csvfile:
			csvwriter = csv.writer(csvfile, delimiter=",")
			for note in data:
				csvwriter.writerow(note)
		self.update_notes_list()
		self.clear()
			
	def clear(self):
		self.title_entry.delete(0, END)
		self.note_textbox.delete(1.0, END)
		self.add_button.config(command=self.add_note, text="Add")
		self.note_heading.config(text="New Note")
		self.index = 0



root = Tk()
clac = Calculator(root)
root.mainloop()