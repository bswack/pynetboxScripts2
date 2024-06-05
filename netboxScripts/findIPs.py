import sys
import pynetbox
import ipaddress

NETBOX_TOKEN='d8f563d5b7453c76f35686479c03c85d6961a008';

def get_network_address(cidr):
    try:
        # Create an IP network object
        network = ipaddress.ip_network(cidr, strict=False)

        # Return the network address in CIDR notation
        return str(network.network_address) + '/' + str(network.prefixlen)
    except ValueError as e:
        # Handle invalid CIDR input
        return f"Invalid CIDR input: {e}"

def main(rack_name, position, vlanid):
    # Connect to NetBox instance
    nb = pynetbox.api('http://netbox.abcnews.app', token='d8f563d5b7453c76f35686479c03c85d6961a008')

    # Find the rack id for the named rack
    racks = nb.dcim.racks.filter(name=rack_name)
    if not racks:
        print(f"No rack found with name {rack_name}")
        return
    
    for r in racks:
        rack=r
        break
        
    # Find device at specified position in the specified rack
    devices = nb.dcim.devices.filter(rack_id=rack.id, position=position)
    if not devices:
        print(f"No devices found at position {position} in rack {rack_name}")
        return
    
    if len(devices)>1:
        print(f"Too many devices found {len(devices)}")
        return
    
    for d in devices:
        device=d
        break
    
    switch_name = device.name
    
    # Find the interface    
    interface_name = f"vlan{vlanid}"
    interfaces = nb.dcim.interfaces.filter(device_id=device.id, name=interface_name)
    if not interfaces:
        print(f"No interface named {interface_name} found on device {switch_name}")
        return
        
    for i in interfaces:
        interface=i
        break;
        
    ip_addresses = nb.ipam.ip_addresses.filter(interface_id=i.id)
    
    # Find the IP address assigned to the interface
    if not ip_addresses:
        print(f"No IP address assigned to interface {interface_name} on device {switch_name}")
        return
    
    for i in ip_addresses:
        svi_ip=i
        break;       

    # Find the parent prefix for the SVI
    prefixes = nb.ipam.prefixes.filter(prefix=get_network_address(svi_ip.address))
    
    if not prefixes:
        print(f"Could not find parent prefix for {svi_ip.address}")
        return
    
    for p in prefixes:
        prefix=p
        break; 

    # Output the results
    print(f"Switch Name: {switch_name}")
    print(f"SVI: {svi_ip}")
    print("Available IPs:")    
    for a in p.available_ips.list():
        print(f"  {a}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <rack_name> <position> <vlanid>")
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3])


