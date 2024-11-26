class CannotFindElement(BaseException):
    def __init__(self, xpath):
        self.message = (
            f"\033[91m{xpath}\033[0m"  # \033[91m은 빨간색, \033[0m은 색상 리셋
        )
        super().__init__(self.message)
