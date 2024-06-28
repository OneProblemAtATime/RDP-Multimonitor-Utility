import customtkinter as ctk, tkinter as tk, ast, subprocess, os, sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class Multiscreen_RDP_util(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Multi-monitor RDP Utility")
        #self.iconbitmap("icon.ico")
        self.geometry("800x800")
        self.resizable(True, True)   

        self.canvas = tk.Canvas(self, width=800, height=400, bg=self.cget("fg_color")[0], highlightthickness=0)
        self.canvas.pack()

        self.monitors = []
        self.selected_monitor = None

        self.create_monitor_boxes()

    def create_monitor_boxes(self):
        self.scale_factor = .1  # Scaling down by one decimal place
        self.gap = 30*self.scale_factor
        self.update()  # Required to use the .winfo_width/.winfo_height attributes

        self.bbox = [float('inf'), float('inf'), float('-inf'), float('-inf')]  # Initialize bbox

        for monitor in mstsc_screen_dict:
            scaled_tlx = mstsc_screen_dict[monitor]['TLX'] * self.scale_factor + self.gap  # Centering horizontally on the canvas
            scaled_tly = mstsc_screen_dict[monitor]['TLY'] * self.scale_factor + self.gap  # Centering vertically on the canvas and raising by half of the tallest monitor height
            scaled_brx = mstsc_screen_dict[monitor]['BRX'] * self.scale_factor - self.gap
            scaled_bry = mstsc_screen_dict[monitor]['BRY'] * self.scale_factor - self.gap

            # Update bbox
            self.bbox[0] = min(self.bbox[0], scaled_tlx)
            self.bbox[1] = min(self.bbox[1], scaled_tly)
            self.bbox[2] = max(self.bbox[2], scaled_brx)
            self.bbox[3] = max(self.bbox[3], scaled_bry)

        self.create_inner_canvas()

    def create_inner_canvas(self):
        self.update()

        inner_width = self.bbox[2] - self.bbox[0]
        inner_height = self.bbox[3] - self.bbox[1]
        
        self.inner_canvas = tk.Canvas(self.canvas, width=inner_width, height=inner_height, bg=self.cget("fg_color")[0], highlightthickness=0)
        self.inner_canvas.place(x=(self.canvas.winfo_width() - inner_width) / 2, y=(self.canvas.winfo_height() - inner_height) / 2)

        # Draw the monitor boxes on the inner canvas
        for monitor in mstsc_screen_dict:
            scaled_tlx = (mstsc_screen_dict[monitor]['TLX'] * self.scale_factor + self.gap) - self.bbox[0]
            scaled_tly = (mstsc_screen_dict[monitor]['TLY'] * self.scale_factor + self.gap) - self.bbox[1]
            scaled_brx = (mstsc_screen_dict[monitor]['BRX'] * self.scale_factor - self.gap) - self.bbox[0]
            scaled_bry = (mstsc_screen_dict[monitor]['BRY'] * self.scale_factor - self.gap) - self.bbox[1]

            box = self.inner_canvas.create_rectangle(scaled_tlx, scaled_tly, scaled_brx, scaled_bry, outline='black', fill='gray', tags="monitor_inner")
            self.monitors.append(box)

        self.inner_canvas.tag_bind("monitor_inner", "<Button-1>", self.on_monitor_click)

    def on_monitor_click(self, event):
        clicked_item = self.inner_canvas.find_closest(event.x, event.y)
        if clicked_item:
            if self.selected_monitor:
                self.inner_canvas.itemconfig(self.selected_monitor, fill='gray')
            self.selected_monitor = clicked_item[0]
            self.inner_canvas.itemconfig(self.selected_monitor, fill='green')

    def run(self):
        self.mainloop()

if __name__ == '__main__':
    # Path to your PowerShell script
    script_path = resource_path('rdp_screens.ps1')

    # Command to execute PowerShell script
    mstsc_screen_command = ['powershell.exe', '-ExecutionPolicy', 'Unrestricted', '-File', script_path]

    # Run the PowerShell script and get the output as a string and put it into a dictionary
    result = subprocess.run(mstsc_screen_command, capture_output=True, text=True)
    mstsc_screen_dict = ast.literal_eval(result.stdout.strip())

    app = Multiscreen_RDP_util()
    app.run()
