import ast, subprocess, os, sys, json
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def json_import_export(path=".", file_name="data.json", mode='r', data=None):
    return_data = None
    with open(f"{path}\\{file_name}", f'{mode}') as data_file:
        if os.path.exists(f"{path}\\{file_name}") or mode == 'w':
            return_data = json.load(data_file) if mode == 'r' else json.dump(data, data_file)
    return return_data

def file_read_write(path=".", file_name="session.rdp", mode='r', data=[]):
    return_data = None
    if not os.path.exists(f"{path}\\{file_name}"):
        if mode == 'w':
            with open(f"{path}\\{file_name}", f'{mode}') as data_file:
                for i in range(len(data)):
                    return_data += f"{data[i]}\n"
                data_file.write(return_data)
    else:
        if mode == 'r':
            with open(f"{path}\\{file_name}", f'{mode}b') as data_file:
                return_data = data_file.readlines()
                for i, line_data in enumerate(return_data):
                    return_data[i] = line_data.decode('utf-8')
    return return_data
        
    
def Find_RDPs(file_path_list):
    rdp_files = []
    for item in file_path_list:
        if os.path.isfile(item):# Should apply changes to a single RDP file
            if item.endswith(".rdp"):
                rdp_files.append(item)
        elif os.path.isdir(item):# Should apply changes to all RDP files in the directory
            for root, dirs, files in os.walk(item):
                for name in files:
                    if name.endswith(".rdp"):
                        file_full_path = os.path.join(root, name)
                        rdp_files.append(file_full_path)
        else:# Should cancel load if a rdp file has not been found.
            print(f"No rdp file was found.")
            return None
    return rdp_files# Should return a list of the rdp files to operate on

class Multiscreen_RDP_util(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Multi-monitor RDP Utility")
        self.geometry("800x400")
        self.resizable(True, True)

        self.monitors = []
        self.selected_slot = None
        self.load_slots = {}
        self.slot_frames = {}

        self.create_widgets()
        self.create_monitor_boxes()
        self.create_load_list()

    def create_widgets(self):
        self.canvas = tk.Canvas(self, width=800, height=250, bg=self.cget("fg_color")[0], highlightthickness=0)
        self.canvas.pack()

        self.frame = ctk.CTkFrame(self)
        self.frame.pack(fill="both", expand=True)

        self.load_list_frame = ctk.CTkScrollableFrame(self.frame, bg_color=self.cget("fg_color")[0])
        self.load_list_frame.pack(padx=10, pady=10, side="left", fill="both", expand=True)
        self.load_list_frame.grid_columnconfigure(1, weight=1)
            
        self.interaction_window = ctk.CTkScrollableFrame(self.frame, width=500, height=500, bg_color=self.cget("fg_color")[0])
        self.interaction_window.pack(padx=10, pady=10, side="right", fill="both", expand=True)
        self.interaction_window.grid_columnconfigure(1, weight=1)

        ##### Interactables for changing operations to an RDP session.
        # IP address select
        # Short and long description
        # Import/Export IP Address config
        # Handle monitor configuration change rules
        # Quick defaults for running in a directory with one or more rdps to configure
        # Import/Export full profile
        # Connect now
        # Save auto connect ip address set
        # (Side note: should make a batch script to call this in quick and auto connect mode)
        # (Side note: can I change something in the batch script to carry around when moved?)

        # Column 1
        self.toggle_1 = ctk.CTkSwitch(self.interaction_window, text="Toggle 1")
        self.toggle_1.grid(row=0, column=0, padx=10, pady=10)

        self.text_entry_1 = ctk.CTkEntry(self.interaction_window, placeholder_text="Enter text 1")
        self.text_entry_1.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

        self.button_1 = ctk.CTkButton(self.interaction_window, text="Button 1", command=self.button_1_click)
        self.button_1.grid(row=2, column=0, padx=10, pady=10)

        self.label_1 = ctk.CTkLabel(self.interaction_window, text="Label 1")
        self.label_1.grid(row=3, column=0, padx=10, pady=10)

        # Column 2
        self.toggle_2 = ctk.CTkSwitch(self.interaction_window, text="Toggle 2")
        self.toggle_2.grid(row=0, column=1, padx=10, pady=10)

        #self.text_entry_2 = ctk.CTkEntry(self.interaction_window, placeholder_text="Enter text 2")
        #self.text_entry_2.grid(row=1, column=1, padx=10, pady=10)

        self.button_2 = ctk.CTkButton(self.interaction_window, text="Button 2", command=self.button_2_click)
        self.button_2.grid(row=2, column=1, padx=10, pady=10)

        self.label_2 = ctk.CTkLabel(self.interaction_window, text="Label 2")
        self.label_2.grid(row=3, column=1, padx=10, pady=10)

    def button_1_click(self):
        # Define what happens when button 1 is clicked
        print(f"Button 1 clicked, text: {self.text_entry_1.get()}")

    def button_2_click(self):
        # Define what happens when button 2 is clicked
        print(f"Button 2 clicked, text: {self.text_entry_2.get()}")

    def create_monitor_boxes(self):
        self.scale_factor = .07
        self.gap = 30 * self.scale_factor
        self.update()

        self.bbox = [float('inf'), float('inf'), float('-inf'), float('-inf')]

        for monitor in mstsc_screen_dict:
            scaled_tlx = mstsc_screen_dict[monitor]['TLX'] * self.scale_factor + self.gap
            scaled_tly = mstsc_screen_dict[monitor]['TLY'] * self.scale_factor + self.gap
            scaled_brx = mstsc_screen_dict[monitor]['BRX'] * self.scale_factor - self.gap
            scaled_bry = mstsc_screen_dict[monitor]['BRY'] * self.scale_factor - self.gap

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

        for monitor in mstsc_screen_dict:
            scaled_tlx = (mstsc_screen_dict[monitor]['TLX'] * self.scale_factor + self.gap) - self.bbox[0]
            scaled_tly = (mstsc_screen_dict[monitor]['TLY'] * self.scale_factor + self.gap) - self.bbox[1]
            scaled_brx = (mstsc_screen_dict[monitor]['BRX'] * self.scale_factor - self.gap) - self.bbox[0]
            scaled_bry = (mstsc_screen_dict[monitor]['BRY'] * self.scale_factor - self.gap) - self.bbox[1]

            box = self.inner_canvas.create_rectangle(scaled_tlx, scaled_tly, scaled_brx, scaled_bry, outline=self.cget("fg_color")[0], fill='gray', tags="monitor_inner")
            self.monitors.append(box)

        self.inner_canvas.tag_bind("monitor_inner", "<Button-1>", self.on_monitor_click)

    def create_load_list(self):
        self.slot_colors = ['red', 'blue', 'green', 'yellow', 'purple', 'orange', 'cyan', 'magenta']
        for i in range(len(mstsc_screen_dict)):
            slot = ctk.CTkFrame(self.load_list_frame, bg_color="white", width=280, height=10)
            slot.pack(padx=10, pady=5, fill="x")
            slot.bind("<Button-1>", lambda event, i=i: self.on_slot_click(event, i))
            self.load_slots[i] = None
            self.slot_frames[i] = slot
            label = tk.Label(slot, text="", bg="white", fg="gray50", font=("Arial", 20))
            label.pack(fill="both", expand=True)
            slot.label = label

            # Ensure the label does not interfere with the slot click event
            label.bind("<Button-1>", lambda event, i=i: self.on_slot_click(event, i))

    def on_monitor_click(self, event):
        clicked_item = self.inner_canvas.find_closest(event.x, event.y)
        if clicked_item and self.selected_slot is not None:
            monitor_id = clicked_item[0]
            slot_index = self.selected_slot
            current_monitor = self.load_slots.get(slot_index)

            if current_monitor == monitor_id:
                # If clicking the same monitor twice, remove it from the slot
                self.inner_canvas.itemconfig(monitor_id, fill='gray')
                self.load_slots[slot_index] = None
                self.clear_slot(slot_index)
            else:
                # Remove the color from the previously selected monitor
                if current_monitor is not None:
                    self.inner_canvas.itemconfig(current_monitor, fill='gray')

                # Remove monitor from any previous slot
                for key, value in self.load_slots.items():
                    if value == monitor_id:
                        self.inner_canvas.itemconfig(value, fill='gray')
                        self.load_slots[key] = None
                        self.clear_slot(key)
                        break

                self.load_slots[slot_index] = monitor_id
                self.inner_canvas.itemconfig(monitor_id, fill=self.slot_colors[slot_index])
                self.fill_slot(slot_index, monitor_id)

            self.print_loaded_monitors()

    def on_slot_click(self, event, slot_index):
        if self.selected_slot is not None:
            # Set the previously selected slot to white if it is empty, otherwise set it to its monitor's color
            if self.load_slots[self.selected_slot] is None:
                self.slot_frames[self.selected_slot].configure(bg_color="white")
                self.slot_frames[self.selected_slot].label.config(bg="white")
            else:
                self.slot_frames[self.selected_slot].configure(bg_color=self.slot_colors[self.selected_slot])
                self.slot_frames[self.selected_slot].label.config(bg=self.slot_colors[self.selected_slot])

        self.selected_slot = slot_index
        if self.load_slots[slot_index] is None:
            self.slot_frames[slot_index].configure(bg_color='gray')
            self.slot_frames[slot_index].label.config(bg='gray')

    def clear_slot(self, slot_index):
        slot = self.slot_frames[slot_index]
        slot.configure(bg_color="white")
        slot.label.config(text="", bg="white")

    def fill_slot(self, slot_index, monitor_id):
        slot = self.slot_frames[slot_index]
        slot.configure(bg_color=self.slot_colors[slot_index])
        slot.label.config(text=f"Monitor {monitor_id}", bg=self.slot_colors[slot_index], fg="gray50")

    def print_loaded_monitors(self):
        loaded_monitors = [self.load_slots[i]-1 for i in sorted(self.load_slots.keys()) if self.load_slots[i] is not None]
        print(loaded_monitors)

    def run(self):
        self.update_idletasks()  # Update the geometry of all widgets
        frame_width = self.frame.winfo_width() // 2
        frame_height = self.frame.winfo_height() // 2
        self.load_list_frame.configure(width=frame_width, height=frame_height)
        self.mainloop()

if __name__ == '__main__':
    rdp_files = Find_RDPs(sys.argv[1:]) if len(sys.argv) > 1 else json_import_export(path=".", file_name="data.json", mode="r", data="")

    if rdp_files:# Remove non-existent files
        # Starting at the last index (e.g. 3) to -1 which will stop at 0 in steps of -1
        # len(rdp_files)-1 is the index of the last element of the list
        for i in range(len(rdp_files)-1, -1, -1): 
            if not os.path.exists(rdp_files[i]):
                rdp_files.pop(i)

        print(rdp_files)

    rdp_commands = file_read_write(path=".\\rdp\\", file_name="full screen.rdp", mode="r", data=None)
    print(rdp_commands)

    if rdp_files:# Start up the UI
        save_file = json_import_export(path=".", file_name="data.json", mode="w", data=rdp_files)
        
        script_path = resource_path('rdp_screens.ps1')
        mstsc_screen_command = ['powershell.exe', '-ExecutionPolicy', 'Unrestricted', '-File', script_path]
        result = subprocess.run(mstsc_screen_command, capture_output=True, text=True)
        mstsc_screen_dict = ast.literal_eval(result.stdout.strip())

        app = Multiscreen_RDP_util()
        app.run()
    else:
        print("No rdp file was found. Please drag a rdp file over the executable to begin. Refer to \"Instructions.txt\" for more information.")
        input("Press enter to exit...")