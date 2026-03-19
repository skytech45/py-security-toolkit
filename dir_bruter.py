import requests
import argparse
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style, init
import sys

init(autoreset=True)

def check_path(base_url: str, path: str) -> str:
    """
    Check if a given path exists on the target URL.
    """
    url = f"{base_url}/{path}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return f"{Fore.GREEN}[+] Found: {url} (Status: {response.status_code}){Style.RESET_ALL}"
        elif response.status_code == 403:
            return f"{Fore.YELLOW}[!] Forbidden: {url} (Status: {response.status_code}){Style.RESET_ALL}"
        elif response.status_code == 401:
            return f"{Fore.YELLOW}[!] Unauthorized: {url} (Status: {response.status_code}){Style.RESET_ALL}"
        else:
            return None # Not found or other status
    except requests.exceptions.RequestException:
        return None

def main():
    parser = argparse.ArgumentParser(description="A multi-threaded directory brute-forcer.")
    parser.add_argument("url", help="Base URL to brute-force (e.g., https://example.com)")
    parser.add_argument("-w", "--wordlist", default="wordlists/common_dirs.txt", help="Path to directory wordlist (default: wordlists/common_dirs.txt)")
    parser.add_argument("-t", "--threads", type=int, default=20, help="Number of threads (default: 20)")
    
    args = parser.parse_args()

    if not args.url.startswith(("http://", "https://")):
        print(f"{Fore.RED}[!] Error: URL must start with http:// or https://{Style.RESET_ALL}")
        sys.exit(1)

    try:
        with open(args.wordlist, "r") as f:
            paths = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"{Fore.RED}[!] Error: Wordlist \'{args.wordlist}\' not found.{Style.RESET_ALL}")
        sys.exit(1)

    print(f"{Fore.CYAN}[*] Starting directory brute-force for: {args.url}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}[*] Using {len(paths)} paths and {args.threads} threads.{Style.RESET_ALL}")
    print("-" * 60)

    found_count = 0
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = [executor.submit(check_path, args.url, path) for path in paths]
        for future in futures:
            result = future.result()
            if result:
                print(result)
                found_count += 1

    print("-" * 60)
    print(f"{Fore.CYAN}[*] Finished. Total directories found: {found_count}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
