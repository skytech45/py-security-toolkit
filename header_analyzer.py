import requests
import argparse
import sys
from typing import Dict, List

def analyze_headers(url: str) -> Dict[str, str]:
    """
    Fetch and analyze HTTP security headers for a given URL.
    """
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    try:
        response = requests.get(url, timeout=10)
        headers = response.headers
        
        security_headers = {
            "Strict-Transport-Security": "Ensures encrypted connection (HTTPS).",
            "Content-Security-Policy": "Prevents XSS and other injection attacks.",
            "X-Frame-Options": "Prevents Clickjacking.",
            "X-Content-Type-Options": "Prevents MIME sniffing.",
            "Referrer-Policy": "Controls how much referrer information is shared.",
            "Permissions-Policy": "Controls which browser features can be used."
        }

        results = []
        print(f"\n[*] Analyzing headers for: {url}")
        print("-" * 60)
        
        found_count = 0
        for header, description in security_headers.items():
            if header in headers:
                print(f"[+] {header}: Present")
                found_count += 1
            else:
                print(f"[-] {header}: MISSING")
                print(f"    Info: {description}")
        
        print("-" * 60)
        print(f"[*] Summary: {found_count}/{len(security_headers)} security headers found.")
        
    except requests.exceptions.RequestException as e:
        print(f"[!] Error: Could not connect to {url}. {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze HTTP security headers of a website.")
    parser.add_argument("url", help="The URL to analyze (e.g., example.com)")
    
    args = parser.parse_args()
    analyze_headers(args.url)
