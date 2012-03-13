from __future__ import absolute_import


def display_stats(name, times):
    print "%s: completed %d trials" % (name, len(times))
    print "\tMin: %0.3f" % min(times)
    print "\tMax: %0.3f" % max(times)
