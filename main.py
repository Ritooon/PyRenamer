from tkinter import *
from models import ProgramWindow

# Display main window
appWindow = ProgramWindow.ProgramWindow()
appWindow = appWindow.createMainWindow()

appWindow.mainloop()
