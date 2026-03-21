import subprocess
import argparse
import re
import sys
from colorama import Fore, Style, init
from utils import print_status

init(autoreset=True)

# ─────────────────────────────────────────────────────────────────
# py-security-toolkit | mac_changer.py
# Author : skytech45
# Desc   : Change the MAC address of a network interface.
# ─────────────────────────────────────────────────────────────────

def get_current_mac(interface: str) -> str:
    """
    Retrieve the current MAC address of the specified interface.
    """
    try:
        ifconfig_result = subprocess.check_output(["ifconfig", interface]).decode("utf-8")
        mac_address_search_result = re.search(r"(\w\w:\w\w:\w\w:\w\w:\w\w:\w\w)", ifconfig_result)
        
        if mac_address_search_result:
            return mac_address_search_result.group(0)
        else:
            print_status(f"Could not read MAC address for {interface}.", "error")
            return None
    except subprocess.CalledProcessError:
        print_status(f"Interface {interface} not found.", "error")
        return None

def change_mac(interface: str, new_mac: str):
    """
    Change the MAC address of the specified interface.
    """
    print_status(f"Changing MAC address for {interface} to {new_mac}", "cyan")
    
    try:
        # Step 1: Disable the interface
        subprocess.check_call(["ifconfig", interface, "down"])
        
        # Step 2: Change the MAC address
        subprocess.check_call(["ifconfig", interface, "hw", "ether", new_mac])
        
        # Step 3: Re-enable the interface
        subprocess.check_call(["ifconfig", interface, "up"])
        
        return True
    except subprocess.CalledProcessError:
        print_status("Failed to change MAC address. Make sure you have root/sudo privileges.", "error")
        return False

def main():
    parser = argparse.ArgumentParser(description="Change the MAC address of a network interface.")
    parser.add_argument("-i", "--interface", required=True, help="Network interface (e.g., eth0, wlan0)")
    parser.add_argument("-m", "--mac", required=True, help="New MAC address (e.g., 00:11:22:33:44:55)")
    
    args = parser.parse_args()
    
    # Validate MAC address format
    if not re.match(r"(\w\w:\w\w:\w\w:\w\w:\w\w:\w\w)", args.mac):
        print_status("Invalid MAC address format. Use XX:XX:XX:XX:XX:XX", "error")
        sys.exit(1)
    
    current_mac = get_current_mac(args.interface)
    if current_mac:
        print_status(f"Current MAC: {current_mac}", "cyan")
        
        if change_mac(args.interface, args.mac):
            new_mac = get_current_mac(args.interface)
            if new_mac == args.mac:
                print_status(f"MAC address successfully changed to {new_mac}", "success")
            else:
                print_status("MAC address change failed.", "error")

if __name__ == "__main__":
    main()
