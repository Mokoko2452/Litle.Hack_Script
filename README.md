# LHS
██╗     ██╗  ██╗███████╗
██║     ██║  ██║██╔════╝
██║     ███████║███████╗
██║     ██╔══██║╚════██║
███████╗██║  ██║███████║
╚══════╝╚═╝  ╚═╝╚══════╝

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## Overview
LHS is an advanced Python tool designed for automating various network penetration tests. It integrates multiple attack techniques including network scanning, deauthentication, brute-force, man-in-the-middle (MITM) operations, and denial-of-service (DoS) attacks. Use LHS for ethical and educational purposes only.

---

## Features
- **Dynamic Network Scanning:** Discover wireless networks using Scapy and psutil.
- **Deauthentication Attacks:** Target both Access Points and individual clients.
- **Brute Force Attacks:** Utilize Crunch and John the Ripper for customizable password cracking.
- **Man-in-the-Middle (MITM) Attacks:** Execute ARP spoofing using external tools or custom Scapy scripts.
- **Denial-of-Service (DoS) Attacks:** Launch TCP/UDP flood attacks via hping3.
- **Terminal Automation:** Open new terminal windows for concurrent operations.
- **Automated Monitor Mode Management:** Detect and configure monitor mode on your wireless interface.

---

## Installation

### Prerequisites
- **Python 3.x** – [Download Python](https://www.python.org/downloads/)
- **Python Libraries:**  
  - `psutil` (Install with: `pip install psutil`)
  - `scapy` (Install with: `pip install scapy`)
- **Additional Tools:**  
  - `airmon-ng`  
  - `aireplay-ng`  
  - `crunch`  
  - `john`  
  - `hping3`  
  - `gnome-terminal`

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/mokoko2452/LHS.git
   cd LHS

    Install Python dependencies:

pip install -r requirements.txt

Run the script as root:

    sudo python3 your_script.py

Usage

Launch LHS with:

sudo python3 your_script.py

Follow the on-screen menu options to:

    Scan nearby networks.
    Perform deauthentication attacks.
    Execute brute-force attacks.
    Run man-in-the-middle (MITM) attacks.
    Initiate DoS attacks.
    Exit the tool.


License

This project is licensed under the MIT License. See the LICENSE file for details.
Contact

    Email: mokoko2452@gmail.com
    GitHub: mokoko2452

Happy Hacking! 
