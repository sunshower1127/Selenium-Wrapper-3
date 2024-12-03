from setuptools import find_packages, setup

setup(
    name="Selenium-Wrapper-3",
    version="1.2.1",
    description="Selenium Wrapper 3",
    long_description="https://github.com/sunshower1127/Selenium-Wrapper-3",
    keywords=["selenium", "wrapper", "webdriver", "python", "selenium-wrapper"],
    packages=find_packages(),
    install_requires=[
        "selenium",
        "pyperclip",
    ],
    entry_points={
        "console_scripts": [
            "sw3=selenium_wrapper_3:main",
        ],
    },
    python_requires=">=3.9",
    author="Sunwoo Kim",
    author_email="sunshower1127@gmail.com",
)
