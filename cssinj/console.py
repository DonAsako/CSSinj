import datetime


class Console:
    @staticmethod
    def log(status: str, message: str):
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

    @staticmethod
    def error_handler(exception: Exception, context: dict):
        Console.log("error", exception)
