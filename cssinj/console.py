import datetime


class Console:
    def log(self, status: str, message: str):
        now = datetime.datetime.now()
        if status == "server":
            print(f"[{now.strftime("%Y-%m-%d %H:%M:%S")}] 🛠️ {message}")
        elif status == "exfiltration":
            print(f"[{now.strftime("%Y-%m-%d %H:%M:%S")}] 🔎 {message}")
        elif status == "end_exfiltration":
            print(f"[{now.strftime("%Y-%m-%d %H:%M:%S")}] ✅ {message}")
        elif status == "connection":
            print(f"[{now.strftime("%Y-%m-%d %H:%M:%S")}] 🌐 {message}")
        elif status == "connection_details":
            print(f"[{now.strftime("%Y-%m-%d %H:%M:%S")}] ⚙️ {message}")
        elif status == "error":
            print(f"[{now.strftime("%Y-%m-%d %H:%M:%S")}] ❌ {message}")
