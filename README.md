# Selenium Wrapper 3

![PyPI](https://img.shields.io/pypi/v/Selenium-Wrapper-3.svg)

**ver1** - [Enhanced Selenium](https://github.com/sunshower1127/Enhanced-Selenium)

**ver2** - [Sw Selenium](https://github.com/sunshower1127/Sw-Selenium)

---

## Projects using Selenium Wrapper 3

[Lecture-Automation-with-Selenium](https://github.com/sunshower1127/Lecture-Automation-with-Selenium)

---

## Quick Start

프로젝트 설명...

### Installation

```shell
pip install selenium-wrapper-3
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

    sleep(3)

    courses_to_do = [
        course
        for course in populate(courses)
        if text(course // A()) != "0"
    ]

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
