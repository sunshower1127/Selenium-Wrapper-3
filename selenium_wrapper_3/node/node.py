from __future__ import annotations

from typing import TypeVar, overload

from selenium_wrapper_3._xpath_parser.xpath_parser import (
    Expr,
    parse_arg,
    parse_kwarg,
    wrap,
)

T = TypeVar("T")
SubNode = TypeVar("SubNode", bound="Node")


class Node:
    @overload
    def __init__(self, index: int): ...
    @overload
    def __init__(self, *args: Expr | str, **kwargs: str | int | float | bool): ...

    def __init__(self, *args: Expr | str | int, **kwargs: str | int | float | bool):
        tag_name = self.__class__.__name__.lower()
        if len(args) == 1 and isinstance(args[0], int):
            self.xpath = wrap(tag_name, [str(args[0])])
            return
        conditions = [parse_arg(arg) if isinstance(arg, tuple) else arg for arg in args]
        conditions += [parse_kwarg(k, v) for k, v in kwargs.items()]
        self.xpath = wrap(tag_name, conditions)

    def __repr__(self):
        return self.xpath

    @overload
    def __truediv__(self, other: str) -> Node: ...

    @overload
    def __truediv__(self, other: SubNode) -> SubNode: ...

    def __truediv__(self, other: str | SubNode):  # type: ignore[SubNode]
        if isinstance(other, str):
            new_node = self.__class__()
            new_node.xpath = f"{self}/{other}"
            return new_node

        elif isinstance(other, Node):
            new_node = other.__class__()
            new_node.xpath = f"{self}/{other}"
            return new_node

        return NotImplemented

    def __rtruediv__(self, other: str):
        if not isinstance(other, str):
            return NotImplemented

        new_node = self.__class__()
        new_node.xpath = f"{other}/{self}"

        return new_node

    @overload
    def __floordiv__(self, other: str) -> Node: ...

    @overload
    def __floordiv__(self, other: SubNode) -> SubNode: ...

    def __floordiv__(self, other: str | SubNode):  # type: ignore[SubNode]
        if isinstance(other, str):
            new_node = self.__class__()
            new_node.xpath = f"{self}//{other}"
            return new_node

        elif isinstance(other, Node):
            new_node = other.__class__()
            new_node.xpath = f"{self}//{other}"
            return new_node

        return NotImplemented

    def __rfloordiv__(self, other: str):
        if not isinstance(other, str):
            return NotImplemented

        new_node = self.__class__()
        new_node.xpath = f"{other}//{self}"

        return new_node

    def __getitem__(self, index: int | str):
        new_node = self.__class__()

        if isinstance(index, int):
            if index == 0:
                msg = "인덱스는 1부터 시작합니다."
                raise ValueError(msg)
            if index < 0:
                index = f"last(){index if index != -1 else ''}"

            if self.xpath.startswith(("/", "(")):
                new_node.xpath = f"({self})[{index}]"
            else:
                new_node.xpath = f"(//{self})[{index}]"

        elif isinstance(index, str):
            new_node.xpath = f"{self}[{index}]"

        else:
            return NotImplemented

        return new_node


class Any(Node): ...


class Div(Node): ...


class Span(Node): ...


class A(Node): ...


class Img(Node): ...


class Input(Node): ...


class Button(Node): ...


class Label(Node): ...


class Select(Node): ...


class Option(Node): ...


class Table(Node): ...


class Tr(Node): ...


class Td(Node): ...


class Th(Node): ...


class Ul(Node): ...


class Ol(Node): ...


class Li(Node): ...


class H1(Node): ...


class H2(Node): ...


class H3(Node): ...


class H4(Node): ...


class H5(Node): ...


class H6(Node): ...


class P(Node): ...


class Form(Node): ...


class Textarea(Node): ...


class IFrame(Node): ...


class Body(Node): ...


class Html(Node): ...


class Head(Node): ...


class Title(Node): ...


class Meta(Node): ...


class Link(Node): ...


class Style(Node): ...


class Script(Node): ...


class Noscript(Node): ...


class Br(Node): ...


class Hr(Node): ...


class Pre(Node): ...


class Code(Node): ...


class Strong(Node): ...


class Em(Node): ...


class B(Node): ...


class I(Node): ...


class U(Node): ...


class S(Node): ...


class Sub(Node): ...


class Sup(Node): ...


class Small(Node): ...


class Big(Node): ...


class Del(Node): ...


class Ins(Node): ...


class Blockquote(Node): ...


class Q(Node): ...


class Cite(Node): ...


class Dfn(Node): ...


class Abbr(Node): ...


class Address(Node): ...


class Var(Node): ...


Root = _ = ""

Parent = __ = ".."


if __name__ == "__main__":
    print((Div(2) / Div(3))[1])
    print(Div(2)[2])
