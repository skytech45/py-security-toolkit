import re
import argparse
import sys

def check_password_strength(password: str) -> dict:
    """
    Analyze the strength of a password based on common security criteria.
    Returns a dictionary with score and feedback.
    """
    score = 0
    feedback = []

    # Length check
    if len(password) < 8:
        feedback.append("Password is too short (minimum 8 characters).")
    elif len(password) >= 12:
        score += 2
        feedback.append("Good length.")
    else:
        score += 1
        feedback.append("Length is acceptable.")

    # Complexity checks
    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("Add lowercase letters for better security.")

    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("Add uppercase letters for better security.")

    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("Add numbers for better security.")

    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1
    else:
        feedback.append("Add special characters for better security.")

    # Categorization
    if score < 3:
        strength = "Weak"
    elif score < 5:
        strength = "Moderate"
    else:
        strength = "Strong"

    return {
        "score": score,
        "strength": strength,
        "feedback": feedback
    }

def main():
    parser = argparse.ArgumentParser(description="A simple password strength analyzer.")
    parser.add_argument("-p", "--password", help="The password to analyze (optional, will prompt if not provided).")
    
    args = parser.parse_args()
    
    password = args.password
    if not password:
        import getpass
        password = getpass.getpass("Enter password to analyze: ")

    if not password:
        print("[!] Error: No password provided.")
        sys.exit(1)

    result = check_password_strength(password)
    
    print("-" * 30)
    print(f"Strength: {result['strength']} ({result['score']}/6)")
    print("-" * 30)
    for note in result['feedback']:
        print(f"- {note}")
    print("-" * 30)

if __name__ == "__main__":
    main()
