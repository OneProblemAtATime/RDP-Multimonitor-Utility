import subprocess
import re

def run_dumpedid():
    # Run the DumpEDID.exe program and capture its output
    result = subprocess.run(['dumpedid\\DumpEDID.exe', '-a'], capture_output=True, text=True)
    return result.stdout


if __name__ == "__main__":
    output = run_dumpedid()
    output = output.replace("\n", "").replace(" ", "")
    output = re.sub(r"SupportStandbyMode:(Yes|No).*?\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*", "", output)
    output = re.sub(r"MonitorName:.*?Inch\)", "", output)

    # Define the pattern and find all matches in one line, storing them in a list
    output = [m.group(0).strip() for m in re.finditer(r'(DISPLAY\\.*?\\.*?UID.*?M)|(\d+\s*x\s*\d+)', output, re.IGNORECASE)]


    for i in range(len(output) - 1, -1, -1):
        if len(output[i]) < 6 or (9 < len(output[i]) < 20):
            output.pop(i)

    for i in range(0, len(output), 2):
        output[i] = output[i][:-1]

    print(output)