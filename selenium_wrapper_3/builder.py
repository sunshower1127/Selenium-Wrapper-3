from time import sleep
from typing import Literal

from selenium.webdriver import ChromeOptions

from .singleton import SingletonMeta
from .utils import Driver, url

Options = Literal[
    "keep_browser_open",
    "mute_audio",
    "maximize",
    "headless",
    "disable_popup",
    "disable_info_bar",
]


class ChromeBuilder(metaclass=SingletonMeta):
    freq = 0.5
    timeout = 10

    def __init__(self) -> None:
        self.options = ChromeOptions()

    def add_option(self, option: Options):
        if option == "keep_browser_open":
            self.options.add_experimental_option("detach", True)  # noqa: FBT003
        elif option == "mute_audio":
            self.options.add_argument("--mute-audio")
        elif option == "maximize":
            self.options.add_argument("--start-maximized")
        elif option == "headless":
            self.options.add_argument("--headless")
        elif option == "disable_popup":
            self.options.add_argument("--disable-popup-blocking")
        elif option == "disable_info_bar":
            self.options.add_argument("--disable-infobars")

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
    ChromeBuilder().add_option("disable_info_bar").build()
    url("https://google.com")
    sleep(100)
