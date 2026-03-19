import socket
import argparse
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style, init

init(autoreset=True)

def scan_port(ip, port):
    """Attempt to connect to a specific port on the target IP."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex((ip, port))
            if result == 0:
                return port, True
    except Exception:
        pass
    return port, False

def run_scanner(target, start_port, end_port, threads=100):
    """Scan a range of ports on the target IP using multiple threads."""
    print(f"{Fore.CYAN}[*] Scanning target: {target}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}[*] Time started: {datetime.now()}{Style.RESET_ALL}")
    print("-" * 50)

    open_ports = []
    
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(scan_port, target, port) for port in range(start_port, end_port + 1)]
        for future in futures:
            port, is_open = future.result()
            if is_open:
                            print(f"{Fore.GREEN}[+] Port {port} is OPEN{Style.RESET_ALL}")
                open_ports.append(port)

    print("-" * 50)
    print(f"{Fore.CYAN}[*] Scanning finished at: {datetime.now()}{Style.RESET_ALL}")
    if open_ports:
        print(f"[*] Total open ports found: {len(open_ports)}")
    else:
        print(f"{Fore.YELLOW}[!] No open ports found in the specified range.{Style.RESET_ALL}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A simple multi-threaded port scanner.")
    parser.add_argument("target", help="Target IP address or hostname to scan.")
    parser.add_argument("-s", "--start", type=int, default=1, help="Start port (default: 1)")
    parser.add_argument("-e", "--end", type=int, default=1024, help="End port (default: 1024)")
    parser.add_argument("-t", "--threads", type=int, default=100, help="Number of threads (default: 100)")

    args = parser.parse_args()

    try:
        # Resolve target hostname to IP
        target_ip = socket.gethostbyname(args.target)
        run_scanner(target_ip, args.start, args.end, args.threads)
    except socket.gaierror:
        print(f"{Fore.RED}[!] Error: Could not resolve hostname.{Style.RESET_ALL}")
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] Scanning interrupted by user.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[!] An unexpected error occurred: {e}{Style.RESET_ALL}")
