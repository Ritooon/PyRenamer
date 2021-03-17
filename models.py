#
import tkinter as tk
from tkinter import filedialog
from os import walk
import os
from PIL import Image

class File():
   
    def __init__(self, filename, path, image, image_zoom):
        self.path = path
        self.filename = filename
        self.image_zoom = image_zoom
        self.image_name = image

    def returnFileLabel(self, frame):
        print(self.image_name)
        # If recognized extension
        try:
            img = tk.PhotoImage(file=self.image_name).subsample(self.image_zoom, self.image_zoom)
        # Else, default icon
        except:
            img = tk.PhotoImage(file='assets/snake.png').subsample(self.image_zoom, self.image_zoom)

        label = tk.Label(frame, text='{}'.format(self.filename), image=img, compound=tk.LEFT)
        label.image = img

        return label


class ProgramWindow():
    
    main_window = tk.Tk()

    def createMainWindow(self):
        # Main window configuration
        self. main_window.title('PyRenamer')
        self. main_window.geometry('800x600')
        self. main_window.iconbitmap('assets/python.ico')
        self. main_window.config(background='#CCC')

        # Get the window menu
        self.windowMenuCreation()
        
        return self. main_window

    def windowMenuCreation(self):
        # Menu bar - Container
        menu_bar = tk.Menu()

        # Menu bar - File section 
        menu_file = tk.Menu(menu_bar, tearoff=0)
        menu_file.add_command(label="Bulk renamer", command=BulkRenamer().displayBulkRenamer(self. main_window))
        menu_file.add_separator()
        menu_file.add_command(label="Exit", command=self. main_window.quit)
        menu_bar.add_cascade(label='File', menu=menu_file)
        
        # Menu bar - Help section 
        menu_help = tk.Menu(menu_bar, tearoff=0)
        menu_help.add_command(label="?", command=print)
        menu_bar.add_cascade(label='Help', menu=menu_help)  

        # Add menu to main window
        self. main_window.config(menu=menu_bar)

class BulkRenamer():

    selected_dir = ''
    window_frame = None   


    def displayBulkRenamer(self, window):
        # Global frame
        self.window_frame = tk.Frame(window, bg='#CCC')

        # Open directory button container
        top_frame = tk.Frame(self.window_frame)
        # Open directory button
        self.image = tk.PhotoImage(file="assets/folder.png").subsample(4, 4)
        open_dir_btn = tk.Button(top_frame, text="Open folder", font=('Helvetica', 15),
            image=self.image, command=self.open_dir, compound=tk.LEFT)
        open_dir_btn.pack(side=tk.LEFT)
        # Position of the frame on the grid
        top_frame.grid(row=0, column=0, sticky=tk.W, pady=10, padx=10)

        # Pack frames
        self.window_frame.pack(fill=tk.X)


    def open_dir(self):
        # Select directory
        self.selected_dir = tk.filedialog.askdirectory()
        # If directory is selected
        if self.selected_dir != '':
            # Directory files container frame
            dir_files_frame = tk.Frame(self.window_frame, bg='#fff')
            # Canvas to display a scrollable container
            canvas = tk.Canvas(dir_files_frame)
            # Create new vertical scrollbar
            scrollbar = tk.Scrollbar(dir_files_frame, orient='vertical', command=canvas.yview)
            # Apply scrollbar to the frame to scroll
            scrollable_frame = tk.Frame(canvas)

            # bin scroll to recalculate scrollable size
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(
                    scrollregion=canvas.bbox("all")
                )
            )

            # Apply scrollbar to the window
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            files_and_folders = []
            # Walk through files and folders
            for(dirpath, dirnames, filenames) in walk(self.selected_dir):
                files_and_folders.extend(filenames)
                break
        
            icons = { 'pdf': 'pdf.png', 'png': 'picture.png', 'jpg': 'picture.png'
                , 'jpeg': 'picture.png', 'bmp': 'picture.png', 'gif': 'picture.png'
                , 'xls': 'excel.png', 'xlsx': 'excel.png', 'doc': 'word.png'
                , 'docx': 'word.png', 'ppt': 'powerpoint.png', 'pptx': 'powerpoint.png'
            }

            for file in files_and_folders:
                # Get file extension
                extension = os.path.splitext(file)
                extension = extension[-1].replace('.', '')

                # If recognized extension
                try:
                    image = "assets/{}".format(icons[extension])
                # Else, default icon
                except:
                    image = "assets/snake.png"

                # Display icon + filename
                fileLabel = File(file, file, image, 1).returnFileLabel(scrollable_frame)
                fileLabel.pack()

            # Pack canvas and scrollbar
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            # Set position of the frame on the grid
            dir_files_frame.grid(row=1, column=0, sticky=tk.W, pady=10, padx=10)
