import pytest
from typing import Any


from pytest_xdist_gnumake.jobserver_client import jobserver_client


def pytest_configure() -> None:
    jobserver_client.print_info()


def pytest_runtest_setup(item: Any) -> None:
    jobserver_client.acquire()


def pytest_runtest_teardown(item: Any) -> None:
    jobserver_client.release()

