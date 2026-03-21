import socket
import argparse
import json
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from typing import List, Tuple, Optional
from colorama import Fore, Style, init

init(autoreset=True)


def scan_port(ip: str, port: int) -> Tuple[int, bool]:
    """Attempt to connect to a specific port on the target IP.

    Args:
        ip: Target IP address or hostname.
        port: Port number to scan.

    Returns:
        Tuple of (port, is_open).
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex((ip, port))
            if result == 0:
                return port, True
    except Exception:
        pass
    return port, False


def run_scanner(
    target: str,
    start_port: int,
    end_port: int,
    threads: int = 100,
    output_json: Optional[str] = None,
) -> List[int]:
    """Scan a range of ports on the target IP using multiple threads.

    Args:
        target: Target hostname or IP address.
        start_port: First port in the scan range.
        end_port: Last port in the scan range (inclusive).
        threads: Number of concurrent threads to use.
        output_json: Optional path to write JSON results.

    Returns:
        List of open port numbers.
    """
    print(f"{Fore.CYAN}[*] Scanning target: {target}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}[*] Time started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}")
    print("-" * 50)

    open_ports: List[int] = []

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [
            executor.submit(scan_port, target, port)
            for port in range(start_port, end_port + 1)
        ]
        for future in futures:
            port, is_open = future.result()
            if is_open:
                print(f"{Fore.GREEN}[+] Port {port} is OPEN{Style.RESET_ALL}")
                open_ports.append(port)

    open_ports.sort()
    print("-" * 50)
    print(f"{Fore.CYAN}[*] Scanning finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}")

    if open_ports:
        print(f"[*] Total open ports found: {len(open_ports)}")
    else:
        print(f"{Fore.YELLOW}[!] No open ports found in the specified range.{Style.RESET_ALL}")

    if output_json:
        report = {
            "target": target,
            "scan_range": f"{start_port}-{end_port}",
            "open_ports": open_ports,
            "total_open": len(open_ports),
            "timestamp": datetime.now().isoformat(),
        }
        with open(output_json, "w") as f:
            json.dump(report, f, indent=2)
        print(f"{Fore.CYAN}[*] Results saved to {output_json}{Style.RESET_ALL}")

    return open_ports


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A fast, multi-threaded TCP port scanner.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("target", help="Target IP address or hostname to scan.")
    parser.add_argument("-s", "--start", type=int, default=1, help="Start port (default: 1)")
    parser.add_argument("-e", "--end", type=int, default=1024, help="End port (default: 1024)")
    parser.add_argument("-t", "--threads", type=int, default=100, help="Number of threads (default: 100)")
    parser.add_argument("-o", "--output", type=str, default=None, help="Save results to JSON file")

    args = parser.parse_args()

    try:
        target_ip = socket.gethostbyname(args.target)
        run_scanner(target_ip, args.start, args.end, args.threads, args.output)
    except socket.gaierror:
        print(f"{Fore.RED}[!] Error: Could not resolve hostname.{Style.RESET_ALL}")
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] Scanning interrupted by user.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[!] An unexpected error occurred: {e}{Style.RESET_ALL}")
