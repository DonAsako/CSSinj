import datetime
# import asyncio


class Console:
    # def __init__(self):
    #     self.is_client_connected = asyncio.Event()

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

    # async def get_command(self):
    #     if not self.is_client_connected.is_set():
    #         await self.print_wait_for_connection()
    #     command = input("> ")

    # async def print_wait_for_connection(self):
    #     i = 0
    #     while(not self.is_client_connected.is_set()):
    #         print(f"\r{"Waiting for connection" + 4*'.'+ i*'.' + (5-i) * ' '}", end="", flush=True)
    #         if i > 4:
    #             i = 0
    #         i+=1

    #         await asyncio.sleep(0.5)
