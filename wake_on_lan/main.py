import socket
import struct

def send_magic_packet(mac_address):
    """
    Sends a magic packet to a device with the given MAC address to wake it up.

    This function constructs a magic packet for Wake-on-LAN (WoL) and sends it over the network
    to the specified MAC address. The magic packet is a broadcast frame containing 6 bytes of
    0xFF followed by 16 repetitions of the target device's MAC address.

    Parameters:
    mac_address (str): The MAC address of the device to be woken up, in human-readable format
                       (e.g., "00:11:22:33:44:55", "00-11-22-33-44-55", or "0011.2233.4455").

    Returns:
    None
    """
    # Remove any separator characters from the MAC address and convert to bytes
    mac_bytes = bytes.fromhex(mac_address.replace(':', '').replace('-', '').replace('.', ''))
    # Create the magic packet with 6 bytes of FF followed by 16 repetitions of the MAC address
    magic_packet = b'\xFF' * 6 + mac_bytes * 16

    # Create a socket for network broadcast
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        # Send the magic packet to the broadcast address
        sock.sendto(magic_packet, ('<broadcast>', 9))

# Example usage
mac_AMD_Ryzen_2600X = "30-9C-23-89-EC-8B"
send_magic_packet(mac_AMD_Ryzen_2600X.replace("-", ":"))