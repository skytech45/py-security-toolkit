import sys
import argparse
from scapy.all import ARP, Ether, srp
from colorama import Fore, Style, init
from utils import print_status

init(autoreset=True)

# ─────────────────────────────────────────────────────────────────
# py-security-toolkit | arp_scanner.py
# Author : skytech45
# Desc   : Scan the local network for active devices using ARP.
# ─────────────────────────────────────────────────────────────────

def scan_arp(target_ip: str, timeout: int = 2):
    """
    Send ARP requests to a target IP range and return active devices.
    """
    print_status(f"Starting ARP scan on: {target_ip}", "cyan")
    
    # Create ARP request packet
    # pdst is the target IP range
    arp = ARP(pdst=target_ip)
    
    # Create Ether broadcast packet
    # ff:ff:ff:ff:ff:ff is the broadcast MAC address
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    
    # Stack layers
    packet = ether/arp
    
    try:
        # Send and receive packets
        # srp: send and receive packets at layer 2
        result = srp(packet, timeout=timeout, verbose=False)[0]
        
        devices = []
        for sent, received in result:
            devices.append({'ip': received.psrc, 'mac': received.hwsrc})
            
        return devices
    except PermissionError:
        print_status("Permission denied. ARP scanning requires root/sudo privileges.", "error")
        return None
    except Exception as e:
        print_status(f"An error occurred: {e}", "error")
        return None

def main():
    parser = argparse.ArgumentParser(description="Scan the local network for active devices using ARP.")
    parser.add_argument("-t", "--target", required=True, help="Target IP range (e.g., 192.168.1.0/24)")
    parser.add_argument("--timeout", type=int, default=2, help="Timeout for ARP requests (default: 2)")
    
    args = parser.parse_args()
    
    devices = scan_arp(args.target, args.timeout)
    
    if devices is not None:
        print("-" * 40)
        print(f"{'IP Address':<20} {'MAC Address':<20}")
        print("-" * 40)
        for device in devices:
            print(f"{Fore.GREEN}{device['ip']:<20}{Style.RESET_ALL} {device['mac']:<20}")
        print("-" * 40)
        print_status(f"Scan complete. Found {len(devices)} active device(s).", "cyan")

if __name__ == "__main__":
    main()
