from __future__ import absolute_import

import argparse

# timeit uses either time.time() or time.clock() depending on which is more
# accurate on the current platform:
from timeit import default_timer as time_f

try:
    import cProfile as profile
except ImportError:
    import profile

from benchmark_harness.utils import format_output

benchmark_parser = argparse.ArgumentParser()
benchmark_parser.add_argument('--max-time', type=float, default=0.5)
benchmark_parser.add_argument('--profile-file', default=None)


@format_output
def run_benchmark(benchmark, setup=None, max_time=None, handle_argv=True, meta={}):
    """
    Run a benchmark a few times and report the results.

    Arguments:

        benchmark
            The benchmark callable. ``run_benchmark`` will time
            the executation of this function and report those times
            back to the harness. However, if ``benchmark`` returns
            a value, that result will reported instead of the
            raw timing.

        syncdb
            If True, a syncdb will be performed before running
            the benchmark.

        setup
            A function to be called before running the benchmark
            function(s).

        max_time
            The number of seconds to run the benchmark function. If not given
            and if ``handle_argv`` is ``True`` this'll be automatically
            determined from the ``--max_time`` flag.

        handle_argv
            ``True`` if the script should handle ``sys.argv`` and configure
            itself from command-line arguments

        meta
            Key/value pairs to be returned as part of the benchmark results.
    """
    if handle_argv:
        args = benchmark_parser.parse_args()
        max_time = max_time or args.max_time

    if setup:
        setup()

    cumulative_time = 0.0
    times = []

    while cumulative_time < max_time:
        start = time_f()

        if args.profile_file is not None:
            loc = locals().copy()
            profile.runctx('benchmark_result = benchmark()', globals(), loc, args.profile_file)
            benchmark_result = loc['benchmark_result']
        else:
            benchmark_result = benchmark()

        elapsed = benchmark_result or time_f() - start
        cumulative_time += elapsed

        times.append(elapsed)

    return {"times": times, "meta": meta}


@format_output
def run_comparison_benchmark(benchmark_a, benchmark_b, setup=None, max_time=None, handle_argv=True, meta={}):
    """
    Benchmark the difference between two functions.

    Arguments are as for ``run_benchmark``, except that this takes 2
    benchmark functions, an A and a B, and reports the difference between
    them.

    For example, you could use this to test the overhead of an ORM query
    versus a raw SQL query -- pass the ORM query as ``benchmark_a`` and the
    raw query as ``benchmark_b`` and this function will report the
    difference in time between them.

    For best results, the A function should be the more expensive one
    (otherwise djangobench will report results like "-1.2x slower", which
    is just confusing).
    """
    if handle_argv:
        args = benchmark_parser.parse_args()
        max_time = max_time or args.max_time

    if setup:
        setup()

    elapsed = 0.0
    times = []

    while elapsed < max_time:
        start_a = time_f()
        result_a = benchmark_a()
        result_a = result_a or time_f() - start_a

        elapsed += result_a

        start_b = time_f()
        result_b = benchmark_b()
        result_b = result_b or time_f() - start_b

        times.append(result_a - result_b)

    return {"times": times, "meta": meta}
