import os
from setuptools import setup, find_packages

setup(name = "benchmark-harness",
    version = "0.0.1",
    description = "Generic framework for writing simple benchmark suites",
    url = 'http://github.com/acdha/benchmark-harness',
    license = 'BSD',
    author = 'Chris Adams',
    author_email = 'chris@improbable.org',
    packages = find_packages(),
    include_package_data = True,
    zip_safe=True,
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Testing',
        'Topic :: System :: Benchmark'
    ],
    install_requires = ['argparse'],

    entry_points = {
        'console_scripts': ['benchmark-harness = benchmark_harness.main:main']
    }
)
