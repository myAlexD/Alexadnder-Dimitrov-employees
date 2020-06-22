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
        self.open_file.pack(side="top", fill=X, pady=30)
        self.quit = Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom", fill=X, pady=150)

    def file_dialog(self):
        label_1 = Label(root, text="")
        label_2 = Label(root, text="")
        label_3 = Label(root, text="")
        label_4 = Label(root, text="")
        label_5 = Label(root, text="")
        label_6 = Label(root, text="")
        text_display = emp(filedialog.askopenfilename(initialdir = "/",
                                title = "Select file",
                                filetypes = (("csv files","*.csv"),("all files","*.*")))).output()
        print(text_display)
        if type(text_display) == str:
            label_6 = Label(root, text="There are no employees that worked togather")
            label_6.place(x=25, y=100)               
        elif len(text_display.keys()) > 1:
            label_6 = Label(root, text=f"Ties: {len(text_display.keys())}")
            label_6.place(x=25, y=100)
        else:
            print("Here")
            column1 = []
            column2 = []
            column3 = []
            column4 = []
            for result in text_display.keys():
                column1.append(result[0])
                column2.append(result[1])
                column3.append(", ".join([key for key in text_display[result].keys() if key != 'total']))
                column4.append(text_display[result]["total"])
            
            column1 = "\n".join(column1)
            column2 = "\n".join(column2)
            column3 = "\n".join([l for l in column3])
            column4 = "\n".join([str(x) for x in column4])
            label_1.config(text=f"Employee ID #1\n{column1}")
            label_1.place(x=25,y=125)
            label_2.config(text=f"Employee ID #2\n{column2}")
            label_2.place(x=120,y=125)
            label_3.config(text=f"Project ID\n{column3}")
            label_3.place(x=215,y=125)
            label_4.config(text=f"Days worked\n{column4}")
            label_4.place(x=290,y=125)
        


root = Tk()
root.geometry('700x300')
root.title('Employees')
app = Application(master=root)

app.mainloop()


