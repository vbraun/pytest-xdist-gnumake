# pytest-xdist-gnumake

## Integration of pytest-xdist with GNU Make job server

Imagine you have a *Makefile* target that runs pytest in addition to
other tests:

	test: test-python test-mypy

    test-python:
	    pytest --numprocesses=8 my_app

	test-mypy:
	    mypy my_app
		
Conveniently, you just have to run ``make test`` to run both test
targets. To save time, you can even run ``make -j8 test`` (8 being the
number of cpu cores that you have at your disposal in this example) to
run everything in parallel. But what really happens now is that

* ``make`` knows it has 8 slots available, and starts pytest and mypy
  in parallel
  
* mypy runs on one cpu core

* pytest-xdist starts its own job server with 8 parallel workers

In effect you now are running 9 parallel processes, one more than
anticipated. This does not matter too much in this simplified example,
but if you have big testsuites then you would like to avoid that.

The solution to this issue is this pytest-xdist plugin, which makes
the pytest-xdist workers communicate with the GNU make jobserver to
avoid exceeding the total limit.


## Installation

Simply `pip install pytest-xdist-gnumake`, and the plugin should be
picked up automatically by pytest-xdist.


## Limitations

### Local execution only

The GNU jobserver uses the local file system (a fifo in ``/tmp``), so
this will not work with remote xdist workers.


### Needs modern make

Older make versions relied on passing open file descriptors to child
process, but pytest-xdist will always close those. You need 
GNU make >= 4.4 in order for the communication with the jobserver 
to work, that is, a version of make that uses the fifo jobserver. See
https://www.gnu.org/software/make/manual/html_node/POSIX-Jobserver.html
for details.

If your make version is too old then the plugin will print:

    $ pytest --numprocesses=8 my_app
    pytest-xdist-gnumake using dummy job server: no job server found

and tests will run as if the plugin was not installed. Otherwise, it
will print:

    $ pytest --numprocesses=8 my_app
    pytest-xdist-gnumake using gnu make jobserver client


## Acknowledgements

* GNU Make https://www.gnu.org/software/make/
* https://pytest.org and https://github.com/pytest-dev/pytest-xdist to
  parallelize Python testsuites
* https://github.com/milahu/gnumake-tokenpool to communicate with GNU Make
