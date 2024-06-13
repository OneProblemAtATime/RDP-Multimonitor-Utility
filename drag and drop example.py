import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinter import filedialog
import modded_libs.customtkinter as ctk

class DragAndDropWindow(ctk.CTkFrame):
    def __init__(self, parent, allowed_extensions, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        self.allowed_extensions = allowed_extensions
        self.info_lines = [""] * 3  # Initialize with empty lines
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.label = ctk.CTkLabel(self, text="Drag a .rdp or .txt onto this window to load it into this software", font=("Arial", 12, "bold"))
        self.label.grid(row=0, column=0, padx=10, pady=10, sticky="n")

        self.info_label = ctk.CTkLabel(self, text="", justify="left")
        self.info_label.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.update_info_terminal()

        self.label.bind("<Button-1>", self.load_file)

        parent.drop_target_register(DND_FILES)
        parent.dnd_bind('<<Drop>>', self.on_drop)

    def load_file(self, event=None):
        file_path = filedialog.askopenfilename(filetypes=[("Allowed files", f"*.{ext}") for ext in self.allowed_extensions])
        if file_path:
            self.event_on_load(file_path)
            self.check_file(file_path)

    def on_drop(self, event):
        file_path = event.data.strip('{}')
        if file_path:
            self.check_file(file_path)

    def check_file(self, file_path):
        if any(file_path.endswith(f".{ext}") for ext in self.allowed_extensions):
            self.event_on_drop_correct(file_path)
        else:
            self.event_on_drop_incorrect(file_path)

    def event_on_load(self, file_path):
        self.update_info(f"File loaded: {file_path}")

    def event_on_drop_correct(self, file_path):
        self.update_info(f"Correct file type dropped: {file_path}")

    def event_on_drop_incorrect(self, file_path):
        self.update_info(f"Incorrect file type dropped: {file_path}")

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            self.event_on_save(file_path)

    def event_on_save(self, file_path):
        self.update_info(f"File saved: {file_path}")

    def update_info(self, message):
        self.info_lines.append(message)
        self.info_lines = self.info_lines[-3:]
        self.update_info_terminal()

    def update_info_terminal(self):
        self.info_label.configure(text="\n".join(reversed(self.info_lines)))

# Example usage
if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Drag and Drop Example")
    allowed_extensions = ["rdp", "txt"]
    drag_and_drop_window = DragAndDropWindow(root, allowed_extensions)
    drag_and_drop_window.pack(expand=True, fill="both")
    root.mainloop()
