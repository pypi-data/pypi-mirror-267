import subprocess
import tomllib as toml
from cleo.io.io import IO
from cleo.events.console_events import COMMAND
from cleo.events.console_command_event import ConsoleCommandEvent
from cleo.events.event_dispatcher import EventDispatcher
from poetry.console.application import Application
from poetry.console.commands.env_command import EnvCommand
from poetry.plugins.application_plugin import ApplicationPlugin


class PoetryPlugin(ApplicationPlugin):
    is_needed: bool = False
    command: str | None = None
    run_in_venv: bool = False
    venv_path = ".venv"

    def activate(self, application: Application):
        self.read_pyproject_toml()
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
        io = event.io

        verbose_level= io.is_verbose() + io.is_very_verbose() + io.is_debug()
        print(verbose_level)
        
        if self.is_needed:
            self._rebuild_rust_code(io)
        elif verbose_level ==3:
            io.write_line("Maturin Watchdog not set to run any command.")

    def read_pyproject_toml(self) -> None:
        try:
            with open("pyproject.toml", "rb") as file:
                config = toml.load(file)

                self.is_needed =  config.get("tool", {}).get("watson", {}).get("always_compile_before_running", False)
                self.compile_command = config.get("tool", {}).get("watsong", {}).get("command", self.command)
                self.run_in_venv = config.get("tool", {}).get("watson", {}).get("run_in_venv", self.run_in_venv)
                self.venv_path = config.get("tool", {}).get("watson", {}).get("venv_path", self.venv_path)

        except FileNotFoundError:
            self.is_needed = False

    def _rebuild_rust_code(self, io: IO):
        """
        Rebuild Rust code using maturin.
        """
        if self.run_in_venv:
            prefix = f"source {self.venv_path}/bin/activate && "
        else: 
            prefix = ""

        process = subprocess.run(f"{prefix}{self.compile_command}", capture_output=True, shell=True, text=True)
        if process.returncode != 0:
            io.write_error("Failed to rebuild Rust code. Are you sure maturin is installed?")
            raise subprocess.CalledProcessError(process.returncode, process.args)
