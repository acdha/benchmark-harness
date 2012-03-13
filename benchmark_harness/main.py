from __future__ import absolute_import
import argparse
import os
import sys

from benchmark_harness.suite import discover_benchmarks, run_benchmarks


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-time', type=float, default=0.5,
                        help='Number of seconds to run each benchmark (default=%(default)s)')
    parser.add_argument('--output-dir', default=None, metavar='PATH',
                        help='Directory to record JSON results',)
    parser.add_argument('--benchmark-dir', metavar='PATH',
                        help='Directory to inspect for benchmarks')
    parser.add_argument('include', metavar='name', default=None,
                        help="Benchmarks to be run by name. Defaults to all",
                        nargs='*')
    parser.add_argument('exclude', metavar='name', default=None,
                        help="Don't run the specified benchmarks by name",
                        nargs='*')
    parser.add_argument('--continue-on-error', action='store_true',
                        help="Don't halt when a benchmark fails")
    parser.add_argument('--python-executable', metavar='PATH',
                        default=sys.executable,
                        help='Python binary for tests. Default: %(default)s')

    args = parser.parse_args()
    if not args.benchmark_dir:
        # FIXME: look under current directory
        parser.error("You must specify the benchmark directory!")

    benchmarks = discover_benchmarks(os.path.expanduser(args.benchmark_dir))

    run_benchmarks(benchmarks, max_time=args.max_time, output_dir=args.output_dir, includes=args.include, excludes=args.exclude,
                  continue_on_error=args.continue_on_error, python_executable=args.python_executable)

if __name__ == '__main__':
    import pdb
    try:
        main()
    except:
        pdb.post_mortem()
        raise