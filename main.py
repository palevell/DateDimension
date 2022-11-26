#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# main.py - Saturday, November 26, 2022
""" DocString goes here. """
__version__ = '0.1.0'

import os, sys
from datetime import datetime, timedelta, timezone
from glob import glob
from os.path import exists, expanduser, join

__MODULE__ = os.path.splitext(os.path.basename(__file__))[0]


def main():
    return


def init():
    print("Run Start: %s" % _run_dt)
    return


def eoj():
    stop_dt = datetime.now().astimezone().replace(microsecond=0)
    duration = stop_dt.replace(microsecond=0) - _run_dt.replace(microsecond=0)
    print("Run Stop : %s  Duration: %s" % (stop_dt, duration))
    return


def do_nothing():
    pass


if __name__ == '__main__':
    _run_dt = datetime.now().astimezone().replace(microsecond=0)
    _run_utc = _run_dt.astimezone(timezone.utc).replace(tzinfo=None)
    _fdate = _run_dt.strftime("%Y-%m-%d")
    _fdatetime = _run_dt.strftime("%Y%m%d_%H%M%S")

    init()
    main()
    eoj()
