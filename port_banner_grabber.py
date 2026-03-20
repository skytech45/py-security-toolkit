import socket
import argparse
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional, Tuple
from datetime import datetime
from colorama import Fore, Style, init
from utils import print_status

# Initialize colorama
init(autoreset=True)

# ─────────────────────────────────────────────────────────────────
# py-security-toolkit | port_banner_grabber.py
# Author : skytech45
# Desc   : Scan open ports and grab service banners for
#          reconnaissance and network analysis.
# ─────────────────────────────────────────────────────────────────

WELL_KNOWN_PORTS = {
    21:  "FTP",
    22:  "SSH",
    23:  "Telnet",
    25:  "SMTP",
    53:  "DNS",
    80:  "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    445: "SMB",
    3306:"MySQL",
    3389:"RDP",
    5432:"PostgreSQL",
    6379:"Redis",
    8080:"HTTP-Alt",
    8443:"HTTPS-Alt",
    27017:"MongoDB",
}


def grab_banner(host: str, port: int, timeout: float = 3.0) -> Optional[str]:
    """
    Attempt to grab a service banner from an open port.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((host, port))
            # Send generic HTTP request for web ports
            if port in (80, 8080):
                s.send(b"HEAD / HTTP/1.0\r\nHost: " + host.encode() + b"\r\n\r\n")
            elif port == 21:
                pass  # FTP sends banner automatically
            else:
                s.send(b"\r\n")
            banner = s.recv(1024).decode("utf-8", errors="ignore").strip()
            return banner[:200] if banner else None
    except Exception:
        return None


def scan_port(host: str, port: int, timeout: float) -> Tuple[int, bool, Optional[str]]:
    """
    Check if a port is open and grab its banner.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((host, port))
            if result == 0:
                banner = grab_banner(host, port, timeout)
                return (port, True, banner)
    except Exception:
        pass
    return (port, False, None)


def resolve_host(host: str) -> str:
    """Resolve hostname to IP address."""
    try:
        return socket.gethostbyname(host)
    except socket.gaierror:
        print_status(f"Cannot resolve host: {host}", "error")
        sys.exit(1)


def run_scan(host: str, ports: list, threads: int = 100, timeout: float = 3.0) -> list:
    """
    Multi-threaded port scan with banner grabbing.
    """
    ip = resolve_host(host)
    open_ports = []

    print(f"\n{Fore.CYAN}{'='*55}{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}PORT BANNER GRABBER — py-security-toolkit{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*55}{Style.RESET_ALL}")
    print(f"  Target    : {host} ({ip})")
    print(f"  Ports     : {len(ports)} | Threads: {threads} | Timeout: {timeout}s")
    print(f"  Started   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'-'*55}")

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {executor.submit(scan_port, ip, p, timeout): p for p in ports}
        for future in as_completed(futures):
            port, is_open, banner = future.result()
            if is_open:
                service = WELL_KNOWN_PORTS.get(port, "Unknown")
                print(f"  {Fore.GREEN}[OPEN]{Style.RESET_ALL} Port {port:<6} | {service:<12}", end="")
                if banner:
                    clean = banner.split("\n")[0][:60]
                    print(f" | {clean}")
                else:
                    print()
                open_ports.append((port, service, banner or ""))

    open_ports.sort(key=lambda x: x[0])
    return open_ports


def parse_ports(port_arg: str) -> list:
    """
    Parse port argument into a list.
    """
    ports = []
    for part in port_arg.split(","):
        part = part.strip()
        if not part: continue
        if "-" in part:
            start, end = part.split("-")
            ports.extend(range(int(start), int(end) + 1))
        else:
            ports.append(int(part))
    return list(set(ports))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scan open ports and grab service banners.",
        epilog="""
Examples:
  python port_banner_grabber.py -t example.com
  python port_banner_grabber.py -t 192.168.1.1 -p 1-1000
  python port_banner_grabber.py -t example.com -p 22,80,443,8080
        """
    )
    parser.add_argument("-t", "--target", required=True, help="Target host or IP")
    parser.add_argument("-p", "--ports", default="1-1024",
                        help="Ports to scan: single, range, or csv (default: 1-1024)")
    parser.add_argument("--threads", type=int, default=100,
                        help="Concurrent threads (default: 100)")
    parser.add_argument("--timeout", type=float, default=3.0,
                        help="Socket timeout in seconds (default: 3.0)")
    parser.add_argument("-o", "--output", default=None,
                        help="Save results to file")
    args = parser.parse_args()

    ports = parse_ports(args.ports)
    results = run_scan(args.target, ports, args.threads, args.timeout)

    print(f"{Fore.CYAN}{'='*55}{Style.RESET_ALL}")
    print_status(f"Scan complete. {len(results)} open port(s) found.", "cyan")
    print(f"{Fore.CYAN}{'='*55}{Style.RESET_ALL}\n")

    if args.output and results:
        with open(args.output, "w") as f:
            f.write("port,service,banner\n")
            for port, service, banner in results:
                f.write(f"{port},{service},{banner.replace(chr(10), ' ')}\n")
        print_status(f"Results saved to: {args.output}", "success")


if __name__ == "__main__":
    main()
