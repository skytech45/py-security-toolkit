import re
import math
import argparse
import sys
from typing import List

# ─────────────────────────────────────────────────────────────────
# py-security-toolkit | password_checker.py
# Author : skytech45
# Desc   : Analyze password strength with entropy scoring,
#          pattern detection, and actionable feedback.
# ─────────────────────────────────────────────────────────────────

COMMON_PATTERNS = [
    r"(012|123|234|345|456|567|678|789|890)",
    r"(abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop)",
    r"(qwerty|asdf|zxcv|password|letmein|welcome|admin|login|iloveyou)",
    r"(\w)\1{2,}",
]

COMMON_PASSWORDS = {
    "password", "123456", "123456789", "qwerty", "abc123",
    "password1", "iloveyou", "admin", "welcome", "monkey",
    "dragon", "master", "sunshine", "princess", "letmein"
}


def calculate_entropy(password: str) -> float:
    """Calculate Shannon entropy (bits) based on character set size."""
    if not password:
        return 0.0
    charset = 0
    if re.search(r"[a-z]", password): charset += 26
    if re.search(r"[A-Z]", password): charset += 26
    if re.search(r"[0-9]", password): charset += 10
    if re.search(r"[^a-zA-Z0-9]", password): charset += 32
    return round(len(password) * math.log2(charset), 2) if charset else 0.0


def detect_patterns(password: str) -> List[str]:
    """Detect common weak patterns in the password."""
    warnings = []
    pw_lower = password.lower()
    for pattern in COMMON_PATTERNS:
        if re.search(pattern, pw_lower):
            warnings.append("Contains weak/sequential pattern.")
            break
    if pw_lower in COMMON_PASSWORDS:
        warnings.append("This is a commonly known password — avoid it!")
    return warnings


def check_password_strength(password: str) -> dict:
    """
    Score a password on length, complexity, entropy, and patterns.

    Args:
        password: The plaintext password string to analyze.

    Returns:
        dict with keys: score, max_score, strength, entropy_bits, feedback
    """
    score = 0
    feedback: List[str] = []

    # Length
    length = len(password)
    if length < 8:
        feedback.append("Too short — use at least 8 characters.")
    elif length < 12:
        score += 1
        feedback.append("Acceptable length — 12+ is recommended.")
    elif length < 16:
        score += 2
        feedback.append("Good length (12-15 chars).")
    else:
        score += 3
        feedback.append("Excellent length (16+ chars).")

    # Complexity
    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("Add lowercase letters.")

    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("Add uppercase letters.")

    if re.search(r"[0-9]", password):
        score += 1
    else:
        feedback.append("Add numbers.")

    if re.search(r"[^a-zA-Z0-9]", password):
        score += 2
        feedback.append("Special characters detected — good!")
    else:
        feedback.append("Add special characters (!@#$%^&*).")

    # Pattern penalties
    pattern_warnings = detect_patterns(password)
    if pattern_warnings:
        score = max(0, score - 2)
        feedback.extend(pattern_warnings)

    # Entropy
    entropy = calculate_entropy(password)
    if entropy < 30:
        feedback.append(f"Low entropy ({entropy} bits) — easily guessable.")
    elif entropy < 60:
        feedback.append(f"Moderate entropy ({entropy} bits).")
    else:
        feedback.append(f"High entropy ({entropy} bits) — strong randomness.")

    # Label
    labels = ["Very Weak", "Very Weak", "Weak", "Weak",
              "Moderate", "Moderate", "Strong", "Strong", "Very Strong", "Very Strong"]
    strength = labels[min(score, 9)]

    return {
        "score": score,
        "max_score": 9,
        "strength": strength,
        "entropy_bits": entropy,
        "feedback": feedback,
    }


def display_result(password: str, result: dict) -> None:
    """Pretty-print the password strength analysis."""
    bar = ("=" * result["score"]).ljust(9, "-")
    print("\n" + "=" * 50)
    print("  PASSWORD STRENGTH ANALYZER — py-security-toolkit")
    print("=" * 50)
    print(f"  Password  : {'*' * len(password)}")
    print(f"  Score     : [{bar}] {result['score']}/{result['max_score']}")
    print(f"  Strength  : {result['strength']}")
    print(f"  Entropy   : {result['entropy_bits']} bits")
    print("-" * 50)
    for item in result["feedback"]:
        print(f"  • {item}")
    print("=" * 50 + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Analyze password strength with entropy and pattern detection.",
        epilog="Example: python password_checker.py -p MyP@ssw0rd123"
    )
    parser.add_argument("-p", "--password", type=str, help="Password to analyze")
    parser.add_argument("--interactive", action="store_true",
                        help="Enter password interactively (hidden input)")
    args = parser.parse_args()

    if args.interactive:
        import getpass
        password = getpass.getpass("Enter password (hidden): ")
    elif args.password:
        password = args.password
    else:
        parser.print_help()
        sys.exit(1)

    result = check_password_strength(password)
    display_result(password, result)


if __name__ == "__main__":
    main()
