import tkinter as tk
from ControlPanel import ControlPanel

if __name__ == "__main__":
    root = tk.Tk()
    app = ControlPanel(root)
    root.mainloop()