
import csv
import pynetbox

NETBOX_TOKEN='d8f563d5b7453c76f35686479c03c85d6961a008';

def get_room_designation(rack_name):
    parts = rack_name.rsplit('.', 1)
    return parts[0] if len(parts) > 1 else ''

def get_rack_designation(rack_name):
    parts = rack_name.rsplit('.', 1)
    return parts[1] if len(parts) > 1 else ''

def create_mnemonic(device):
    room = get_room_designation(device.rack.name)
    rack = get_rack_designation(device.rack.name)
    position = int(device.position)
    return f"{room}.ESW {rack}.{position:02d}"

def main():
    # Configure API token and URL
    nb = pynetbox.api('https://netbox.abcnews.app', token=NETBOX_TOKEN)

    # Retrieve devices manufactured by Arista
    arista_devices = nb.dcim.devices.filter(manufacturer='arista')

    # Process and write to CSV
    with open('arista_devices.csv', 'w', newline='') as csvfile:
        fieldnames = ['Mnemonic','Device Name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for device in arista_devices:
            if device.rack and device.position:
                mnemonic = create_mnemonic(device)
                writer.writerow({'Mnemonic': mnemonic, 'Device Name': device.name})

if __name__ == "__main__":
    main()

