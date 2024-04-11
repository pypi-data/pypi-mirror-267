from pathlib import Path
import subprocess
import json
import os

from cleo.events.console_events import COMMAND
from cleo.events.console_command_event import ConsoleCommandEvent
from cleo.events.event_dispatcher import EventDispatcher
from dotenv import load_dotenv
from poetry.console.application import Application
from poetry.console.commands.env_command import EnvCommand
from poetry.plugins.application_plugin import ApplicationPlugin


class PoetryPlugin(ApplicationPlugin):
    def activate(self, application: Application):
        application.event_dispatcher.add_listener(
            COMMAND, self.main
        )

    def main(
        self,
        event: ConsoleCommandEvent,
        event_name: str,
        dispatcher: EventDispatcher
    ) -> None:
        command = event.command
        if not isinstance(command, EnvCommand):
            return

        # Check if Rust code needs to be rebuilt
        if self._rust_code_needs_rebuild():
            print("Rust code needs to be rebuilt.")
            self._rebuild_rust_code()
        else:
            print("Rust code is up to date.")

    def _rust_code_needs_rebuild(self) -> bool:
        """
        Check if Rust code needs to be rebuilt by comparing
        timestamps of source files and compiled binaries.
        """
        # Define paths to Rust source files
        rust_src_dir = Path("src")
        rust_src_files = list(rust_src_dir.glob("*.rs"))
        
        # Check if there are no Rust source files
        if not rust_src_files:
            return False  # No Rust code to rebuild

        # Check if the target directory exists
        target_dir = Path("target")
        if not target_dir.exists():
            return True  # Target directory doesn't exist, rebuild needed

        # Check modification time of each Rust source file
        for src_file in rust_src_files:
            # Check if source file is newer than target binary
            target_binary = target_dir / src_file.stem
            if not target_binary.exists() or src_file.stat().st_mtime > target_binary.stat().st_mtime:
                return True  # Rust source file is newer than target binary, rebuild needed

        return False  # No need to rebuild Rust code

    def _rebuild_rust_code(self):
        """
        Rebuild Rust code using cargo.
        """
        print("Rebuilding Rust code.")
        subprocess.run(["cargo", "build"])  # Assuming cargo is in PATH
