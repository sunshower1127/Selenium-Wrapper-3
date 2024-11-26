from selenium.webdriver import Chrome

from .singleton import SingletonMeta


class Driver(metaclass=SingletonMeta):
    def __init__(self, options=None):
        if options:
            self.driver = Chrome(options=options)
        else:
            self.driver = Chrome()

        self.driver.implicitly_wait(0)

    def set_retry(self, freq: float, timeout: float):
        self.freq = freq
        self.timeout = timeout
        return self


def driver():
    return Driver().driver
