# Selenium Wrapper 3

### Installation

[![PyPI - Package](https://img.shields.io/badge/Selenium--Wrapper--3-PyPI-blue?logo=pypi&logoColor=white&style=for-the-badge)](https://pypi.org/project/Selenium-Wrapper-3/)

```shell
pip install selenium-wrapper-3
```

**ver1** - [Enhanced Selenium](https://github.com/sunshower1127/Enhanced-Selenium)

**ver2** - [Sw Selenium](https://github.com/sunshower1127/Sw-Selenium)

---

## Projects using Selenium Wrapper 3

[Lecture-Automation-with-Selenium](https://github.com/sunshower1127/Lecture-Automation-with-Selenium)

---

## Cli 지원

Selenium Wrapper 3의 Expression과 Xpath Expression을 양방향 번역해줌.

```shell
sw3
# 안되면
python -m selenium_wrapper_3
```

### Example Code

```python

from time import sleep

from selenium_wrapper_3.node import *
from selenium_wrapper_3.util import *


url("https://cyberuniv.com/login")

id, pw = "ID", "PW"

send_keys( Input(name="userid"), [id, "\t", pw, "\n"] )

click( Button(text="MyPage") / Parent )

with frame( IFrame(id="my-iframe") ):
    courses = Div(class_="course-header")

    courses_to_do = poll(
        lambda: [
            course
            for course in populate(courses)
            if text(course // A()) != "0"
        ]
    )


for course in courses_to_do:

    url("https://cyberuniv.com/mypage")

    with frame( IFrame(id="my-iframe") ):

        click( course // Button() )

        lectures = course // ( Div(2) / Div( ("text", "in", ["online", "supplement"]) ) )[2]

        sleep(2)

        titles = [
            text(lecture / A())
            for lecture in populate(lectures)
            if count( lecture / I( ("video-lecture", "in", "class") ) )
        ]

        print("Online Classes to do")
        print(*titles, sep="\n")

```

---
