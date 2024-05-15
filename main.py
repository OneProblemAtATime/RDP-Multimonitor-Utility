# Need to make a tool that is able to search for rdp files
#   |then it should detect what type of monitors are to be
#   |used by the RDP session. After this, it should map
#   |setting screens to RDP screens and allow the user to
#   |choose the screens to pass to the RDP session.

import subprocess
import ast

# Path to your PowerShell script
script_path = 'rdp_screens_py_dict_output.ps1'
script_path_two = 'screens3.ps1'

# Command to execute PowerShell script
mstsc_screen_command = ['powershell.exe', '-ExecutionPolicy', 'Unrestricted', '-File', script_path]
system_screen_command = ['powershell.exe', '-ExecutionPolicy', 'Unrestricted', '-File', script_path_two]

# Run the PowerShell script and get the output as a string and put it into a dictionary
result = subprocess.run(mstsc_screen_command, capture_output=True, text=True)
mstsc_screen_dict = ast.literal_eval(result.stdout.strip())

result = subprocess.run(system_screen_command, capture_output=True, text=True)
system_screen_dict = ast.literal_eval(result.stdout.strip())

#print(mstsc_screen_dict)
#print(mstsc_screen_dict[0])

#print(system_screen_dict)
#print(system_screen_dict['____DISPLAY3'])


print("------------------------------")
print(mstsc_screen_dict[0])
print(system_screen_dict['____DISPLAY1'])
print("------------------------------")
print(mstsc_screen_dict[1])
print(system_screen_dict['____DISPLAY2'])
print("------------------------------")
print(mstsc_screen_dict[2])
print(system_screen_dict['____DISPLAY3'])
print("------------------------------")
print(mstsc_screen_dict[3])
print(system_screen_dict['____DISPLAY4'])
print("------------------------------")