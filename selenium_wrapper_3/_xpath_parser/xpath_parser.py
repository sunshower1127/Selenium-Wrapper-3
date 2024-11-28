from __future__ import annotations

from typing import Literal, Union

pairs = {
    "class_": "@class",
    "text": "text()",
    "position": "position()",
}

ops = [
    "in",
    "not in",
    "startswith",
    "endswith",
    "not startswith",
    "not endswith",
]

Operator = Literal[
    "=",
    "!=",
    ">",
    ">=",
    "<",
    "<=",
    "in",
    "not in",
    "starts with",
    "ends with",
    "not starts with",
    "not ends with",
]

Operand = Union[str, int, float, list]
Expr = tuple[Operand, Operator, Operand]


def parse_kwarg(key, value: str | float | bool):
    new_key = pairs.get(key, f"@{key}")

    if isinstance(value, str):
        return f"{new_key}='{value}'"
    elif isinstance(value, (int, float)):
        return f"{new_key}={value}"
    elif isinstance(value, bool):
        if value:
            return new_key
        else:
            return f"not({new_key})"
    return None


def quote_if_str(v):
    if isinstance(v, str):
        return f"'{v}'"
    return v


def parse_attr(v):
    if not isinstance(v, str):
        raise TypeError
    return pairs.get(v, f"@{v}")


def parse_arg(expr: Expr | str):  # noqa: C901, PLR0911
    # 속성이 존재하는지만 체크하는 경우
    if isinstance(expr, str):
        return f"'{parse_attr(expr)}'"

    op1, operator, op2 = expr

    if operator in ("in", "not in") and isinstance(op2, str):
        op2 = parse_attr(op2)
    else:
        op1 = parse_attr(op1)

    if operator in ("=", "!=", ">", ">=", "<", "<="):
        op2 = quote_if_str(op2)
        return f"{op1}{operator}{op2}"

    if operator == "in":
        if isinstance(op2, str):
            # 어떤거 in 속성 -> contains(속성, a)
            return f"contains({op2},{quote_if_str(op1)})"
        elif isinstance(op2, (tuple, list)):
            # 속성 in (a, b, c) -> (속성=a or 속성=b or 속성=c)
            return " or ".join(f"{op1}={quote_if_str(v)}" for v in op2)

    elif operator == "not in":
        if isinstance(op2, str):
            # 어떤거 not in 속성 -> not(contains(속성, a))
            return f"not(contains({op2},{quote_if_str(op1)})"
        elif isinstance(op2, list):
            # 속성 not in (a, b, c) -> not(속성=a or 속성=b or 속성=c)
            return " and ".join(f"{op1}!={quote_if_str(v)}" for v in op2)

    elif operator in ("starts with", "ends with"):
        return f"{operator.replace(' ', '-')}({op1},{quote_if_str(op2)})"

    elif operator in ("not starts with", "not ends with"):
        return f"not({operator[4:].replace(' ', '-')}({op1},{quote_if_str(op2)}))"

    raise ValueError


def wrap(tagname, conditions):
    if tagname == "any":
        tagname = "*"
    if not conditions:
        return tagname

    return f"{tagname}[{' and '.join(conditions)}]"


if __name__ == "__main__":
    print(parse_arg("text"))
    print(parse_arg(("text", ">", 1)))
    print(parse_arg(("hi", "in", "class")))
    print(parse_arg(("class", "in", ["a", "b", "c"])))
    print(parse_arg(("class", "not in", "a")))
    print(parse_arg(("class", "not in", ["a", "b", "c"])))
    print(parse_arg(("class", "starts with", "a")))
    print(parse_arg(("class", "ends with", "a")))
    print(parse_arg(("class", "not starts with", "a")))
