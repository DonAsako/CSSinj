---

# CSSINJ  

```
  _____   _____   _____  _____  _   _       _     _____  __     __
 / ____| / ____| / ____||_   _|| \ | |     | |   |  __ \ \ \   / /
| |     | (___  | (___    | |  |  \| |     | |   | |__) | \ \_/ /
| |      \___ \  \___ \   | |  | . ` | _   | |   |  ___/   \   /
| |____  ____) | ____) | _| |_ | |\  || |__| | _ | |        | |
 \_____||_____/ |_____/ |_____||_| \_| \____/ (_)|_|        |_|
```

## About  

**CSSINJ** is a penetration testing tool that exploits **CSS injection vulnerabilities** to exfiltrate sensitive information from web applications. This tool is designed for security professionals to assess the security posture of web applications by demonstrating how CSS can be used to extract data covertly.  


## Installation  

To install and set up **CSSINJ**, run the following commands:  

```bash
git clone https://github.com/DonAsako/CSSinj.git
cd CSSinj
python3 -m venv venv  
source venv/bin/activate
python3 -m pip install -r requirements.txt
```

Now you’re ready to use **CSSINJ**! 🎯  

## Usage  

```bash
python3 CSSINJ.py [-h] -H HOSTNAME -p PORT -i IDENTIFIER -l LENGTH
```

### Options  

| Option                 | Description                                 |
|------------------------|---------------------------------------------|
| `-h, --help`           | Show help message and exit                  |
| `-H, --hostname`       | Attacker hostname or IP address             |
| `-p, --port`           | Port number of the attacker                 |
| `-i, --identifier`     | CSS identifier (CSS selector) to extract data |
| `-l, --length`         | Length of data to extract                   |

### Example  

```bash
python3 CSSINJ.py  -H 127.0.0.1 -p 5005 -i input.here -l 10
```

## Disclaimer  

This tool is intended **only for ethical hacking and security research**. **Unauthorized use on systems without explicit permission is illegal**. The developer **is not responsible** for any misuse of this tool.  

## Author  

**CSSINJ** was developed by **Asako**.  
