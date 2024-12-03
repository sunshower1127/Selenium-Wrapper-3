"""xpath 에서 sw3식 변환 어떻게 할지

//는 없애기
/는 '' / 로 바꾸기
[]는 ()로 바꾸기
* -> Any
tag -> Tag

[] 안에 있는건 전부 and로 분해하고
)[] -> 이건 그냥 냅두고. (안에 last() 들어있으면 변환.)
일단 띄어쓰기를 전부 없애자. 없애고

괄호 냅두고
// 이거 없애고? 맨 앞에 있거나 앞에 괄호가 있거나 하면 없애고
그러니깐 바로 // 나오거나 )// 는 이제 교체.

태그의 특징을 봅시다.

//div
(//div(어쩌구))

div의 오른쪽에는 항상? -> [ 아니면 아무것도 없거나, ) 가 있거나 /가 있거나

"""

import re

from .args_parser import process_xpath


def xpath2sw3(xpath: str):
    # // 제거해주기
    xpath = re.sub(r"^//|\(//", "", xpath)

    # / 앞에 '' 붙여주기
    xpath = re.sub(r"\(/(?!/)", "(''/", xpath)

    xpath = re.sub(r"^\/(?!/)", "''/", xpath)

    # * -> any
    xpath = xpath.replace("*", "any")

    # 태그 대문자화
    # [a-zA-Z]+(?=[/)\[\s]|$) : 영어 단어를 찾고 뒤에 /, ), [, 공백이 오거나 문자열이 끝나는 경우
    xpath = re.sub(
        r"([a-zA-Z]+)(?=[/)\[]|\s*$)", lambda m: m.group(1).capitalize(), xpath
    )

    # 속성 없는 태그 뒤에 () 붙여주기
    # 대문자로 시작하는 영단어 뒤에 (가 없으면  ()추가
    xpath = re.sub(r"([A-Z][a-z]*)(?![\[\w])", r"\1()", xpath)

    def process_last_expression(match):
        content = match.group(1)

        # last() 표현식 처리
        # 1. 공백 제거된 버전도 처리하기 위해 모든 공백 제거
        content = content.replace(" ", "")

        if content == "last()":
            return "[-1]"

        # last() - 숫자 패턴 처리
        if "last()-" in content:
            # 숫자 추출
            number = int(content.split("-")[1])
            # 숫자에 1을 더해서 음수로 반환
            return f"[-{number + 1}]"

        return match.group(0)  # 매칭되지 않으면 원본 반환

    # last() 처리
    xpath = re.sub(r"\[(.*?)\]", process_last_expression, xpath)

    # 인자 처리
    def args(match):
        content = match.group(1)
        content = map(process_xpath, content.split(" and "))
        return f"({','.join(content)})"

    # 속성 있는 태그 처리
    xpath = re.sub(r"(?<!\))\[(.*?)\]", args, xpath)

    return xpath
