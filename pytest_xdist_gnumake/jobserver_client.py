from __future__ import annotations

import atexit
import os
import time
from abc import ABC, abstractmethod
from typing import Any


class JobserverClientABC(ABC):
    """
    Base for clients to job servers that limit the number of parallel processes
    """

    @abstractmethod
    def print_info(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def acquire(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def release(self) -> None:
        raise NotImplementedError()


class GnuMakeJobserverClient(JobserverClientABC):
    """
    Gnu make job server client (using the value of make -jN)
    """

    count = 0

    def print_info(self) -> None:
        print('pytest-xdist-gnumake using gnu make jobserver client')

    def __init__(self, worker_id: str | None, job_client: Any) -> None:
        self._worker_id = worker_id
        self._job_client = job_client
        self._token: str | None = None

    def acquire(self) -> None:
        if self._token:
            raise RuntimeError('token already acquired, this should never happen')
        while self._token is None:
            self._token = self._job_client.acquire()
            if not self._token:
                time.sleep(1)
            else:
                self.count += 1

    def release(self) -> None:
        if not self._token:
            return
        self.count -= 1
        self._job_client.release(self._token)
        self._token = None


class DummyJobserverClient(JobserverClientABC):
    """
    Dummy implementation that does not apply any limit
    """

    def __init__(self, info: str) -> None:
        self.info = info

    def print_info(self) -> None:
        print(f'pytest-xdist-gnumake using dummy job server: {self.info}')

    def acquire(self) -> None:
        pass

    def release(self) -> None:
        pass


def _init_jobserver_client() -> JobserverClientABC:
    try:
        import gnumake_tokenpool  # type: ignore
        job_client = gnumake_tokenpool.JobClient()
    except gnumake_tokenpool.tokenpool.NoJobServer:
        return DummyJobserverClient('no job server found')
    if not job_client._fdFifo:
        # the older way of passing open file descriptors does not work with pytest-xdist
        return DummyJobserverClient('only fifo job clients are supported')
    worker_id = os.environ.get('PYTEST_XDIST_WORKER')
    return GnuMakeJobserverClient(worker_id, job_client)


jobserver_client = _init_jobserver_client()


@atexit.register
def release_jobserver_token_at_exit():
    jobserver_client.release()
