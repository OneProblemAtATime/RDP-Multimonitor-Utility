Add-Type -AssemblyName System.Windows.Forms

# Initialize the output as a Python dictionary in string format
$pythonDictOutput = "{"

# Get all screen information
[System.Windows.Forms.Screen]::AllScreens | ForEach-Object {
    # Device name processing for use as a Python dictionary key
    $deviceName = $_.DeviceName -replace '[\\.]', '_'

    # Format each screen's properties as a sub-dictionary in Python syntax
    $screenInfo = "`"$deviceName`": {"
    $screenInfo += "`"Bounds`": $($_.Bounds.ToString().Replace("X", '`"X`"').Replace("Y", '`"Y`"').Replace("Width", '`"Width`"').Replace("Height", '`"Height`"')), "
    $screenInfo += "`"WorkingArea`": $($_.WorkingArea.ToString().Replace("X", '`"X`"').Replace("Y", '`"Y`"').Replace("Width", '`"Width`"').Replace("Height", '`"Height`"')), "
    $screenInfo += "`"Primary`": $($_.Primary)"
    $screenInfo += "}, "

    # Append each screen's dictionary to the main dictionary output
    $pythonDictOutput += $screenInfo
}

# Close the main dictionary string
$pythonDictOutput += "}"

# Output the complete Python dictionary string
Write-Output $pythonDictOutput.Replace("=", ":").Replace(", }", "}")
