import ssl
import socket
import argparse
from datetime import datetime
from typing import Dict, Any

def check_ssl_expiry(hostname: str, port: int = 443) -> Dict[str, Any]:
    """
    Fetch and analyze the SSL/TLS certificate for a given hostname.
    """
    context = ssl.create_default_context()
    
    try:
        with socket.create_connection((hostname, port), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                
                # Parse expiration date
                not_after_str = cert.get('notAfter')
                expiry_date = datetime.strptime(not_after_str, '%b %d %H:%M:%S %Y %Z')
                days_to_expiry = (expiry_date - datetime.utcnow()).days
                
                issuer = dict(x[0] for x in cert.get('issuer'))
                subject = dict(x[0] for x in cert.get('subject'))
                
                return {
                    "status": "success",
                    "hostname": hostname,
                    "issuer": issuer.get('organizationName', 'Unknown'),
                    "subject": subject.get('commonName', 'Unknown'),
                    "expiry_date": expiry_date.strftime('%Y-%m-%d %H:%M:%S'),
                    "days_remaining": days_to_expiry,
                    "version": ssock.version(),
                    "cipher": ssock.cipher()[0]
                }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

def main():
    parser = argparse.ArgumentParser(description="Analyze SSL/TLS certificate of a website.")
    parser.add_argument("hostname", help="The hostname to check (e.g., google.com)")
    parser.add_argument("-p", "--port", type=int, default=443, help="The port to check (default: 443)")
    
    args = parser.parse_args()
    
    print(f"\n[*] Analyzing SSL/TLS Certificate for: {args.hostname}:{args.port}")
    print("-" * 60)
    
    result = check_ssl_expiry(args.hostname, args.port)
    
    if result['status'] == 'success':
        print(f"[+] Subject: {result['subject']}")
        print(f"[+] Issuer: {result['issuer']}")
        print(f"[+] Expiry Date: {result['expiry_date']}")
        print(f"[+] Days Remaining: {result['days_remaining']}")
        print(f"[+] TLS Version: {result['version']}")
        print(f"[+] Cipher: {result['cipher']}")
        
        if result['days_remaining'] < 30:
            print("[!] WARNING: Certificate expires soon!")
    else:
        print(f"[!] Error: {result['message']}")
    
    print("-" * 60)

if __name__ == "__main__":
    main()
