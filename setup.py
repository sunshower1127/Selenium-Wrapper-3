from setuptools import find_packages, setup

setup(
    name="Selenium-Wrapper-3",
    version="1.0",
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
