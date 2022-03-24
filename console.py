from datetime import datetime
from typing import Any
import rich
from rich.table import Table

class timer:

    def __init__(self) -> None:
        self.time = datetime.now()

    def getTime(self) -> str:
        now = datetime.now()
        delta = now - self.time
        return delta.total_seconds()

class Console:

    def __init__(self, saveToFile: bool=False) -> None:
        self.timers: dict = {}
        self.save = saveToFile

    def _init_grid(self) -> Table.grid:
        grid = Table.grid()
        grid.add_column()
        grid.add_column()

        return grid

    def _get_time(self) -> str:
        return datetime.now().strftime("[grey23][bold][[/bold]%H:%M:%S[bold]][/bold][/grey23] ")

    def toFile(self, toLog: str, type: str) -> None:
        if self.save:
            now = datetime.now()
            filename = now.strftime("./logs/%Y-%m-%d")+"-log.txt"
            logTime = now.strftime('%Y-%m-%d %H:%M:%S')
            toLog = " ".join(map(str, toLog))

            with open(filename, "a") as f:
                f.write(f"{logTime} [{type}] {toLog}\n")

    def log(self, *toLog: Any) -> None:
        grid = self._init_grid()
        grid.add_row(self._get_time(), " ".join(map(str, toLog)))
        rich.print(grid)
        self.toFile(toLog, "LOG")

    def info(self, *toLog: Any) -> None:
        grid = self._init_grid()
        toLog = " ".join(map(str, toLog))
        grid.add_row(self._get_time(), f"[white on cyan] INFO [/white on cyan] [cyan bold]{toLog}[/cyan bold]")
        rich.print(grid)
        self.toFile(toLog, "INFO")

    def warn(self, *toWarn: Any) -> None:
        grid = self._init_grid()
        toWarn = " ".join(map(str, toWarn))
        grid.add_row(self._get_time(), f"[white on orange_red1] WARN [/white on orange_red1] [yellow]{toWarn}[/yellow]")
        rich.print(grid)
        self.toFile(toWarn, "WARN")

    def error(self, *toError: Any) -> None:
        grid = self._init_grid()
        toError = " ".join(map(str, toError))
        grid.add_row(self._get_time(), f"[white on red] ERROR [/white on red] [red bold]{toError}[/red bold]")
        rich.print(grid)
        self.toFile(toError, "ERROR")

    def clear(self) -> None:
        print("\033[H\033[J")

    def time(self, timerName: str="timer"):
        self.timers[timerName] = timer()
        self.toFile(f"Timer {timerName} started.", "TIME")

    def timeEnd(self, timerName: str="timer") -> float:
        time = self.timers.get(timerName)

        if time:
            seconds = time.getTime()
            self.timers.pop(timerName)
            self.toFile(f"Timer {timerName} ended. Time: {seconds} seconds.", "TIME")
            return seconds

    def timeLog(self, timerName: str="timer") -> float:
        time = self.timers.get(timerName)

        if time:
            seconds = time.getTime()
            self.toFile(f"Timer {timerName} logged at {seconds}.", "TIME")
            return seconds