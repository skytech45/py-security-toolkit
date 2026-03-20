import random
import os
from typing import List, Optional
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def get_random_user_agent(wordlist_path: str = "wordlists/common_agents.txt") -> str:
    """
    Returns a random user agent from the specified wordlist.
    Defaults to a common browser agent if the wordlist is missing.
    """
    default_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    
    if not os.path.exists(wordlist_path):
        return default_agent
    
    try:
        with open(wordlist_path, "r") as f:
            agents = [line.strip() for line in f if line.strip()]
        return random.choice(agents) if agents else default_agent
    except Exception:
        return default_agent

def print_status(message: str, status: str = "info"):
    """
    Prints a color-coded status message.
    """
    if status == "success":
        print(f"{Fore.GREEN}[+] {message}{Style.RESET_ALL}")
    elif status == "error":
        print(f"{Fore.RED}[!] {message}{Style.RESET_ALL}")
    elif status == "warning":
        print(f"{Fore.YELLOW}[!] {message}{Style.RESET_ALL}")
    elif status == "cyan":
        print(f"{Fore.CYAN}[*] {message}{Style.RESET_ALL}")
    else:
        print(f"[*] {message}")

def load_wordlist(path: str) -> List[str]:
    """
    Loads a wordlist from the specified path.
    """
    if not os.path.exists(path):
        print_status(f"Wordlist '{path}' not found.", "error")
        return []
    
    try:
        with open(path, "r") as f:
            return [line.strip() for line in f if line.strip()]
    except Exception as e:
        print_status(f"Error loading wordlist: {e}", "error")
        return []
