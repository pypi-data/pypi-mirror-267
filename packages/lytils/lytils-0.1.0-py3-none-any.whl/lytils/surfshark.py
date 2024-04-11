import os
from .app import (
    is_process_running,
    kill_process,
    kill_service,
    start_process,
    start_service,
)
from .input import cinput
from .print import cprint


class Surfshark:
    def __init__(self, path: str):
        self.__path = path

    def ensure(self):
        # Pause if Surfshark is not running to allow user to connect to Surfshark
        is_running = is_process_running("Surfshark.exe")
        if not is_running:
            cprint("<y>Surfshark is not running. Starting Surfshark now...")
            self.start()  # Ensure
        else:
            print("Surfshark is running. Proceeding...")
        while not is_running:
            cinput("Press <y><ENTER><w> once Surfshark has connected to continue...")
            is_running = is_process_running("Surfshark.exe")

    def kill(self):
        kill_process("Surfshark.exe")
        kill_service("Surfshark Service")
        kill_service("Surfshark WireGuard Service")

    def start(self):
        # Main application
        start_process(self.__path)
        # Background service
        start_service("Surfshark Service")
        start_service("Surfshark WireGuard Service")
