"""
whois_lookup.py — WHOIS domain information lookup tool.

Usage:
    python whois_lookup.py example.com
    python whois_lookup.py example.com -o result.json
    python whois_lookup.py --interactive
"""

import argparse
import json
import socket
import sys
from datetime import datetime
from typing import Optional, Dict, Any

try:
    import whois  # type: ignore
    from colorama import Fore, Style, init  # type: ignore
    init(autoreset=True)
except ImportError:
    print("Missing dependencies. Run: pip install python-whois colorama")
    sys.exit(1)


def lookup_domain(domain: str) -> Dict[str, Any]:
    """Perform a WHOIS lookup for the given domain.

    Args:
        domain: Domain name to look up (e.g. 'example.com').

    Returns:
        Dictionary containing WHOIS information.

    Raises:
        Exception: If the lookup fails or the domain is invalid.
    """
    w = whois.whois(domain)
    info: Dict[str, Any] = {
        "domain_name": _normalize(w.domain_name),
        "registrar": w.registrar,
        "creation_date": _normalize_date(w.creation_date),
        "expiration_date": _normalize_date(w.expiration_date),
        "updated_date": _normalize_date(w.updated_date),
        "name_servers": _normalize(w.name_servers),
        "status": _normalize(w.status),
        "emails": _normalize(w.emails),
        "dnssec": w.dnssec,
        "country": w.country,
        "org": w.org,
    }
    return info


def _normalize(value: Any) -> Any:
    """Normalize list/string values for consistent output."""
    if isinstance(value, list):
        seen = []
        for v in value:
            v_lower = str(v).lower() if isinstance(v, str) else v
            if v_lower not in [str(s).lower() for s in seen]:
                seen.append(v)
        return seen if len(seen) > 1 else (seen[0] if seen else None)
    return value


def _normalize_date(value: Any) -> Optional[str]:
    """Convert datetime or list of datetimes to ISO string."""
    if isinstance(value, list):
        value = value[0]
    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%d %H:%M:%S")
    return str(value) if value else None


def print_whois(domain: str, info: Dict[str, Any]) -> None:
    """Pretty-print WHOIS information to the terminal."""
    print(f"\n{Fore.CYAN}{'=' * 55}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}  WHOIS Lookup: {Fore.WHITE}{domain}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'=' * 55}{Style.RESET_ALL}\n")

    fields = [
        ("Domain Name",    info.get("domain_name")),
        ("Registrar",      info.get("registrar")),
        ("Created",        info.get("creation_date")),
        ("Expires",        info.get("expiration_date")),
        ("Updated",        info.get("updated_date")),
        ("Organisation",   info.get("org")),
        ("Country",        info.get("country")),
        ("DNSSEC",         info.get("dnssec")),
        ("Emails",         info.get("emails")),
        ("Name Servers",   info.get("name_servers")),
        ("Status",         info.get("status")),
    ]

    for label, value in fields:
        if value is None:
            continue
        if isinstance(value, list):
            print(f"  {Fore.GREEN}{label:<18}{Style.RESET_ALL}")
            for v in value:
                print(f"    {Fore.WHITE}• {v}{Style.RESET_ALL}")
        else:
            print(f"  {Fore.GREEN}{label:<18}{Style.RESET_ALL}{Fore.WHITE}{value}{Style.RESET_ALL}")

    print(f"\n{Fore.CYAN}{'=' * 55}{Style.RESET_ALL}\n")


def resolve_ip(domain: str) -> Optional[str]:
    """Resolve a domain to its IP address."""
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        return None


def main() -> None:
    parser = argparse.ArgumentParser(
        description="WHOIS domain information lookup tool.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="Examples:\n"
               "  python whois_lookup.py example.com\n"
               "  python whois_lookup.py google.com -o result.json\n"
               "  python whois_lookup.py --interactive",
    )
    parser.add_argument("domain", nargs="?", help="Domain name to look up")
    parser.add_argument("-o", "--output", type=str, help="Save results to a JSON file")
    parser.add_argument("--interactive", action="store_true", help="Enter interactive mode")
    parser.add_argument("--ip", action="store_true", help="Also resolve and display the domain's IP address")

    args = parser.parse_args()

    if args.interactive:
        print(f"{Fore.CYAN}[*] WHOIS Lookup — Interactive Mode (Ctrl+C to exit){Style.RESET_ALL}")
        while True:
            try:
                domain = input(f"{Fore.YELLOW}Enter domain: {Style.RESET_ALL}").strip()
                if not domain:
                    continue
                _run_lookup(domain, None, args.ip)
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}[!] Exiting.{Style.RESET_ALL}")
                break
    elif args.domain:
        _run_lookup(args.domain, args.output, args.ip)
    else:
        parser.print_help()


def _run_lookup(domain: str, output: Optional[str], show_ip: bool) -> None:
    """Execute the lookup and handle output."""
    try:
        print(f"{Fore.CYAN}[*] Looking up {domain}...{Style.RESET_ALL}")
        info = lookup_domain(domain)

        if show_ip:
            ip = resolve_ip(domain)
            info["ip_address"] = ip
            print(f"  {Fore.GREEN}{'IP Address':<18}{Style.RESET_ALL}{Fore.WHITE}{ip or 'Could not resolve'}{Style.RESET_ALL}")

        print_whois(domain, info)

        if output:
            with open(output, "w") as f:
                json.dump({"domain": domain, "whois": info}, f, indent=2, default=str)
            print(f"{Fore.CYAN}[*] Results saved to {output}{Style.RESET_ALL}")

    except Exception as e:
        print(f"{Fore.RED}[!] WHOIS lookup failed: {e}{Style.RESET_ALL}")


if __name__ == "__main__":
    main()
