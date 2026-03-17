import socket
import argparse
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional

# ─────────────────────────────────────────────────────────────────
# py-security-toolkit | subdomain_finder.py
# Author : skytech45
# Desc   : Multi-threaded subdomain enumeration tool.
#          Resolves DNS and reports live subdomains.
# ─────────────────────────────────────────────────────────────────

DEFAULT_WORDLIST = [
    "www", "mail", "ftp", "smtp", "pop", "imap", "webmail",
    "admin", "portal", "api", "dev", "staging", "test", "beta",
    "app", "dashboard", "cdn", "static", "media", "assets",
    "blog", "shop", "store", "secure", "vpn", "remote",
    "support", "help", "forum", "wiki", "docs", "status",
    "ns1", "ns2", "mx", "auth", "login", "account", "mobile",
    "m", "wap", "download", "upload", "git", "gitlab", "jenkins",
]


def resolve_subdomain(domain: str, sub: str, timeout: float = 2.0) -> Optional[tuple]:
    """
    Attempt DNS resolution for a subdomain.

    Args:
        domain:  Base domain (e.g., example.com)
        sub:     Subdomain prefix (e.g., www)
        timeout: DNS timeout in seconds

    Returns:
        (full_domain, ip) if resolved, else None
    """
    full = f"{sub}.{domain}"
    socket.setdefaulttimeout(timeout)
    try:
        ip = socket.gethostbyname(full)
        return (full, ip)
    except (socket.gaierror, socket.timeout):
        return None


def load_wordlist(path: str) -> list:
    """Load subdomains from a custom wordlist file."""
    try:
        with open(path, "r") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"[!] Wordlist file not found: {path}")
        sys.exit(1)


def run_scan(domain: str, wordlist: list, threads: int = 50, timeout: float = 2.0) -> list:
    """
    Run multi-threaded subdomain scan.

    Args:
        domain:   Target domain
        wordlist: List of subdomain prefixes
        threads:  Max concurrent threads
        timeout:  DNS timeout per request

    Returns:
        List of (subdomain, ip) tuples for resolved hosts
    """
    found = []
    total = len(wordlist)
    print(f"\n[*] Scanning {domain} | {total} subdomains | {threads} threads")
    print("-" * 55)

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {
            executor.submit(resolve_subdomain, domain, sub, timeout): sub
            for sub in wordlist
        }
        for i, future in enumerate(as_completed(futures), 1):
            result = future.result()
            if result:
                full, ip = result
                print(f"  [+] FOUND  {full:<40} -> {ip}")
                found.append(result)

    return found


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Multi-threaded subdomain enumeration tool.",
        epilog="Example: python subdomain_finder.py -d example.com -t 100"
    )
    parser.add_argument("-d", "--domain", required=True,
                        help="Target domain (e.g., example.com)")
    parser.add_argument("-w", "--wordlist", default=None,
                        help="Path to custom wordlist file (one subdomain per line)")
    parser.add_argument("-t", "--threads", type=int, default=50,
                        help="Number of concurrent threads (default: 50)")
    parser.add_argument("--timeout", type=float, default=2.0,
                        help="DNS resolution timeout in seconds (default: 2.0)")
    parser.add_argument("-o", "--output", default=None,
                        help="Save results to output file")
    args = parser.parse_args()

    wordlist = load_wordlist(args.wordlist) if args.wordlist else DEFAULT_WORDLIST

    found = run_scan(args.domain, wordlist, args.threads, args.timeout)

    print("-" * 55)
    print(f"\n[*] Scan complete. Found {len(found)} subdomains.\n")

    if found:
        print("[+] Results:")
        for full, ip in sorted(found):
            print(f"    {full} -> {ip}")

    if args.output and found:
        with open(args.output, "w") as f:
            for full, ip in found:
                f.write(f"{full},{ip}\n")
        print(f"\n[*] Results saved to: {args.output}")


if __name__ == "__main__":
    main()
