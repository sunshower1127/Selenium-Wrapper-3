from __future__ import annotations

from functools import wraps
from time import sleep
from typing import TYPE_CHECKING, Any, Literal, TypeVar, overload

from selenium.common.exceptions import WebDriverException
from selenium_wrapper_3.driver.driver import Driver
from selenium_wrapper_3.exception.exception import (
    CannotFindElement,
    PollTimeout,
    SeleniumWrapperException,
)
from selenium_wrapper_3.node.node import Node

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


def poll(
    func: Callable[[], T],
    condition: Callable[[T], bool] = lambda x: bool(x),
):
    """Retry a function until it meets a condition or timeout.

    Raises:
        exception.PollTimeout: When the condition is not met within the timeout period
    """
    for _ in range(int(Driver().timeout / Driver().freq)):
        try:
            result = func()
            if condition(result):
                return result
            else:
                sleep(Driver().freq)
        except WebDriverException:
            sleep(Driver().freq)

    try:
        result = func()
        if condition(result):
            return result
        else:
            msg = f"Value: {result}"
        raise PollTimeout(msg)
    except WebDriverException as e:
        raise PollTimeout(e.msg or "") from None


def url(addr: str):
    Driver().web.get(addr)


@add_descendant
def check(xpath: str | Node):
    print(xpath)
    result = retry(lambda: Driver().web.find_element("xpath", str(xpath)))
    return result != CannotFindElement


@add_descendant
def count(xpath: str | Node):
    result = len(Driver().web.find_elements("xpath", str(xpath)))
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
    for i in range(count(Div()))):
        print(text(Div())[i]))
    ```
    into
    ```python
    for div in populate(Div())):
        print(text(div))

    print([text(div) for div in populate(Div()))])

    """
    length = count(xpath)
    if isinstance(xpath, Node):
        node = xpath.__class__()
        node.xpath = xpath.xpath
    else:
        node = Node()
        node.xpath = xpath

    for i in range(1, length + 1):
        yield node[i]


@add_descendant
def send_keys(xpath: str | Node, value: str | list[str]):
    if isinstance(value, str):
        value = [value]
    result = retry(
        lambda: Driver().web.find_element("xpath", str(xpath)).send_keys(*value)
    )
    if result == CannotFindElement:
        raise CannotFindElement(xpath)


@add_descendant
def click(xpath: str | Node, method: Literal["script", "click", "enter"] = "script"):
    if method == "script":
        retry(
            lambda: Driver().web.execute_script(
                "arguments[0].click();",
                Driver().web.find_element("xpath", str(xpath)),
            )
        )
        return

    if method == "enter":
        send_keys(xpath, "\n")
    else:
        retry(lambda: Driver().web.find_element("xpath", str(xpath)).click())


@add_descendant
def text(xpath: str | Node):
    result = retry(lambda: Driver().web.find_element("xpath", str(xpath)).text)
    if isinstance(result, str):
        return result

    raise CannotFindElement(xpath)


def root_frame():
    Driver().web.switch_to.default_content()


class FrameContext:
    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        root_frame()


@add_descendant
def frame(xpath: str | Node):
    result = retry(
        lambda: Driver().web.switch_to.frame(
            Driver().web.find_element("xpath", str(xpath))
        )
    )

    if result == CannotFindElement:
        raise CannotFindElement(xpath)

    return FrameContext()


if __name__ == "__main__":
    url("https://www.naver.com")
    check("/sav")
