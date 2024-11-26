from __future__ import annotations

from .xpath_parser import Expr, parse_arg, parse_kwarg, wrap


class Node:
    def __init__(self, *args: Expr | str, **kwargs: str | int | float | bool):  # noqa: PYI041
        tag_name = self.__class__.__name__.lower()
        conditions = [parse_arg(arg) for arg in args]
        conditions += [parse_kwarg(k, v) for k, v in kwargs.items()]
        self.xpath = wrap(tag_name, conditions)

    def __repr__(self):
        return self.xpath

    def __truediv__(self, other: str | Node):
        if not isinstance(other, (str, Node)):
            return NotImplemented

        new_node = Node()
        new_node.xpath = f"{self}/{other}"
        return new_node

    def __rtruediv__(self, other: str):
        if not isinstance(other, str):
            return NotImplemented
        new_node = Node()
        new_node.xpath = f"{other}/{self}"
        return new_node

    def __floordiv__(self, other: str | Node):
        if not isinstance(other, (str, Node)):
            return NotImplemented
        new_node = Node()
        new_node.xpath = f"{self}//{other}"
        return new_node

    def __rfloordiv__(self, other: str):
        if not isinstance(other, str):
            return NotImplemented
        new_node = Node()
        new_node.xpath = f"{other}//{self}"
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

# test
if __name__ == "__main__":
    print(Div() // Div(("data-id", "starts with", "1412"), id="main", class_="content"))
