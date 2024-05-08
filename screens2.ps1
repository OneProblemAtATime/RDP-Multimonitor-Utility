Add-Type -AssemblyName System.Windows.Forms
[System.Windows.Forms.Screen]::AllScreens | ForEach-Object { "Device Name: $($_.DeviceName)"; "Bounds: $($_.Bounds.ToString())"; "Working Area: $($_.WorkingArea.ToString())"; "Primary: $($_.Primary)"; "" }
