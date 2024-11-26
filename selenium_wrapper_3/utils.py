from __future__ import annotations

from time import sleep
from typing import TYPE_CHECKING, TypeVar

from selenium.common.exceptions import WebDriverException

from .driver import Driver, driver
from .exceptions import CannotFindElement
from .nodes import Nodes

if TYPE_CHECKING:
    from typing import Callable

    from .node import Node


T = TypeVar("T")


def retry(func: Callable[[], T]):
    for _ in range(int(Driver().timeout / Driver().freq)):
        try:
            return func()
        except WebDriverException:
            sleep(Driver().freq)

    return CannotFindElement


def url(addr: str):
    driver().get(addr)


def check(xpath: str | Node):
    result = retry(lambda: driver().find_element("xpath", str(xpath)))
    return result != CannotFindElement


def count(xpath: str | Nodes):
    result = len(driver().find_elements("xpath", str(xpath)))
    return result


def populate(xpath: str | Nodes):
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

    print(list(map(text, populate(All(_ // Div()))))
    ```
    """
    length = count(xpath)
    nodes = xpath if isinstance(xpath, Nodes) else Nodes(xpath)
    for i in range(length):
        yield nodes[i]


def send_keys(xpath: str | Node, *value: str):
    result = retry(lambda: driver().find_element("xpath", str(xpath)).send_keys(*value))
    if result == CannotFindElement:
        raise CannotFindElement(xpath)


def click(xpath: str | Node):
    send_keys(xpath, "\n")


def text(xpath: str | Node):
    result = retry(lambda: driver().find_element("xpath", str(xpath)).text)
    if isinstance(result, str):
        return result

    raise CannotFindElement(xpath)


def frame(xpath: str | Node = "default"):
    if xpath == "default":
        driver().switch_to.default_content()
        return

    result = retry(
        lambda: driver().switch_to.frame(driver().find_element("xpath", str(xpath)))
    )
    if result == CannotFindElement:
        raise CannotFindElement(xpath)
