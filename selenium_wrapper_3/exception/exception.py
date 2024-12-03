class SeleniumWrapperException(BaseException): ...


class CannotFindElement(SeleniumWrapperException):
    def __init__(self, xpath):
        self.message = (
            f"\033[91m{xpath}\033[0m"  # \033[91m은 빨간색, \033[0m은 색상 리셋
        )
        super().__init__(self.message)


class PollTimeout(SeleniumWrapperException):
    def __init__(self, message: str):
        self.message = f"\033[91m{message}\033[0m"  # 빨간색 메시지
        super().__init__(self.message)
