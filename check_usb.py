import usb.core

USB_SPECIFICATION = {
    0x0: {
        "USAGE": "Device",
        "DESCRIPTION": "Unspecified",
        "EXAMPLE": "Device class is unspecified, interface descriptors are used to determine needed drivers",
    },
    0x1: {
        "USAGE": "Interface",
        "DESCRIPTION": "Audio",
        "EXAMPLE": "Speaker, microphone, sound card, MIDI",
    },
    0x2: {
        "USAGE": "Both",
        "DESCRIPTION": "Communications and CDC control",
        "EXAMPLE": "UART and RS-232 serial adapter, Modem, Wi-Fi adapter, Ethernet adapter. Used together with class 0Ah (CDC-Data) below",
    },
    0x3: {
        "USAGE": "Interface",
        "DESCRIPTION": "Human interface device (HID)",
        "EXAMPLE": "Keyboard, mouse, joystick",
    },
    0x5: {
        "USAGE": "Interface",
        "DESCRIPTION": "Physical interface device (PID)",
        "EXAMPLE": "Force feedback joystick",
    },
    0x6: {
        "USAGE": "Interface",
        "DESCRIPTION": "Image (PTP/MTP)",
        "EXAMPLE": "Webcam, scanner",
    },
    0x7: {
        "USAGE": "Interface",
        "DESCRIPTION": "Printer",
        "EXAMPLE": "Laser printer, inkjet printer, CNC machine",
    },
    0x8: {
        "USAGE": "Interface",
        "DESCRIPTION": "Mass storage (MSC or UMS)",
        "EXAMPLE": "USB flash drive, memory card reader, digital audio player, digital camera, external drive",
    },
    0x9: {
        "USAGE": "Device",
        "DESCRIPTION": "USB hub",
        "EXAMPLE": "Full bandwidth hub",
    },
    0xA: {
        "USAGE": "Interface",
        "DESCRIPTION": "CDC-Data",
        "EXAMPLE": "Used together with class 02h (Communications and CDC Control) above",
    },
    0xB: {
        "USAGE": "Interface",
        "DESCRIPTION": "Smart Card",
        "EXAMPLE": "USB smart card reader",
    },
    0xD: {
        "USAGE": "Interface",
        "DESCRIPTION": "Content security",
        "EXAMPLE": "Fingerprint reader",
    },
    0xE: {"USAGE": "Interface", "DESCRIPTION": "Video", "EXAMPLE": "Webcam"},
    0xF: {
        "USAGE": "Interface",
        "DESCRIPTION": "Personal healthcare device class (PHDC)",
        "EXAMPLE": "Pulse monitor (watch)",
    },
    0x10: {
        "USAGE": "Interface",
        "DESCRIPTION": "Audio/Video (AV)",
        "EXAMPLE": "Webcam, TV",
    },
    0x11: {
        "USAGE": "Device",
        "DESCRIPTION": "Billboard",
        "EXAMPLE": "Describes USB-C alternate modes supported by device",
    },
    0xDC: {
        "USAGE": "Both",
        "DESCRIPTION": "Diagnostic device",
        "EXAMPLE": "USB compliance testing device",
    },
    0xE0: {
        "USAGE": "Interface",
        "DESCRIPTION": "Wireless Controller",
        "EXAMPLE": "Bluetooth adapter, Microsoft RNDIS",
    },
    0xEF: {
        "USAGE": "Both",
        "DESCRIPTION": "Miscellaneous",
        "EXAMPLE": "ActiveSync device",
    },
    0xFE: {
        "USAGE": "Interface",
        "DESCRIPTION": "Application-specific",
        "EXAMPLE": "IrDA Bridge, Test & Measurement Class (USBTMC), USB DFU (Device Firmware Upgrade)",
    },
    0xFF: {
        "USAGE": "Both",
        "DESCRIPTION": "Vendor-specific",
        "EXAMPLE": "Indicates that a device needs vendor-specific drivers",
    },
}


def view_all_devices():
    devices = usb.core.find(find_all=True)
    for dev in devices:

        vendor = str(hex(dev.idVendor)).replace("0x", "")
        while len(vendor) < 4:
            vendor = "0" + vendor

        product = str(hex(dev.idProduct)).replace("0x", "")
        while len(product) < 4:
            product = "0" + product

        device_id = vendor + ":" + product
        device_class = dev.bDeviceClass

        if device_class in USB_SPECIFICATION.keys():
            dev_spc = USB_SPECIFICATION[device_class]
            usage = dev_spc.get("USAGE")
            description = dev_spc.get("DESCRIPTION")
            example = dev_spc.get("EXAMPLE")

        else:
            usage = "undefined"
            description = "undefined"
            example = "undefined"

        yield dict(
            device_id=device_id, usage=usage, description=description, example=example
        )


def main():
    print("ACTIVE DEVICES:\n\n")
    devices = [*view_all_devices()]
    for i in devices:
        print(i)

    while True:
        actual_devices = [*view_all_devices()]
        if actual_devices != devices:
            actual_ids = [item.get("device_id") for item in actual_devices]
            ids = [item.get("device_id") for item in devices]
            dif = list(set(ids) - set(actual_ids)) + list(set(actual_ids) - set(ids))

            print("\n\nChanges detected: ")
            for device in actual_devices:
                for item_id in dif:
                    if item_id in device.values():
                        print("Device connected. DETAILS: \n\n")
                        device_id = device.get("device_id")
                        usage = device.get("usage")
                        description = device.get("description")
                        example = device.get("example")
                        print(
                            f"DEVICE ID = {device_id} \nCLASS INFO: \n\tUSAGE: {usage}\n\tDESCRIPTION: {description}\n\tEXAMPLE: {example}\n\n"
                        )

            for device in devices:
                for item_id in dif:
                    if item_id in device.values():
                        print("Device disconnected. DETAILS: \n\n")
                        device_id = device.get("device_id")
                        usage = device.get("usage")
                        description = device.get("description")
                        example = device.get("example")
                        print(
                            f"DEVICE ID = {device_id} \nCLASS INFO: \n\tUSAGE: {usage}\n\tDESCRIPTION: {description}\n\tEXAMPLE: {example}\n\n"
                        )

            devices = actual_devices
            main()


if __name__ == "__main__":
    print("Listening for changes...\n")
    main()
