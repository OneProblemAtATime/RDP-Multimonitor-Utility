# Hard-coded UUID
$targetUUID = "12613"

# Function to parse EDID and get monitor UUID and other details
function ParseEDID {
    param (
        [byte[]]$edid
    )
    
    $uuid = [BitConverter]::ToString($edid[8..15]) -replace '-'
    $manufacturer = [System.Text.Encoding]::ASCII.GetString($edid[8..9])
    $productCode = [BitConverter]::ToUInt16($edid[10..11], 0)
    $serialNumber = [BitConverter]::ToUInt32($edid[12..15], 0)

    [PSCustomObject]@{
        UUID = $uuid
        Manufacturer = $manufacturer
        ProductCode = $productCode
        SerialNumber = $serialNumber
    }
}

# Function to retrieve monitor information using WMI
function Get-MonitorInfo {
    $monitors = Get-WmiObject -Namespace root\wmi -Class WmiMonitorDescriptorMethods
    $monitorInfoList = @()

    foreach ($monitor in $monitors) {
        $edid = $monitor.WmiGetMonitorRawEEdidV1Block(0)
        $monitorInfo = ParseEDID -edid $edid

        $monitorInfoList += [PSCustomObject]@{
            UUID = $monitorInfo.UUID
            InstanceName = $monitor.InstanceName
            ManufacturerName = $monitor.ManufacturerName
            ProductCodeID = $monitor.ProductCode
            SerialNumberID = $monitor.SerialNumber
            UserFriendlyName = $monitor.UserFriendlyName
        }
    }

    return $monitorInfoList
}

# Function to retrieve monitor coordinates using Win32 API
function Get-MonitorCoordinates {
    $monitorCoordinates = @()
    
    Add-Type @"
using System;
using System.Runtime.InteropServices;
public class MonitorHelper {
    [StructLayout(LayoutKind.Sequential)]
    public struct RECT {
        public int Left;
        public int Top;
        public int Right;
        public int Bottom;
    }

    [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Auto)]
    public class MonitorInfo {
        public int cbSize = Marshal.SizeOf(typeof(MonitorInfo));
        public RECT rcMonitor = new RECT();
        public RECT rcWork = new RECT();
        public int dwFlags = 0;
    }

    public delegate bool MonitorEnumProc(IntPtr hMonitor, IntPtr hdcMonitor, ref RECT lprcMonitor, IntPtr dwData);

    [DllImport("user32.dll")]
    [return: MarshalAs(UnmanagedType.Bool)]
    public static extern bool EnumDisplayMonitors(IntPtr hdc, IntPtr lprcClip, MonitorEnumProc lpfnEnum, IntPtr dwData);

    [DllImport("user32.dll", CharSet = CharSet.Auto)]
    public static extern bool GetMonitorInfo(IntPtr hMonitor, MonitorInfo lpmi);

    public static void EnumerateMonitors() {
        MonitorEnumProc callback = (IntPtr hMonitor, IntPtr hdcMonitor, ref RECT lprcMonitor, IntPtr dwData) => {
            MonitorInfo mi = new MonitorInfo();
            if (GetMonitorInfo(hMonitor, mi)) {
                $monitorCoordinates.Add((IntPtr)$hMonitor, new int[] { mi.rcMonitor.Left, mi.rcMonitor.Top, mi.rcMonitor.Right, mi.rcMonitor.Bottom });
            }
            return true;
        };
        EnumDisplayMonitors(IntPtr.Zero, IntPtr.Zero, callback, IntPtr.Zero);
    }
}
"@

    [MonitorHelper]::EnumerateMonitors()
    
    return $monitorCoordinates
}

# Function to combine monitor info and coordinates
function Get-MonitorInfoWithCoordinates {
    $monitorInfoList = Get-MonitorInfo
    $monitorCoordinates = Get-MonitorCoordinates

    foreach ($monitor in $monitorInfoList) {
        foreach ($coord in $monitorCoordinates) {
            if ($monitor.InstanceName -eq $coord.Key) {
                $monitor | Add-Member -MemberType NoteProperty -Name Left -Value $coord.Value[0]
                $monitor | Add-Member -MemberType NoteProperty -Name Top -Value $coord.Value[1]
                $monitor | Add-Member -MemberType NoteProperty -Name Right -Value $coord.Value[2]
                $monitor | Add-Member -MemberType NoteProperty -Name Bottom -Value $coord.Value[3]
            }
        }
    }

    # Filter to only include the monitor with the hard-coded UUID
    return $monitorInfoList | Where-Object { $_.UUID -eq $targetUUID }
}

# Display monitor information with UUID and coordinates for the target UUID
$monitorInfoWithCoordinates = Get-MonitorInfoWithCoordinates
$monitorInfoWithCoordinates | Format-Table -AutoSize
