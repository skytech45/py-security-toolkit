import socket
import argparse
import sys
from concurrent.futures import ThreadPoolExecutor
from typing import Optional, List
from colorama import init
from utils import print_status, load_wordlist

init(autoreset=True)

# ─────────────────────────────────────────────────────────────────
# py-security-toolkit | subdomain_finder.py
# Author : skytech45
# Desc   : Enumerate subdomains using multi-threaded DNS resolution.
# ─────────────────────────────────────────────────────────────────

def check_subdomain(domain: str, subdomain: str) -> Optional[str]:
    """
    Check if a subdomain resolves to an IP address.
    """
    full_domain = f"{subdomain}.{domain}"
    try:
        ip = socket.gethostbyname(full_domain)
        return f"{full_domain} -> {ip}"
    except socket.gaierror:
        return None
    except Exception:
        return None

def main():
    parser = argparse.ArgumentParser(
        description="Enumerate subdomains using multi-threaded DNS resolution.",
        epilog="Example: python subdomain_finder.py -d example.com -w wordlists/common_subdomains.txt -t 50"
    )
    parser.add_argument("-d", "--domain", required=True, help="Target domain (e.g., google.com)")
    parser.add_argument("-w", "--wordlist", help="Path to subdomain wordlist (default: wordlists/common_subdomains.txt)")
    parser.add_argument("-t", "--threads", type=int, default=20, help="Number of threads (default: 20)")
    parser.add_argument("-o", "--output", help="Save results to a text file")
    
    args = parser.parse_args()

    # Default wordlist path
    wordlist_path = args.wordlist if args.wordlist else "wordlists/common_subdomains.txt"
    
    subdomains = load_wordlist(wordlist_path)
    
    # Fallback if wordlist is empty or not found
    if not subdomains:
        print_status("Using a small default list as fallback.", "warning")
        subdomains = ["www", "mail", "ftp", "localhost", "webmail", "smtp", "pop", "ns1", "ns2", "admin", "blog", "dev", "staging", "api", "vpn"]

    print_status(f"Starting subdomain search for: {args.domain}", "cyan")
    print_status(f"Using {args.threads} threads and {len(subdomains)} subdomains.", "cyan")
    print("-" * 60)

    found_results = []
    found_count = 0
    
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = [executor.submit(check_subdomain, args.domain, sub) for sub in subdomains]
        for future in futures:
            result = future.result()
            if result:
                print_status(result, "success")
                found_results.append(result)
                found_count += 1

    print("-" * 60)
    print_status(f"Finished. Total subdomains found: {found_count}", "cyan")

    if args.output and found_results:
        try:
            with open(args.output, "w") as f:
                for res in found_results:
                    f.write(res + "\n")
            print_status(f"Results saved to: {args.output}", "success")
        except Exception as e:
            print_status(f"Failed to save results: {e}", "error")

if __name__ == "__main__":
    main()
