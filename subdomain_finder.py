import socket
import argparse
import sys
from concurrent.futures import ThreadPoolExecutor

def check_subdomain(domain: str, subdomain: str) -> str:
    """
    Check if a subdomain resolves to an IP address.
    """
    full_domain = f"{subdomain}.{domain}"
    try:
        ip = socket.gethostbyname(full_domain)
        return f"[+] Found: {full_domain} -> {ip}"
    except socket.gaierror:
        return None

def main():
    parser = argparse.ArgumentParser(description="A basic multi-threaded subdomain finder.")
    parser.add_argument("domain", help="Target domain (e.g., google.com)")
    parser.add_argument("-w", "--wordlist", help="Path to subdomain wordlist (default: common_subdomains.txt)")
    parser.add_argument("-t", "--threads", type=int, default=10, help="Number of threads (default: 10)")
    
    args = parser.parse_args()

    # Default common subdomains if no wordlist provided
    common_subdomains = ["www", "mail", "ftp", "localhost", "webmail", "smtp", "pop", "ns1", "ns2", "admin", "blog", "dev", "staging", "api", "vpn"]
    
    subdomains = []
    if args.wordlist:
        try:
            with open(args.wordlist, "r") as f:
                subdomains = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"[!] Error: Wordlist '{args.wordlist}' not found. Using default list.")
            subdomains = common_subdomains
    else:
        subdomains = common_subdomains

    print(f"[*] Starting subdomain search for: {args.domain}")
    print(f"[*] Using {args.threads} threads and {len(subdomains)} subdomains.")
    print("-" * 50)

    found_count = 0
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = [executor.submit(check_subdomain, args.domain, sub) for sub in subdomains]
        for future in futures:
            result = future.result()
            if result:
                print(result)
                found_count += 1

    print("-" * 50)
    print(f"[*] Finished. Total subdomains found: {found_count}")

if __name__ == "__main__":
    main()
