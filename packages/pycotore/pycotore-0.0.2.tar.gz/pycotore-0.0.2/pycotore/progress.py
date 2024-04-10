import sys
import os
from logging import getLogger, DEBUG, basicConfig

basicConfig(level=DEBUG)
_logger = getLogger(__name__)


class PorgressBar():
    """
    Progress bar class
    """

    def __init__(self, base_marker: str = ".", done_marke: str = "#", current_marker: str = ">"):
        self.preffix: str = ""
        self.suffix: str = ""
        self.bar_length: int = 0
        self.bar_size: int = 0
        self.terminal_size: int = os.get_terminal_size().columns
        self.progress: float = 0.00
        self.total: float = 100.00
        self.done_marker = done_marke
        self.in_progress_marker = base_marker
        self.current_marker = current_marker

    def __str__(self):
        bar = f"prefix: {self.preffix}\nsufix: {self.suffix}\nbar size: {self.bar_length}\ncurrent terminal: {self.terminal_size}\nbar size: {self.bar_size}\nMarker: {self.done_marker}\ntotal: {self.total}\nprogress: {self.progress}"
        return bar

    def __update_bar_length(self) -> None:
        """
        Updating progress bar total size
        """
        self.bar_length = len(self.preffix) + len(self.suffix) + 1
        self.__update_bar_size()

    def __update_bar_size(self) -> None:
        self.bar_size = self.terminal_size - self.bar_length - 3

    def draw(self) -> None:
        finished = int(self.bar_size * self.progress / self.total)
        finished_mark = self.done_marker * finished
        in_progress_mark = self.in_progress_marker * (self.bar_size - finished - 1)
        if self.bar_size <= finished:
            self.current_marker = ""
        if self.bar_length > self.terminal_size:
            sys.stdout.write("\rDL:")
        else:
            sys.stdout.write(f"{self.preffix} [{finished_mark}{self.current_marker}{in_progress_mark}] {self.suffix}\r")
            sys.stdout.flush()

    def set_prefix(self, preffix: str) -> None:
        """
        Change bar prefix
        """
        self.preffix = preffix
        self.__update_bar_length()

    def set_suffix(self, suffix: str) -> None:
        """
        Change bar suffix
        """
        self.suffix = suffix
        self.__update_bar_length()

    def set_bar_size(self, size: int) -> None:
        """
        Change bar size
        """
        try:
            if int(size):
                self.bar_size = size
        except ValueError:
            _logger.warning("Unable to set bar size")

    def update_progress(self, done: float) -> None:
        """
        Update progress done percentage
        """
        # self.progress = round(done * 100 / self.total, 2)
        self.progress = done

    def set_total(self, total) -> None:
        """
        Set progress bar total value
        """
        try:
            if float(total):
                self.total = total
        except ValueError:
            _logger.warning("Unable to set total")
