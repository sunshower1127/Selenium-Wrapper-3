import pyperclip

from ._xpath_parser.sw3_parser import xpath2sw3
from ._xpath_parser.xpath_parser import *
from .node import *


def is_xpath(expr: str) -> bool:
    return not any(char.isupper() for char in expr)


def sw3_to_xpath(expr: str):
    xpath = str(eval(expr))  # noqa: S307
    if not xpath.startswith(("/", "(")):
        xpath = f"//{xpath}"
    return xpath


def xpath_to_sw3(expr: str):
    return xpath2sw3(expr)


print("xpath나 sw3의 expression을 입력하세요(클립보드에 복사됨)")
while True:
    expr = input("> ")
    result = xpath_to_sw3(expr) if is_xpath(expr) else sw3_to_xpath(expr)
    pyperclip.copy(result)
    print(f"\033[32m{result}\033[0m")

"""
버그 리스트

> /div[12]
''/Div()[12]

"""
