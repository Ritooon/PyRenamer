import tkinter as tk
from tkinter import filedialog
from models import File
from models import BulkRenamer

class ProgramWindow():
    
    main_window = tk.Tk()

    def createMainWindow(self):
        # Main window configuration
        self.main_window.title('PyRenamer')
        self.main_window.geometry('800x600')
        positionRight = int(self.main_window.winfo_screenwidth()/3 - self.main_window.winfo_reqwidth()/2)
        positionDown = int(self.main_window.winfo_screenheight()/3 - self.main_window.winfo_reqheight()/2)
        self.main_window.geometry("+{}+{}".format(positionRight, positionDown))
        self.main_window.resizable(False, False)
        self.main_window.iconbitmap('assets/python.ico')
        self.main_window.config(background='#130f40')

        # Home buttons        
        img = tk.PhotoImage(file='assets/paper.png').subsample(1, 1)
        self.bulkBtn = tk.Button(self.main_window, image=img, compound=tk.LEFT,font=('Helvetica', 20), command=self.displayBulk,
            text=' Bulk renamer ', bg='#686de0', foreground='#fff')
        self.bulkBtn.image = img
        self.bulkBtn.pack(expand=True)

        # Get the window menu
        self.windowMenuCreation()
        
        return self.main_window

    def windowMenuCreation(self):
        # Menu bar - Container
        menu_bar = tk.Menu()

        # Menu bar - File section 
        menu_file = tk.Menu(menu_bar, tearoff=0)
        menu_file.add_command(label="Bulk renamer", command=self.displayBulk)
        menu_file.add_separator()
        menu_file.add_command(label="Exit", command=self.main_window.quit)
        menu_bar.add_cascade(label='File', menu=menu_file)
        
        # Menu bar - Help section 
        menu_help = tk.Menu(menu_bar, tearoff=0)
        menu_help.add_command(label="?", command=print)
        menu_bar.add_cascade(label='Help', menu=menu_help)  

        # Add menu to main window
        self.main_window.config(menu=menu_bar)

    def displayBulk(self):
        self.cleanWindow()
        BulkRenamer.BulkRenamer().displayBulkRenamer(self.main_window)
    
    def cleanWindow(self):
        for child in self.main_window.winfo_children():
            if child.winfo_name() != '!menu':
                child.destroy()