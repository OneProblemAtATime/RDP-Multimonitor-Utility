Add-Type -AssemblyName System.Windows.Forms
$Array = ([System.Windows.Forms.Screen]::AllScreens | Sort-Object -Property {$_.DisplayName})

foreach ($screen in $Array) {
    $deviceName = $screen.DeviceName.Split('\\')[-1]
    $width = $screen.Bounds.Width
    $height = $screen.Bounds.Height
    $left = $screen.Bounds.Left
    $top = $screen.Bounds.Top
    $right = $screen.Bounds.Right - 1
    $bottom = $screen.Bounds.Bottom - 1

    Write-Output "Device Name: $deviceName"
    Write-Output "Width: $width"
    Write-Output "Height: $height"
    Write-Output "Left: $left"
    Write-Output "Top: $top"
    Write-Output "Right: $right"
    Write-Output "Bottom: $bottom"
    Write-Output "" # Adding a blank line for better readability
}
