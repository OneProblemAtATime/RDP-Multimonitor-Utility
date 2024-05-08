Add-Type -AssemblyName 'UIAutomationClient'

#Start mstsc.exe with the argument /l, retain a process reference in $mstscProc
$mstscProc = Start-Process -FilePath 'mstsc.exe' -ArgumentList '/l' -PassThru
try {
  $handle = $null
  #MainWindowHandle sometimes returns 0, this while loop is a workaround
  while ((-not $mstscProc.HasExited) -and ($null -eq $handle))
  {
    Start-Sleep -Milliseconds 500
    $mstscProc.Refresh()
    if ($mstscProc.MainWindowHandle -ne 0)
    {
      $handle = $mstscProc.MainWindowHandle
    }
  }

  $cTrue = [System.Windows.Automation.PropertyCondition]::TrueCondition
  #Get the root element of the mstsc.exe process by handle
  $root = [System.Windows.Automation.AutomationElement]::FromHandle($handle)

  $rawText = $root.FindAll("Children", $cTrue) | 
    Select-Object -ExpandProperty Current | 
    # I used inspect.exe from the WinSDK to determine the AutomationId for the element containing the text
    Where-Object AutomationId -ieq 'ContentText' | 
    Select-Object -ExpandProperty Name  
}
finally {
  $mstscProc | Stop-Process -Force  
}

#split the raw text and process one line at a time
$pythonList = $rawText -split '\r?\n' | ForEach-Object {
  $parts = @()
  try {
    # Convert the line format "0: 1920 x 1080; (0, 0, 1919, 1079)" into numbers separated by , then split
    $parts = @($_ -replace ':', ',' -replace ' x ', ',' -replace ';', ',' -replace '[() ]', '').Split(',')    
  }
  catch {
    # If any exceptions occur we assume the line is malformed
    $_ | Write-Verbose
  }
  
  if ($parts.Length -eq 7) {
    # A well-formed line should have 7 parts
    # Create a string that looks like a Python dictionary
    $index, $width, $height, $left, $top, $right, $bottom = $parts
    "$index`: {`"Width`": $width, `"Height`": $height, `"Left`": $left, `"Top`": $top, `"Right`": $right, `"Bottom`": $bottom},"
  }
} | Out-String

# Remove extra newlines and wrap the result in square brackets to form a Python list
$pythonList = $pythonList.Trim()
$pythonList = $pythonList.Substring(0, $pythonList.Length-1)
$pythonList = ($pythonList -replace '\r?\n', ' ')
$pythonList = "{" + $pythonList + "}"
$pythonList

