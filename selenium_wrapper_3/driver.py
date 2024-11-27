from selenium.webdriver import Chrome
from selenium_wrapper_3.singleton import SingletonMeta


class RetryContext:
    def __init__(self, freq: float, timeout: float):
        self.freq = freq
        self.timeout = timeout

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        Driver().set_retry(self.freq, self.timeout)
        return exc_type is None


class Driver(metaclass=SingletonMeta):
    def __init__(self, options=None):
        if options:
            self.driver = Chrome(options=options)
        else:
            self.driver = Chrome()

        self.driver.implicitly_wait(0)
        self.freq = 0.5
        self.timeout = 10

    def set_retry(self, freq: float, timeout: float):
        retry_context = RetryContext(self.freq, self.timeout)
        self.freq = freq
        self.timeout = timeout
        return retry_context


def driver():
    return Driver().driver
