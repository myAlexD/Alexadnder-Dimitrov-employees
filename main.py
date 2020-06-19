from tkinter import *
from tkinter import filedialog
from Employees.Employees import Employees as emp

class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):

        self.open_file = Button(self)
        self.open_file["text"] = "Browse Files"
        self.open_file["command"] = self.file_dialog
        self.open_file.pack(side="top")

        self.quit = Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

    def file_dialog(self):
        text_display = emp(filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("csv files","*.csv"),("all files","*.*")))).output()
        '''
        label_1.config(text=f"Employee ID #1\n{text_display[0]}")
        label_1.place(x=25,y=85)
        label_2.config(text=f"Employee ID #2\n{text_display[1]}")
        label_2.place(x=120,y=85)
        label_3.config(text=f"Project ID\n{text_display[2]}")
        label_3.place(x=215,y=85)
        label_4.config(text=f"Days worked\n{text_display[3]}")
        label_4.place(x=290,y=85)
        '''

root = Tk()
root.geometry('400x120+850+300')
root.title('Employees')
label_1 = Label(root, text="Employee ID #1")
label_2 = Label(root, text="Employee ID #2")
label_3 = Label(root, text="Project ID")
label_4 = Label(root, text="Days worked")
app = Application(master=root)

app.mainloop()


