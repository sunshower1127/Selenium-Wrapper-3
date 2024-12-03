from time import sleep
from typing import Callable, Literal

from selenium.webdriver import ChromeOptions

from selenium_wrapper_3.pattern.singleton import SingletonMeta
from selenium_wrapper_3.util.util import Driver, url

Option = Literal[
    "do not quit",
    "mute audio",
    "maximize",
    "headless",
    "disable blocking alert",
    "disable top infobar",
]


option_dict: dict[Option, Callable[[ChromeOptions], None]] = {
    "do not quit": lambda options: options.add_experimental_option("detach", True),  # noqa: FBT003
    "mute audio": lambda options: options.add_argument("--mute-audio"),
    "maximize": lambda options: options.add_argument("--start-maximized"),
    "headless": lambda options: options.add_argument("--headless"),
    "disable blocking alert": lambda options: options.add_argument(
        "--disable-popup-blocking"
    ),
    "disable top infobar": lambda options: options.add_argument("--disable-infobars"),
}


class ChromeBuilder(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self.options = ChromeOptions()
        self.configure_poll()

    def add_option(self, option: Option):
        option_dict[option](self.options)
        return self

    def debug_setting(self):
        """Do not quit, mute audio, disable blocking alert, disable top infobar"""
        self.add_option("do not quit")
        self.add_option("mute audio")
        self.add_option("disable blocking alert")
        self.add_option("disable top infobar")
        return self

    def headless_setting(self):
        """Headless, mute audio, disable blocking alert, disable top infobar"""
        self.add_option("headless")
        self.add_option("mute audio")
        self.add_option("disable blocking alert")
        self.add_option("disable top infobar")
        return self

    def add_argument(self, argument: str):
        self.options.add_argument(argument)
        return self

    def add_experimental_option(self, option: str, value):
        self.options.add_experimental_option(option, value)
        return self

    def configure_poll(self, freq=0.1, timeout=10):
        """Configure polling frequency and timeout

        Args:
            freq: Time between polls in seconds
            timeout: Maximum time to poll in seconds
        """
        self.freq = freq
        self.timeout = timeout
        return self

    def set_window_size(self, width: int, height: int):
        self.width = width
        self.height = height
        return self

    def build(self):
        driver = Driver(self.options)
        if hasattr(self, "width") and hasattr(self, "height"):
            driver.web.set_window_size(self.width, self.height)
        driver.set_retry(self.freq, self.timeout)


if __name__ == "__main__":
    ChromeBuilder().debug_setting().build()
    url("https://google.com")
    sleep(100)
