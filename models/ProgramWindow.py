import tkinter as tk
from tkinter import filedialog
from models import File
from models import BulkRenamer

class ProgramWindow():
    
    main_window = tk.Tk()

    def createMainWindow(self):
        # Main window configuration
        self. main_window.title('PyRenamer')
        self. main_window.geometry('800x600')
        self. main_window.resizable(False, False)
        self. main_window.iconbitmap('assets/python.ico')
        self. main_window.config(background='#130f40')

        # Get the window menu
        self.windowMenuCreation()
        
        return self. main_window

    def windowMenuCreation(self):
        # Menu bar - Container
        menu_bar = tk.Menu()

        # Menu bar - File section 
        menu_file = tk.Menu(menu_bar, tearoff=0)
        menu_file.add_command(label="Bulk renamer", command=BulkRenamer.BulkRenamer().displayBulkRenamer(self. main_window))
        menu_file.add_separator()
        menu_file.add_command(label="Exit", command=self. main_window.quit)
        menu_bar.add_cascade(label='File', menu=menu_file)
        
        # Menu bar - Help section 
        menu_help = tk.Menu(menu_bar, tearoff=0)
        menu_help.add_command(label="?", command=print)
        menu_bar.add_cascade(label='Help', menu=menu_help)  

        # Add menu to main window
        self. main_window.config(menu=menu_bar)