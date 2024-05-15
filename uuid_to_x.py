import wmi
import win32api

def get_monitor_coordinates():
    # Get monitor handles and their info
    monitors = win32api.EnumDisplayMonitors()
    monitor_coords = []
    for monitor in monitors:
        monitor_info = win32api.GetMonitorInfo(monitor[0])
        device = monitor_info.get("Device")
        coordinates = {
            'Device': device,
            'Left': monitor_info.get("Monitor")[0],
            'Top': monitor_info.get("Monitor")[1],
            'Right': monitor_info.get("Monitor")[2],
            'Bottom': monitor_info.get("Monitor")[3]
        }
        monitor_coords.append(coordinates)
    return monitor_coords

def list_all_monitor_device_paths():
    wmi_service = wmi.WMI()
    monitors = wmi_service.Win32_PnPEntity(ConfigManagerErrorCode=0)
    
    monitor_paths = []
    for monitor in monitors:
        if "DISPLAY" in monitor.PNPDeviceID:
            monitor_paths.append(monitor.PNPDeviceID)
    return monitor_paths

# Get all monitor coordinates
monitor_coordinates = get_monitor_coordinates()

# Get all monitor device paths
monitor_device_paths = list_all_monitor_device_paths()

# Print coordinates for each monitor
for device_path in monitor_device_paths:
    print(f"Device Path: {device_path}")
    for coords in monitor_coordinates:
        print(coords)
        if coords['Device'] in device_path:
            print(f"Left x-coordinate: {coords['Left']}")
            print(f"Top y-coordinate: {coords['Top']}")
            print(f"Right x-coordinate: {coords['Right']}")
            print(f"Bottom y-coordinate: {coords['Bottom']}")
            break
    else:
        print("Coordinates not found for this device path.")
    print("-----")
