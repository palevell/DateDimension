#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# week_ids.py - Sunday, November 17, 2024
""" Comparing Week IDs from Python, PSQL and GNU date command against dim_date table """
__version__ = "0.1.0-dev13"

import calendar
import os
import sys
import time
from datetime import datetime, timedelta
from glob import glob
from os.path import exists, getmtime, join, lexists, realpath
from pathlib import Path

import sqlalchemy as sa
from environs import Env
from sqlalchemy import create_engine, text

__module__ = Path(__file__).resolve().stem
_basedir = Path(__file__).resolve().parent

env = Env(expand_vars=True)
env.read_env()


def main_new():
	c = calendar.Calendar(firstweekday=calendar.SUNDAY)

	print(calendar.prcal(_run_dt.year))
	return


def main():
	generate()
	return


def init():
	started = time.strftime(_iso_datefmt, _run_localtime)
	print(f"Run Start: {__module__} v{__version__} {started}")
	# Test database connection
	# insp = sa.inspect(engine)
	# insp.get_schema_names()
	return


def eoj():
	stop_ts = time.time()
	stop_localtime = time.localtime(stop_ts)
	stop_gmtime = time.gmtime(stop_ts)
	duration = timedelta(seconds=(stop_ts - _run_ts))
	print(f"Run Stop : {time.strftime(_iso_datefmt, stop_localtime)}  Duration: {duration}")
	return


def generate():
	this_date = datetime(1970, 1, 1).date()
	stop_date = datetime(2049, 12, 31).date()
	while this_date <= stop_date:
		print(this_date)
		this_date += timedelta(days=1)
		do_nothing()
	return


def generate1():
	""" Database Columns
	id, date_id, epoch, day_suffix, day_name, day_of_week, day_of_week_iso, day_of_month,
	day_of_quarter, day_of_year, week_id, week_id_iso, week_name, week_name_iso, week_of_month,
	week_of_year, week_of_year_id, week_of_year_iso, week_of_year_iso_id, month_of_year,
	month_name, month_name_abbreviated, quarter_of_year, quarter_name, quarter_id, yyyy,
	first_day_of_week, last_day_of_week, first_day_of_week_iso, last_day_of_week_iso,
	first_day_of_month, last_day_of_month, first_day_of_quarter, last_day_of_quarter,
	first_day_of_year, last_day_of_year, mmyyyy, mmddyyyy, weekend_indr
	"""
	# In Python, 0 = Monday
	day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday",]
	c = calendar.Calendar(firstweekday=calendar.SUNDAY)
	for yyyy in range(1970, 2050):
		for mm in range(1, 13):
			for y, m, d, dow in c.itermonthdays4(yyyy, mm):
				this_date = datetime(y, m, d).date()
				week, iso_week = this_date.strftime("%U %W").split()
				print(this_date, week, iso_week, day_names[dow])
				if _run_dt.date() == this_date:
					do_nothing()

	return


def do_nothing():
	pass


if __name__ == '__main__':
	_run_ts = time.time()
	_run_dt = datetime.fromtimestamp(_run_ts).astimezone()
	_run_localtime = time.localtime(_run_ts)
	_run_gmtime = time.gmtime(_run_ts)
	_run_ymd = time.strftime("%Y%m%d", _run_localtime)
	_run_hms = time.strftime("%H%M%S", _run_localtime)
	_run_ymdhms = f"{_run_ymd}_{_run_hms}"
	_iso_datefmt = "%Y-%m-%d %H:%M:%S%z"

	# Database
	_db_uri = env("SQLALCHEMY_DATABASE_URI")
	print(f"DB_URL: {_db_uri}")
	engine = create_engine(_db_uri)

	init()
	main()
	eoj()
