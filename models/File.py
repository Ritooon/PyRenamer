import tkinter as tk
from tkinter import filedialog
from os import walk
import os
from PIL import Image

class File():
   
    def __init__(self, filename, path, image, image_zoom, renamed_file):
        self.path = path
        self.filename = filename
        self.image_zoom = image_zoom
        self.image_name = image
        self.renamed_file = renamed_file

    def returnFileLabel(self, frame):
        # If recognized extension
        try:
            img = tk.PhotoImage(file=self.image_name).subsample(self.image_zoom, self.image_zoom)
        # Else, default icon
        except:
            img = tk.PhotoImage(file='assets/snake.png').subsample(self.image_zoom, self.image_zoom)

        if self.renamed_file != '':
            label = tk.Label(frame, text='{}'.format(self.renamed_file), image=img, compound=tk.LEFT, bg='#30336b', foreground='#fff')
        else: 
            label = tk.Label(frame, text='{}'.format(self.filename), image=img, compound=tk.LEFT, bg='#30336b', foreground='#fff')

        label.image = img

        return label