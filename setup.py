#!/usr/bin/env python3

"""Setup script"""

from setuptools import setup, find_packages

setup(
    name="adventure",
    version="0.0.0",
    author="Vladislav Kosukhin",
    author_email="vladlenkos@yandex.ru",
    url="https://github.com/Gramotei-vlad/adventure",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "pygame",
        "pyganim"
    ],
    setup_requires=[
        "pytest-runner",
        "pytest-pylint",
        "pytest-pycodestyle",
        "pytest-pep257",
        "pytest-cov",
    ],
    tests_require=[
        "pytest",
        "pylint",
        "pycodestyle",
        "pep257",
    ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ]
)
