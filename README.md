# 🔐 Python Security Toolkit

> A lightweight, modular collection of Python security and network analysis utilities — built for ethical hacking, CTFs, and developer productivity.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Author](https://img.shields.io/badge/Author-skytech45-orange)

---

## 📦 Tools Included

| File | Description |
|------|-------------|
| `network_scanner.py` | Multi-threaded TCP port scanner with JSON output |
| `port_banner_grabber.py` | Port scanner with service banner grabbing |
| `subdomain_finder.py` | DNS-based subdomain enumeration (refactored) |
| `ssh_bruter.py` | Multi-threaded SSH brute-forcer |
| `header_analyzer.py` | HTTP security header analyzer |
| `ssl_checker.py` | SSL/TLS certificate analyzer |
| `hash_tool.py` | File hash generator and validator |
| `password_checker.py` | Password strength analyzer with entropy scoring |
| `dir_bruter.py` | Multi-threaded directory brute-forcer |
| `whois_lookup.py` | WHOIS domain information lookup with JSON export |

---

## 🚀 Installation

```bash
git clone https://github.com/skytech45/py-security-toolkit.git
cd py-security-toolkit
pip install -r requirements.txt
```

---

## 🛠️ Usage

### 🔎 Network Scanner
Scan open ports on a target host using multi-threading. Supports JSON output.
```bash
python network_scanner.py 192.168.1.1
python network_scanner.py 192.168.1.1 -s 1 -e 1024 -t 200
python network_scanner.py example.com -s 1 -e 65535 -o results.json
```

### 🏷️ Port Banner Grabber
Scan ports and grab service banners for identification.
```bash
python port_banner_grabber.py -t example.com
python port_banner_grabber.py -t 192.168.1.1 -p 22,80,443,8080
python port_banner_grabber.py -t example.com -p 1-1000 -o results.csv
```

### 🌐 Subdomain Finder
Enumerate subdomains using multi-threaded DNS resolution.
```bash
python subdomain_finder.py -d example.com
python subdomain_finder.py -d example.com -w wordlists/common_subdomains.txt -t 50
python subdomain_finder.py -d example.com -o found.txt
```

### 🔑 SSH Brute-Forcer
A multi-threaded SSH brute-forcer for authorized testing.
```bash
python ssh_bruter.py -t 192.168.1.1 -u admin -w wordlists/common_passwords.txt -th 10
```

### 🔒 HTTP Header Analyzer
Audit a website's security headers.
```bash
python header_analyzer.py -u https://example.com
```

### 🛡️ SSL/TLS Checker
Analyze website SSL certificates for expiration and configuration.
```bash
python ssl_checker.py google.com
```

### #️⃣ Hash Tool
Generate and verify file hashes.
```bash
python hash_tool.py -f myfile.txt -a sha256
python hash_tool.py -f myfile.txt --verify abc123...
```

### 🔑 Password Checker
Analyze password strength with entropy scoring.
```bash
python password_checker.py -p MyP@ssw0rd123
python password_checker.py --interactive
```

### 📂 Directory Brute-Forcer
Discover hidden directories and files on a web server.
```bash
python dir_bruter.py https://example.com -w wordlists/common_dirs.txt -t 50
```

### 🌍 WHOIS Lookup
Retrieve WHOIS registration and ownership information for any domain.
```bash
python whois_lookup.py example.com
python whois_lookup.py google.com --ip
python whois_lookup.py example.com -o whois_result.json
python whois_lookup.py --interactive
```

---

## 📁 Project Structure

```
py-security-toolkit/
├── network_scanner.py       # Multi-threaded port scanner (JSON output)
├── port_banner_grabber.py   # Banner grabber
├── subdomain_finder.py      # Subdomain enumeration
├── ssh_bruter.py            # SSH brute-forcer
├── header_analyzer.py       # HTTP security header audit
├── ssl_checker.py           # SSL/TLS certificate checker
├── hash_tool.py             # File hash utility
├── password_checker.py      # Password strength analyzer
├── dir_bruter.py            # Directory brute-forcer
├── whois_lookup.py          # WHOIS domain lookup tool
├── wordlists/               # Common wordlists
│   ├── common_subdomains.txt
│   └── common_passwords.txt
├── requirements.txt         # Python dependencies
├── LICENSE                  # MIT License
└── README.md                # Documentation
```

---

## ⚙️ Requirements

- Python 3.8+
- See `requirements.txt` for all dependencies

```bash
pip install -r requirements.txt
```

---

## ⚠️ Disclaimer

> These tools are intended for **educational purposes** and **authorized security testing only**.
> Do not use on systems without explicit permission.
> The author is not responsible for any misuse.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 👨‍💻 Author

**Sachin Kumar (skytech45)**
Electronics Engineering Student | AI & Cybersecurity Enthusiast
📍 Bihar, India

---

*Part of an ongoing developer portfolio — actively maintained.*
