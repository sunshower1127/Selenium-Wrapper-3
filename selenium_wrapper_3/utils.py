from __future__ import annotations

from functools import wraps
from time import sleep
from typing import TYPE_CHECKING, Any, TypeVar, overload

from selenium.common.exceptions import WebDriverException
from selenium_wrapper_3.driver import Driver, driver
from selenium_wrapper_3.exceptions import (
    CannotFindElement,
    RetryUntilTimeout,
    SeleniumWrapperException,
)
from selenium_wrapper_3.node import Node

if TYPE_CHECKING:
    from collections.abc import Generator
    from typing import Callable


T = TypeVar("T")


class NoErrorContext:
    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        return issubclass(exc_type, SeleniumWrapperException)


def no_error():
    return NoErrorContext()


def add_descendant(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "xpath" not in kwargs:
            if not args:
                return func(*args, **kwargs)
            xpath = args[0]
            if isinstance(xpath, Node):
                xpath = xpath.xpath

            if not xpath.startswith(("/", "(")):
                xpath = f"//{xpath}"

            args = (xpath, *args[1:])
        else:
            xpath: str = kwargs["xpath"]
            if isinstance(xpath, Node):
                xpath = xpath.xpath

            if not xpath.startswith("/") and not xpath.startswith("//"):
                kwargs["xpath"] = f"//{xpath}"

        # 원래 함수 호출
        return func(*args, **kwargs)

    return wrapper


def retry(func: Callable[[], T]):
    for _ in range(int(Driver().timeout / Driver().freq)):
        try:
            return func()
        except WebDriverException:
            sleep(Driver().freq)

    return CannotFindElement


def retry_until(
    func: Callable[[], T], condition: Callable[[T], bool] = lambda x: bool(x)
):
    for _ in range(int(Driver().timeout / Driver().freq)):
        try:
            result = func()
            if condition(result):
                return result
            else:
                sleep(Driver().freq)
        except WebDriverException:
            sleep(Driver().freq)

    result = func()
    if condition(result):
        return result
    else:
        msg = f"Value: {result}"
        raise RetryUntilTimeout(msg)


def url(addr: str):
    driver().get(addr)


@add_descendant
def check(xpath: str | Node):
    print(xpath)
    result = retry(lambda: driver().find_element("xpath", str(xpath)))
    return result != CannotFindElement


@add_descendant
def count(xpath: str | Node):
    result = len(driver().find_elements("xpath", str(xpath)))
    return result


SubNode = TypeVar("SubNode", bound=Node)


@overload
def populate(xpath: SubNode) -> Generator[SubNode, Any, None]: ...


@overload
def populate(xpath: str) -> Generator[Node, Any, None]: ...


@add_descendant
def populate(xpath: str | SubNode):  # type: ignore[SubNode]
    """Simplify the following code:

    ```python
    for i in range(count(All(_ // Div()))):
        print(text(All(_ // Div())[i]))
    ```
    into
    ```python
    for div in populate(All(_ // Div())):
        print(text(div))

    print([text(div) for div in populate(All(_ // Div()))])

    """
    length = count(xpath)
    if isinstance(xpath, Node):
        node = xpath.__class__()
        node.xpath = xpath.xpath
    else:
        node = Node()
        node.xpath = xpath

    for i in range(length):
        yield node[i]


@add_descendant
def send_keys(xpath: str | Node, value: str | list[str]):
    if isinstance(value, str):
        value = [value]
    result = retry(lambda: driver().find_element("xpath", str(xpath)).send_keys(*value))
    if result == CannotFindElement:
        raise CannotFindElement(xpath)


@add_descendant
def click(xpath: str | Node):
    send_keys(xpath, "\n")


@add_descendant
def text(xpath: str | Node):
    result = retry(lambda: driver().find_element("xpath", str(xpath)).text)
    if isinstance(result, str):
        return result

    raise CannotFindElement(xpath)


def root_frame():
    driver().switch_to.default_content()


class FrameContext:
    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        root_frame()


@add_descendant
def frame(xpath: str | Node):
    result = retry(
        lambda: driver().switch_to.frame(driver().find_element("xpath", str(xpath)))
    )

    if result == CannotFindElement:
        raise CannotFindElement(xpath)

    return FrameContext()


if __name__ == "__main__":
    url("https://www.naver.com")
    check("/sav")
