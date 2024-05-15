import wmi

def get_monitor_info():
    wmi_service = wmi.WMI(namespace='root\\wmi')
    monitors = wmi_service.WmiMonitorBasicDisplayParams()
    monitor_info = {}
    for i, monitor in enumerate(monitors):
        monitor_number = i + 1
        monitor_info[f"Monitor {monitor_number}"] = {
            "width": monitor.MaxHorizontalImageSize,
            "height": monitor.MaxVerticalImageSize,
            "instance_name": monitor.InstanceName
        }
    return monitor_info

if __name__ == "__main__":
    monitor_info = get_monitor_info()
    if monitor_info:
        for monitor, info in monitor_info.items():
            print(f"{monitor}:")
            print(f"  Width (cm): {info['width']}")
            print(f"  Height (cm): {info['height']}")
            print(f"  Instance Name: {info['instance_name']}")
    else:
        print("No monitor information found.")
