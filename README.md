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
| `network_scanner.py` | Multi-threaded TCP port scanner |
| `port_banner_grabber.py` | Port scanner with service banner grabbing |
| `subdomain_finder.py` | DNS-based subdomain enumeration |
| `header_analyzer.py` | HTTP security header analyzer |
| `hash_tool.py` | File hash generator and validator |
| `password_checker.py` | Password strength analyzer with entropy scoring |

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
Scan open ports on a target host using multi-threading.
```bash
python network_scanner.py -t 192.168.1.1 -s 1 -e 1024
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
python subdomain_finder.py -d example.com -w wordlist.txt -t 100
python subdomain_finder.py -d example.com -o found.txt
```

### 🔒 HTTP Header Analyzer
Audit a website's security headers.
```bash
python header_analyzer.py -u https://example.com
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

---

## 📁 Project Structure

```
py-security-toolkit/
├── network_scanner.py       # Port scanner
├── port_banner_grabber.py   # Banner grabber
├── subdomain_finder.py      # Subdomain enum
├── header_analyzer.py       # HTTP header audit
├── hash_tool.py             # Hash utility
├── password_checker.py      # Password analysis
├── requirements.txt         # Dependencies
├── LICENSE                  # MIT License
└── README.md                # This file
```

---

## ⚙️ Requirements

- Python 3.8+
- `requests` library

Install dependencies:
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
