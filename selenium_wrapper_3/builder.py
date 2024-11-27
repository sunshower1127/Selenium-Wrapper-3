from time import sleep
from typing import Callable, Literal

from selenium.webdriver import ChromeOptions
from selenium_wrapper_3.singleton import SingletonMeta
from selenium_wrapper_3.utils import Driver, url

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
        self.freq = 0.5
        self.timeout = 10

    def add_option(self, option: Option):
        option_dict[option](self.options)
        return self

    def debug_setting(self):
        self.add_option("do not quit")
        self.add_option("mute audio")
        self.add_option("disable blocking alert")
        self.add_option("disable top infobar")
        return self

    def headless_setting(self):
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

    def set_retry(self, freq: float, timeout: float):
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
            driver.driver.set_window_size(self.width, self.height)
        driver.set_retry(self.freq, self.timeout)


if __name__ == "__main__":
    ChromeBuilder().debug_setting().build()
    url("https://google.com")
    sleep(100)
