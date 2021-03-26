import tkinter as tk
from tkinter import filedialog
from os import walk
import os
from models import File
import re

class BulkRenamer():

    selected_dir = ''
    window_frame = None   

    def displayBulkRenamer(self, window):
        # Global frame
        self.window_frame = tk.Frame(window, bg='#130f40')

        # Open directory button container
        top_frame = tk.Frame(self.window_frame)
        # Open directory button
        self.image = tk.PhotoImage(file="assets/folder.png").subsample(4, 4)
        open_dir_btn = tk.Button(top_frame, text=" Open folder", font=('Helvetica', 15),
            image=self.image, command=self.open_dir, compound=tk.LEFT, bg='#686de0', foreground='#fff')
        open_dir_btn.pack(side=tk.LEFT)
        # Position of the frame on the grid
        top_frame.grid(row=0, column=0, sticky=tk.W, pady=10, padx=10)

        # Pack frames
        self.window_frame.pack(fill=tk.X)

    def preview(self):
        self.list_files(self.selected_dir, 'display_renamed_files')
    
    def reset(self):
        for child in self.window_frame.winfo_children():
            if child.winfo_name() != '!frame':
                child.destroy()

    def list_files(self, dir, list_action):
        # Directory files container frame
        dir_files_frame = tk.Frame(self.window_frame, bg='#30336b')
        # Canvas to display a scrollable container
        canvas = tk.Canvas(dir_files_frame)
        canvas.config(width=750, height=150, bg='#30336b')
        # Create new vertical scrollbar
        scrollbar = tk.Scrollbar(dir_files_frame, orient='vertical', command=canvas.yview)
        # Apply scrollbar to the frame to scroll
        scrollable_frame = tk.Frame(canvas, bg='#30336b')

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

        if list_action == 'display_renamed_files':
            if self.pos_val.get() != '':
                position = int(self.pos_val.get())
            else:
                position = 0

            if position > 0:
                i = position
            else:
                i = 0
        else:
            i = 0
            
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

            if list_action == 'display_renamed_files':
                renamed_version = "{}{}.{}".format(self.rename_mask.get(), i, extension)
            else:
                renamed_version = ''

            # Display icon + filename
            fileLabel = File.File(file, file, image, 1, renamed_version).returnFileLabel(scrollable_frame)
            fileLabel.pack()
            i += 1


        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Set position of the frame on the grid
        if list_action == 'display_original_content':

            dir_files_frame.grid(row=1, column=0, sticky=tk.W, pady=10, padx=10)
        
        elif list_action == 'display_renamed_files':
            
            preview_title_Frame = tk.Frame(self.window_frame, bg='#30336b')
            tk.Label(preview_title_Frame, text='Preview :', bg='#130f40', font=('Helvetica', 15), foreground='#fff').pack()
            preview_title_Frame.grid(row=3, column=0, sticky=tk.W, pady=5, padx=10)

            dir_files_frame.grid(row=4, column=0, sticky=tk.W, pady=10, padx=10)

            # Apply button
            apply_btn_frame = tk.Frame(self.window_frame, bg='#130f40')
            tk.Button(apply_btn_frame, text="Apply", font=('Helvetica', 10), command=self.apply ,compound=tk.LEFT, bg='#686de0', foreground='#fff').pack()
            apply_btn_frame.grid(row=5, column=0,  padx=10)


    def apply(self):
        
        files_and_folders = []
        dirpath = ''
        # Walk through files and folders
        for(dirpath, dirnames, filenames) in walk(self.selected_dir):
            files_and_folders.extend(filenames)
            break
        
        if self.pos_val.get() != '':
            position = int(self.pos_val.get())
        else:
            position = 0

        if position > 0:
            i = position
        else:
            i = 0

        for file in files_and_folders:
            # Get file extension
            extension = os.path.splitext(file)
            extension = extension[-1].replace('.', '')

            # Define the new name
            new_file_name = '{}/{}{}.{}'.format(dirpath, self.rename_mask.get(), i, extension)
            original_file = '{}/{}'.format(dirpath, file)
            # Apply new filename
            os.rename(original_file, new_file_name)
            i += 1
        
        self.reset()
            

    def stringChecker(self, P, checkType):
        if checkType == 'digit':
            if str.isdigit(P) or P == "":
                return True
            else:
                return False
        elif checkType == 'windowsFileName':
            if P != '':
                regex= re.compile('[*<>?/\\\|:"]') 
                if(regex.search(P) == None):
                    return True
                else: 
                    return False
            else:
                return True

    def open_dir(self):
        frame_size = self.window_frame.grid_size() 
        if(frame_size[1]) > 1:
            self.reset()

        # Select directory
        self.selected_dir = tk.filedialog.askdirectory()
        # If directory is selected
        if self.selected_dir != '':
            
            # Display dir files
            self.list_files(self.selected_dir, 'display_original_content')

            # Validation command
            vcmd = (self.window_frame.register(self.stringChecker))

            # Renaming options 
            renaming_options = tk.Frame(self.window_frame, bg='#130f40')
            # Renaming label
            rename_label_frame = tk.Frame(renaming_options, bg='#130f40')
            tk.Label(rename_label_frame, text='Renaming mask (e.g. : "video_")', bg='#130f40', font=('Helvetica', 10), foreground='#fff').pack()
            rename_label_frame.grid(row=0, column=0)

            # Renaming mask
            rename_mask_frame = tk.Frame(renaming_options, bg='#130f40')
            self.rename_mask = tk.Entry(rename_mask_frame, validate='all', validatecommand=(vcmd, '%S', 'windowsFileName'), font=('Helvetica', 10))
            self.rename_mask.pack(ipady=2, ipadx=10)
            rename_mask_frame.grid(row=0, column=1, padx=5)

            # Start count start position label
            start_pos_label_frame = tk.Frame(renaming_options, bg='#130f40')
            tk.Label(start_pos_label_frame, text='Start at :', bg='#130f40', font=('Helvetica', 10), foreground='#fff').pack()
            start_pos_label_frame.grid(row=0, column=2, padx=5)

            # Start count start position value
            start_pos_val_frame = tk.Frame(renaming_options, bg='#130f40')
            self.pos_val = tk.Entry(start_pos_val_frame, validate='all', validatecommand=(vcmd, '%P', 'digit'), width=6)
            self.pos_val.pack(ipady=2)
            start_pos_val_frame.grid(row=0, column=3, padx=5)

            # Preview button
            preview_btn_frame = tk.Frame(renaming_options, bg='#130f40')
            tk.Button(preview_btn_frame, text=" Preview", font=('Helvetica', 10), command=self.preview ,compound=tk.LEFT, bg='#686de0', foreground='#fff').pack()
            preview_btn_frame.grid(row=0, column=4,  padx=10)

            # Apply frame to grid
            renaming_options.grid(row=2, column=0, sticky=tk.W, pady=10, padx=10)
