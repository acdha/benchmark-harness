Welcome to Benchmark Harness's documentation!
=============================================

benchmark-harness is designed to make it easy to create simple suites of
standalone benchmarks while avoiding some common pitfalls in benchmarking. In
particular, benchmarks are always run for a specified duration to avoid
reporting anomalies due to background system activity, startup costs, garbage
collection or JIT activity, etc.

Quick Start
-----------

A simple benchmark looks like this:

.. literalinclude:: ../tests/fib/benchmark.py
   :linenos:


This script can be run directly::

    $ python fib/benchmark.pyfib/benchmark.py: completed 67 trials
    	Min: 0.007
    	Max: 0.010

Output can be redirected to get a full JSON record::

    {
        "meta": {
            "title": "Everyone loves fib()"
        },
        "times": [
            0.00791311264038086,
            …
        ]
    }


benchmark-harness installs the command-line :ref:`benchmark-harness` utility which
makes it easy to run many benchmarks if you organize them into a directory
containing one directory per benchmark with a benchmark.py file. If the above
file were saved to ``benchmarks/fib/benchmark.py``, a sample run would look
like this::

    $ benchmark-harness --benchmark-dir=benchmarks/
    fib: completed 59 trials
	Min: 0.008
	Max: 0.010


Contents
========

.. toctree::
   :maxdepth: 2
   :glob:

   *


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

