import re


def process_comparison(text):
    """부등호가 있는 경우를 처리"""
    pattern = r"(@\w+)\s*([<>])\s*(\w+)"
    return re.sub(pattern, r"('\1', '\2', \3)", text)


def remove_empty_parentheses(text):
    """빈 괄호 제거"""
    return re.sub(r"(\w+)\(\)", r"\1", text)


def process_class_attribute(text):
    """@class를 class_로 변환"""
    return re.sub(r"@class\s*=", "class_=", text)


def process_contains(text):
    """.contains 함수 처리"""
    # 다중 contains (OR 조건) 먼저 처리
    pattern_multiple = r'contains\((@\w+),\s*[\'"](\w+)[\'"]\)\s*or\s*contains\(\1,\s*[\'"](\w+)[\'"]\)'
    text = re.sub(pattern_multiple, r"(['\2', '\3'], 'in', '\1')", text)

    # 단일 contains
    pattern_single = r'contains\((@\w+),\s*[\'"](\w+)[\'"]\)'
    text = re.sub(pattern_single, r"('\2', 'in', '\1')", text)

    return text


def process_starts_with(text):
    """starts-with 함수 처리"""
    # 다중 (OR 조건) 먼저 처리
    pattern_multiple = r'starts-with\((@\w+),\s*[\'"](\w+)[\'"]\)\s*or\s*starts-with\(\1,\s*[\'"](\w+)[\'"]\)'
    text = re.sub(pattern_multiple, r"('\1', 'starts with', ['\2', '\3'])", text)

    # 단일
    pattern_single = r'starts-with\((@\w+),\s*[\'"](\w+)[\'"]\)'
    text = re.sub(pattern_single, r"('\1', 'starts with', '\2')", text)

    return text


def process_ends_with(text):
    """ends-with 함수 처리"""
    # 다중 (OR 조건) 먼저 처리
    pattern_multiple = r'ends-with\((@\w+),\s*[\'"](\w+)[\'"]\)\s*or\s*ends-with\(\1,\s*[\'"](\w+)[\'"]\)'
    text = re.sub(pattern_multiple, r"('\1', 'ends with', ['\2', '\3'])", text)

    # 단일
    pattern_single = r'ends-with\((@\w+),\s*[\'"](\w+)[\'"]\)'
    text = re.sub(pattern_single, r"('\1', 'ends with', '\2')", text)

    return text


def process_equals_or(text):
    """= 'a' or = 'b' 패턴 처리"""
    # 마지막 괄호 제거하고 패턴 수정
    pattern = r'@(\w+)\s*=\s*[\'"](\w+)[\'"]\s*or\s*@\1\s*=\s*[\'"](\w+)[\'"]'
    return re.sub(pattern, r"('\1', 'in', ['\2', '\3'])", text)


def process_at_symbol(text):
    """@ 심볼 제거 (마지막에 실행)"""
    return re.sub(r"@(\w+)", r"\1", text)


def process_not_function(text):
    """not() 함수 처리"""
    pattern = r"not\((.*?)\)"

    def replace_operator(match):
        inner_content = match.group(1)
        # 'in' -> 'not in'
        inner_content = inner_content.replace("'in'", "'not in'")
        # 'starts with' -> 'not starts with'
        inner_content = inner_content.replace("'starts with'", "'not starts with'")
        # 'ends with' -> 'not ends with'
        inner_content = inner_content.replace("'ends with'", "'not ends with'")
        return inner_content

    return re.sub(pattern, replace_operator, text)


def process_xpath(text):
    """모든 변환을 순서대로 적용"""
    text = process_comparison(text)
    text = remove_empty_parentheses(text)
    text = process_class_attribute(text)
    text = process_contains(text)
    text = process_starts_with(text)
    text = process_ends_with(text)
    text = process_equals_or(text)
    text = process_not_function(text)  # not() 처리 추가
    text = process_at_symbol(text)  # 마지막에 실행
    return text


if __name__ == "__main__":
    # 테스트
    test_cases = [
        "@a='b'",
        "@a <= 2",
        "text() = 'a'",
        "@class = 'a'",
        "contains(@a, 'b')",
        "starts-with(@class, 'sdfs sdf')",
        "ends-with(@a, 'b')",
        "contains(@a, 'b') or contains(@a, 'c')",
        "starts-with(@a, 'b') or starts-with(@a, 'c')",
        "ends-with(@a, 'b') or ends-with(@a, 'c')",
        "@a = 'b' or @a = 'c'",
        "not(contains(@a, 'b'))",
        "not(starts-with(@a, 'b'))",
        "not(ends-with(@a, 'b'))",
        "not(contains(@a, 'b') or contains(@a, 'c'))",
    ]

    for test in test_cases:
        result = process_xpath(test)
        print(f"입력: {test}")
        print(f"출력: {result}")
        print("-" * 30)
