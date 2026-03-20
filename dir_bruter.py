import requests
import argparse
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style, init
import sys
import os
from utils import get_random_user_agent, print_status, load_wordlist

init(autoreset=True)

def check_path(base_url: str, path: str, user_agent: str) -> str:
    """
    Check if a given path exists on the target URL with a randomized User-Agent.
    """
    url = f"{base_url}/{path}"
    headers = {"User-Agent": user_agent}
    
    try:
        response = requests.get(url, headers=headers, timeout=5, allow_redirects=False)
        if response.status_code == 200:
            return f"{Fore.GREEN}[200 OK] {url}{Style.RESET_ALL}"
        elif response.status_code == 403:
            return f"{Fore.YELLOW}[403 Forbidden] {url}{Style.RESET_ALL}"
        elif response.status_code == 401:
            return f"{Fore.YELLOW}[401 Unauthorized] {url}{Style.RESET_ALL}"
        elif response.status_code in [301, 302]:
            location = response.headers.get('Location', 'Unknown')
            return f"{Fore.CYAN}[{response.status_code} Redirect] {url} -> {location}{Style.RESET_ALL}"
        else:
            return None
    except requests.exceptions.RequestException:
        return None

def main():
    parser = argparse.ArgumentParser(description="A multi-threaded directory brute-forcer with User-Agent randomization.")
    parser.add_argument("url", help="Base URL to brute-force (e.g., https://example.com)")
    parser.add_argument("-w", "--wordlist", default="wordlists/common_dirs.txt", help="Path to directory wordlist (default: wordlists/common_dirs.txt)")
    parser.add_argument("-t", "--threads", type=int, default=20, help="Number of threads (default: 20)")
    parser.add_argument("-r", "--random-agent", action="store_true", help="Use a random User-Agent for each request")
    
    args = parser.parse_args()

    if not args.url.startswith(("http://", "https://")):
        print_status("URL must start with http:// or https://", "error")
        sys.exit(1)

    # Remove trailing slash from base URL
    base_url = args.url.rstrip("/")

    paths = load_wordlist(args.wordlist)
    if not paths:
        sys.exit(1)

    print_status(f"Starting directory brute-force for: {base_url}", "cyan")
    print_status(f"Using {len(paths)} paths and {args.threads} threads.", "cyan")
    if args.random_agent:
        print_status("User-Agent randomization enabled.", "cyan")
    print("-" * 60)

    found_count = 0
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = []
        for path in paths:
            user_agent = get_random_user_agent() if args.random_agent else "Security-Toolkit/1.0"
            futures.append(executor.submit(check_path, base_url, path, user_agent))
        
        for future in futures:
            result = future.result()
            if result:
                print(result)
                found_count += 1

    print("-" * 60)
    print_status(f"Finished. Total directories found: {found_count}", "cyan")

if __name__ == "__main__":
    main()
