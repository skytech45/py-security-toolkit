# Python Security Toolkit

A collection of lightweight, useful Python utilities for security analysis, network scanning, and automation.

## Features
- [x] **Network Scanner**: Identify active hosts and open ports using multi-threading.
- [x] **Hash Generator/Validator**: Quickly generate and verify file hashes (MD5, SHA-1, SHA-256, SHA-512).
- [x] **Password Strength Checker**: Analyze password complexity and provide security feedback.
- [x] **Subdomain Finder**: Basic multi-threaded reconnaissance tool for finding active subdomains.
- [x] **HTTP Header Analyzer**: Check for security headers (CSP, HSTS, etc.) on any website.

## Installation
```bash
git clone https://github.com/skytech45/py-security-toolkit.git
cd py-security-toolkit
pip install -r requirements.txt
```

## Usage

### Network Scanner
```bash
python network_scanner.py 127.0.0.1 -s 1 -e 1024 -t 200
```

### Hash Tool
```bash
# Calculate SHA-256 hash of a file
python hash_tool.py path/to/file.ext

# Verify a file's hash
python hash_tool.py path/to/file.ext -a md5 -v <expected_md5_hash>
```

### Password Strength Checker
```bash
# Analyze a password
python password_checker.py -p "YourPassword123!"
```

### Subdomain Finder
```bash
# Search for subdomains of a target domain
python subdomain_finder.py google.com -t 20
```

### HTTP Header Analyzer
```bash
# Analyze security headers of a website
python header_analyzer.py google.com
```

## License
MIT
