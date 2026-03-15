import hashlib
import argparse
import os

def calculate_hash(file_path, algorithm='sha256'):
    """Calculate the hash of a file using the specified algorithm."""
    hash_func = getattr(hashlib, algorithm)()
    try:
        with open(file_path, 'rb') as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                hash_func.update(byte_block)
        return hash_func.hexdigest()
    except FileNotFoundError:
        return f"[!] Error: File '{file_path}' not found."
    except Exception as e:
        return f"[!] Error: {e}"

def main():
    parser = argparse.ArgumentParser(description="A simple file hash generator.")
    parser.add_argument("file", help="Path to the file to hash.")
    parser.add_argument("-a", "--algorithm", choices=['md5', 'sha1', 'sha256', 'sha512'], default='sha256', help="Hash algorithm to use (default: sha256)")
    parser.add_argument("-v", "--verify", help="Verify the calculated hash against this value.")

    args = parser.parse_args()

    if not os.path.isfile(args.file):
        print(f"[!] Error: '{args.file}' is not a valid file.")
        return

    print(f"[*] Calculating {args.algorithm.upper()} for: {args.file}")
    file_hash = calculate_hash(args.file, args.algorithm)
    
    if "[!]" in file_hash:
        print(file_hash)
    else:
        print(f"[+] {args.algorithm.upper()}: {file_hash}")
        
        if args.verify:
            if file_hash.lower() == args.verify.lower():
                print("[+] Verification: SUCCESS (Hashes match)")
            else:
                print("[!] Verification: FAILED (Hashes do not match)")

if __name__ == "__main__":
    main()
