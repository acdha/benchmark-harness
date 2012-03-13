from __future__ import absolute_import
import logging
import json
import os
import sys
import subprocess

from benchmark_harness.stats import display_stats


def discover_benchmarks(base_dir):
    base_dir = os.path.realpath(base_dir)

    for dirname, subdirs, filenames in os.walk(base_dir, topdown=True):
        if "benchmark.py" in filenames:
            yield os.path.join(base_dir, dirname)


def run_benchmarks(benchmarks, max_time=None, output_dir=None, includes=None, excludes=None,
                  continue_on_error=False, python_executable=None, env=None):

    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for benchmark_dir in benchmarks:
        name = os.path.basename(benchmark_dir)

        if name in excludes:
            continue

        if includes and name not in includes:
            continue

        if not output_dir:
            stderr = sys.stderr
        else:
            stderr = open(os.path.join(output_dir, "%s.stderr.log" % name), "wb")

        data = None

        try:
            data = run_benchmark(os.path.join(benchmark_dir, "benchmark.py"), env=None,
                                 max_time=max_time, python_executable=python_executable,
                                 stderr=stderr)
            if output_dir:
                stderr.close()
                with open(os.path.join(output_dir, "%s.json" % name), "wb") as f:
                    json.dump(data, f, indent=4)

            display_stats(name, data['times'])

            del data
        except RuntimeError as exc:
            logging.error("%s failed to complete: %s", name, exc)
            if not continue_on_error:
                raise


def run_benchmark(benchmark, env=None, max_time=None, python_executable=None,
                  stderr=None):
    # We'll split python_executable to allow values like 'coverage run'
    command = python_executable.split() + [benchmark]

    if max_time is not None:
        command += ['--max-time', str(max_time)]

    proc = subprocess.Popen(command, env=env, shell=False,
                            stdout=subprocess.PIPE, stderr=stderr)

    stdout, stderr = proc.communicate()

    if proc.returncode != 0:
        raise RuntimeError("%s returned %d", command, proc.returncode)

    data = json.loads(stdout)

    return data
