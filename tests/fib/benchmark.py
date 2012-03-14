from benchmark_harness import run_benchmark


def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)


def benchmark():
    """fib!"""
    fib(20)


run_benchmark(benchmark, meta={"title": "Everyone loves fib()"})
