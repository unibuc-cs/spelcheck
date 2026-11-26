"""Lets the package be run as a program: `python -m speccheck ...`."""

from .cli import main

if __name__ == "__main__":  # not in the worker processes that cli.py starts for a project in parts
    main()
