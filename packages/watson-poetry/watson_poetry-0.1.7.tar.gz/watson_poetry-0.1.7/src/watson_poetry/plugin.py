from enum import IntEnum
import subprocess
import tomllib as toml
from cleo.io.io import IO
from cleo.events.console_events import COMMAND
from cleo.events.console_command_event import ConsoleCommandEvent
from cleo.events.event_dispatcher import EventDispatcher
from poetry.console.application import Application
from poetry.console.commands.env_command import EnvCommand
from poetry.plugins.application_plugin import ApplicationPlugin

class Verbosity(IntEnum):
    QUIET = 0
    VERBOSE = 1
    VERY_VERBOSE = 2
    DEBUG = 3

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

        verbose_level= Verbosity(io.is_verbose() + io.is_very_verbose() + io.is_debug())
        print(verbose_level)
        
        if self.is_needed:
            self._run_command(io, verbose_level)
        elif verbose_level >= Verbosity.VERBOSE:
            io.write_line("Watson not set to run any command.")

    def read_pyproject_toml(self) -> None:
        try:
            with open("pyproject.toml", "rb") as file:
                config = toml.load(file)

                self.is_needed =  config.get("tool", {}).get("watson", {}).get("always_compile_before_running", False)
                self.command = config.get("tool", {}).get("watsong", {}).get("command", self.command)
                self.run_in_venv = config.get("tool", {}).get("watson", {}).get("run_in_venv", self.run_in_venv)
                self.venv_path = config.get("tool", {}).get("watson", {}).get("venv_path", self.venv_path)

        except FileNotFoundError:
            self.is_needed = False

    def _run_command(self, io: IO, verbosity: Verbosity):
        if self.run_in_venv:
            if verbosity is Verbosity.DEBUG:
                io.write_line(f"Adding prefix to activate venv: source {self.venv_path}/bin/activate &&")
            prefix = f"source {self.venv_path}/bin/activate && "
        else: 
            if verbosity is Verbosity.DEBUG:
                io.write_line("No prefix to activate venv.")
            prefix = ""
        if verbosity is Verbosity.DEBUG:
            io.write_line(f"Running command: {prefix}{self.command}")
        process = subprocess.run(f"{prefix}{self.command}", capture_output=True, shell=True, text=True)
        if process.returncode != 0:
            if verbosity is Verbosity.DEBUG:
                io.write_line(f"Command failed with return code {process.returncode}.")
            raise subprocess.CalledProcessError(process.returncode, process.args)
