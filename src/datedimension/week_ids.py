#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# week_ids.py - Sunday, November 17, 2024
""" Comparing Week IDs from Python, PSQL and GNU date command against dim_date table """
__version__ = "0.1.0-dev81"

import calendar
import datetime
import jsons
import os
import pandas as pd
import sys
import time
from datetime import datetime, timedelta, timezone
from glob import glob
from os.path import exists, getmtime, join, lexists, realpath
from pathlib import Path

import sqlalchemy as sa
from dateutil.relativedelta import relativedelta
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
	calendar_1()
	# inspect_weeks()
	# psql_week_number(datetime(2023, 12, 31))
	# psql_week_number(datetime(2024, 1, 1))
	return


def init():
	started = time.strftime(_iso_datefmt, _run_localtime)
	print(f"Run Start: {__module__} v{__version__} {started}")
	# Test database connection
	# insp = sa.inspect(engine)
	# insp.get_schema_names()

	columns = """
	date_id, epoch, day_suffix, day_name, day_abbr, day_of_week, day_of_week_iso, day_of_month,
	day_of_quarter, day_of_year, week_id, week_id_iso, week_name, week_name_iso, week_of_month,
	week_of_year, week_of_year_id, week_of_year_iso, week_of_year_iso_id, month_of_year,
	month_name, month_abbr, quarter_of_year, quarter_name, quarter_id, yyyy,
	first_day_of_week, last_day_of_week, first_day_of_week_iso, last_day_of_week_iso,
	first_day_of_month, last_day_of_month, first_day_of_quarter, last_day_of_quarter,
	first_day_of_year, last_day_of_year, mmyyyy, mmddyyyy, weekend_indr
	""".replace(
		",", ""
	).split()
	return


def eoj():
	stop_ts = time.time()
	run_stop = time.strftime(_iso_datefmt, time.localtime(stop_ts))
	stop_gmtime = time.gmtime(stop_ts)
	duration = timedelta(seconds=(stop_ts - _run_ts))
	print(f"Run Stop : {run_stop}  Duration: {duration}")
	return


def do_nothing():
	pass


def calendar_1():
	y = 2024
	month_count = 0
	week_count = 0
	full_week_count = 0
	day_count = 0
	seen_weeks = []
	seen_days = []
	c = calendar.Calendar(firstweekday=calendar.SUNDAY)
	# Width of three means one quarter per row
	for q, months in enumerate(c.yeardatescalendar(year=y, width=3)):
		for m, month in enumerate(months):
			month_count += 1
			for w, week in enumerate(month):
				if week not in seen_weeks:
					week_count += 1
					seen_weeks.append(week)
				else:
					do_nothing()
				for d, day in enumerate(week):
					if day not in seen_days:
						day_count += 1
						seen_days.append(day)
					else:
						do_nothing()
					dt = date2datetime(day)

					num_strings = 4
					parts = dt.strftime("%A %a %B %b %w %u %d %j %U %W").split()
					# Extract string values
					day_name, day_abbr, month_name, month_abbr = parts[:num_strings]
					# Extract integers
					day_of_week, day_of_week_iso, day_of_month, day_of_year, \
						week_of_year, week_of_year_iso = [int(x) for x in parts[num_strings:]]

					columns = [
						f"Q{q + 1}",
						f"M{month_count:02d}",
						f"W{week_count:02d}",
						f"{day_count:3d} {day}",

						f"{day_abbr}, {month_abbr} {day_of_month:02d}, {day.year}",
						f"{day_of_year:3d}",
						f"W{week_of_year:02d}",
						f"W{week_of_year_iso:02d}",
					]
					# print(f"Q{q+1} M{month_count:02d} W{week_count:02d} {day_count:3d} {day}")
					print(" ".join(columns))
					do_nothing()
	return


def date2datetime(date_value: datetime.date) -> datetime:
	y = date_value.year
	m = date_value.month
	d = date_value.day
	dt = datetime(y, m, d)
	return dt


def inspect_weeks():
	from_date = (_run_dt - timedelta(days=15)).date()
	thru_date = (_run_dt + timedelta(days=15)).date()
	sql = "SELECT * FROM dim_date WHERE date_id BETWEEN :from_date AND :thru_date;"
	params = {"from_date": from_date,
			  "thru_date": thru_date
	}
	column_names = []
	db_dict_rows = []
	py_dict_rows = []
	rows = []

	with engine.connect() as conn:
		result = conn.execute(text(sql), params)
		column_names = list(result.keys())
		rows = result.fetchall()
		db_dict_rows = [dict(zip(column_names, row)) for row in rows]
		# py_dict = [{f"{x}": "" for x in column_names}]
		for cn in column_names:
			if cn in ["id", "date_id"] or cn.startswith("week") or cn.endswith("name"):
				print(cn, end=", ")
		print("")
		do_nothing()
	df = pd.DataFrame(rows)
	print(df.head(3))
	for dr in db_dict_rows:
		py_dict = {"id": dr["id"], "date_id": dr["date_id"]}
		# Assign Python values
		dt = date2datetime(dr["date_id"])
		# First four items are strings, followed by integers
		num_strings = 4
		parts = dt.strftime("%A %a %B %b %w %u %d %j %U %W").split()
		# Extract string values
		day_name, day_abbr, month_name, month_abbr = parts[:num_strings]
		# Extract integers
		day_of_week, day_of_week_iso, day_of_month, day_of_year, \
			week_of_year, week_of_year_iso = [int(x) for x in parts[num_strings:]]
		# Assign compound values
		yyyy = str(dt.year)
		week_id = f"{yyyy}W{week_of_year}"
		week_id_iso = f"{yyyy}W{week_of_year_iso}"
		week_name = f"W{week_of_year}"
		week_name_iso = f"W{week_of_year_iso}"
		# ToDo: Extras
		week_of_month = week_number_of_month(dt)
		# Add strings to dictionary
		py_dict.update({"day_name": day_name})
		py_dict.update({"day_abbr": day_abbr})
		py_dict.update({"month_name": month_name})
		py_dict.update({"month_abbr": month_abbr})
		# Add integers to dictionary
		py_dict.update({"day_of_week": day_of_week})
		py_dict.update({"day_of_week_iso": day_of_week_iso})
		py_dict.update({"day_of_month": day_of_month})
		py_dict.update({"day_of_year": day_of_year})
		py_dict.update({"week_of_year": week_of_year})
		py_dict.update({"week_of_year_iso": week_of_year_iso})
		# Add compound values to dictionary
		py_dict.update({"week_id": week_id})
		py_dict.update({"week_id_iso": week_id_iso})
		py_dict.update({"week_name": week_name})
		py_dict.update({"week_name_iso": week_name_iso})
		py_dict.update({"week_of_month": week_of_month})

		# Compare values
		for key in dr.keys():
			if key.startswith("week") or key.endswith("name"):
				print(f"DB: {key}: {dr[key]}")
				if dr[key] != py_dict[key]:
					do_nothing()
				else:
					do_nothing()
			else:
				py_dict.update({key: None})
		print("")
		# py_dict_rows.append(py_dict)
	return


def generate2():
	dt = datetime(1970, 1, 1, tzinfo=timezone.utc)
	# stop_date = datetime(2049, 12, 31)
	stop_date = dt + timedelta(days=21)
	while dt <= stop_date:
		print(dt)
		id = int(dt.strftime("%Y%m%d"))
		date_id = dt.strftime("%Y-%m-%d")
		epoch = dt.timestamp()
		day_suffix = ordinal_suffix(dt)
		day_name = dt.strftime("%A")
		day_abbr = ""
		day_of_week = -1
		day_of_week_iso = -1
		day_of_month = -1
		day_of_quarter = -1
		day_of_year = -1
		week_id = -1
		week_id_iso = -1
		week_name = ""
		week_name_iso = ""
		week_of_month = -1
		week_of_year = -1
		week_of_year_id = ""
		week_of_year_iso = -1
		week_of_year_iso_id = ""
		month_of_year = -1
		month_name = ""
		month_abbr = ""
		quarter_of_year = -1
		quarter_name = ""
		quarter_id = ""
		yyyy = -1
		first_day_of_week = ""
		last_day_of_week = ""
		first_day_of_week_iso = ""
		last_day_of_week_iso = ""
		first_day_of_month = ""
		last_day_of_month = ""
		first_day_of_quarter = ""
		last_day_of_quarter = ""
		first_day_of_year = ""
		last_day_of_year = ""
		mmyyyy = ""
		mmddyyyy = ""
		weekend_indr = ""

		# ToDo: Consolidate calls to strftime()
		# First four items are strings, followed by integers
		num_strings = 4
		parts = dt.strftime("%A %a %B %b %w %u %d %j %U %W").split()
		print(parts)
		# Extract string values
		day_name, day_abbr, month_name, month_abbr = parts[:num_strings]
		# Extract integers
		day_of_week, day_of_week_iso, day_of_month, day_of_year, \
			week_of_year, week_of_year_iso = [int(x) for x in parts[num_strings:]]
		do_nothing()

		dt += timedelta(days=1)
	return


def generate():
	"""Database Columns
	id, date_id, epoch, day_suffix, day_name, day_of_week, day_of_week_iso, day_of_month,
	day_of_quarter, day_of_year, week_id, week_id_iso, week_name, week_name_iso, week_of_month,
	week_of_year, week_of_year_id, week_of_year_iso, week_of_year_iso_id, month_of_year,
	month_name, month_abbr, quarter_of_year, quarter_name, quarter_id, yyyy,
	first_day_of_week, last_day_of_week, first_day_of_week_iso, last_day_of_week_iso,
	first_day_of_month, last_day_of_month, first_day_of_quarter, last_day_of_quarter,
	first_day_of_year, last_day_of_year, mmyyyy, mmddyyyy, weekend_indr
	"""
	start_date = datetime(2024, 11, 1, tzinfo=timezone.utc)
	stop_date = start_date + timedelta(days=21)

	# In Python, 0 = Monday
	day_names = [
		"Monday",
		"Tuesday",
		"Wednesday",
		"Thursday",
		"Friday",
		"Saturday",
		"Sunday",
	]
	c = calendar.Calendar(firstweekday=calendar.SUNDAY)
	for cal_year in range(start_date.year, stop_date.year + 1):
		for mm in range(1, 13):
			for y, m, d, dow in c.itermonthdays4(cal_year, mm):
				dt = datetime(y, m, d, tzinfo=timezone.utc)
				epoch = dt.timestamp()
				if epoch < start_date.timestamp() or epoch > stop_date.timestamp():
					continue
				id = int(dt.strftime("%Y%m%d"))
				date_id = dt.strftime("%Y-%m-%d")
				day_suffix = ordinal_suffix(dt)
				day_name = ""
				day_abbr = ""
				day_of_week = -1
				day_of_week_iso = -1
				day_of_month = -1
				day_of_quarter = -1
				day_of_year = -1
				week_id = -1
				week_id_iso = -1
				week_name = ""
				week_name_iso = ""
				week_of_month = -1
				week_of_year = -1
				week_of_year_id = ""
				week_of_year_iso = -1
				week_of_year_iso_id = ""
				month_of_year = -1
				month_name = ""
				month_abbr = ""
				quarter_of_year = -1
				quarter_name = ""
				quarter_id = ""
				yyyy = -1
				first_day_of_week = ""
				last_day_of_week = ""
				first_day_of_week_iso = ""
				last_day_of_week_iso = ""
				first_day_of_month = ""
				last_day_of_month = ""
				first_day_of_quarter = ""
				last_day_of_quarter = ""
				first_day_of_year = ""
				last_day_of_year = ""
				mmyyyy = ""
				mmddyyyy = ""
				weekend_indr = ""

				num_strings = 4
				parts = dt.strftime("%A %a %B %b %w %u %d %j %U %W").split()
				# Extract string values
				day_name, day_abbr, month_name, month_abbr = parts[:num_strings]
				# Extract integers
				day_of_week, day_of_week_iso, day_of_month, day_of_year, \
					week_of_year, week_of_year_iso = [int(x) for x in parts[num_strings:]]
				week_name = f"W{week_of_year}"
				week_name_iso = f"W{week_of_year_iso}"
				week_id = f"{y}{week_name}"
				week_id_iso = f"{y}{week_name_iso}"
				week_of_year_id = f"{y}-{week_name}-{day_of_week}"
				week_of_year_iso_id = f"{y}-{week_name_iso}-{day_of_week_iso}"
				print(dt, week_id, week_id_iso, week_name, week_name_iso, week_of_year_id, week_of_year_iso_id, " ".join(parts))

				db_columns = ["week_id", "week_id_iso", "week_name", "day_name", "week_name_iso",
							  "week_of_year_id", "week_of_year_iso_id"]
				db_cols = ",".join(db_columns)
				sql = f"SELECT {db_cols} FROM dim_date WHERE date_id = :date_id"
				params = {"date_id": date_id}
				with engine.connect() as conn:
					result = conn.execute(text(sql), params)
					db_week_id, db_week_id_iso, db_week_name, db_day_name, db_week_name_iso, \
						db_week_of_year_id, db_week_of_year_iso_id = result.fetchone()
					print(" " * 25 , db_week_id, db_week_id_iso, db_week_name, db_day_name, \
						  db_week_name_iso, db_week_of_year_id, db_week_of_year_iso_id)

				if _run_dt.date() == dt.date():
					do_nothing()
	return


def ordinal_suffix(dt: datetime):
	# return "%d%s" % (dt.day, 'th' if 4 <= dt.day <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(dt.day % 10, 'th'))
	return "%s" % (
		"th"
		if 4 <= dt.day <= 20
		else {1: "st", 2: "nd", 3: "rd"}.get(dt.day % 10, "th")
	)


def psql_week_number(date_value: datetime.date):
	print(date_value)
	params = {"date_value": date_value}
	sql = """
		SELECT
		:date_value AS date_id,
		TO_CHAR(:date_value, 'TMDay') AS day_name,
		EXTRACT(DOW FROM :date_value) AS day_of_week,
		EXTRACT(ISODOW FROM :date_value) AS day_of_week_iso,
		EXTRACT(WEEK FROM :date_value + INTERVAL '1 day') AS week_of_year,
		EXTRACT(WEEK FROM :date_value) AS week_of_year_iso,
		EXTRACT(YEAR FROM :date_value + INTERVAL '1 day') || TO_CHAR(:date_value + INTERVAL '1 day', '"W"IW') AS week_id,
		EXTRACT(YEAR FROM :date_value) || TO_CHAR(:date_value, '"W"WW') AS week_id_iso,
		TO_CHAR(:date_value + INTERVAL '1 day', '"W"WW') AS week_name,
		TO_CHAR(:date_value, '"W"WW') AS week_name_iso,
		TO_CHAR(:date_value, 'W')::INT AS week_of_month,
		EXTRACT(WEEK FROM :date_value + INTERVAL '1 day') AS week_of_year,
		EXTRACT(WEEK FROM :date_value) AS week_of_year,
		EXTRACT(YEAR FROM :date_value + INTERVAL '1 day') || TO_CHAR(:date_value + INTERVAL '1 day', '"-W"WW-') || EXTRACT(DOW FROM :date_value) AS week_of_year_id,
		EXTRACT(WEEK FROM :date_value) AS week_of_year_iso,
		EXTRACT(ISOYEAR FROM :date_value) || TO_CHAR(:date_value, '"-W"IW-') || EXTRACT(ISODOW FROM :date_value) AS week_of_year_iso_id
	""".strip()
	with engine.connect() as conn:
		result = conn.execute(text(sql), params)
		row = result.fetchone()
		print(row)
	return


def psql_week_info():
	sql = """
		SELECT	datum AS date_id,
		TO_CHAR(datum, 'TMDay') AS day_name,
		EXTRACT(DOW FROM datum) AS day_of_week,
		EXTRACT(ISODOW FROM datum) AS day_of_week_iso,
		EXTRACT(YEAR FROM datum + INTERVAL '1 day') || TO_CHAR(datum + INTERVAL '1 day', '"W"IW') AS week_id,
		EXTRACT(YEAR FROM datum) || TO_CHAR(datum, '"W"WW') AS week_id_iso,
		TO_CHAR(datum + INTERVAL '1 day', '"W"WW') AS week_name,
		TO_CHAR(datum, '"W"WW') AS week_name_iso,
		-- TO_CHAR(datum, 'W')::INT AS week_of_month,
		-- EXTRACT(WEEK FROM datum + INTERVAL '1 day') AS week_of_year,
		EXTRACT(WEEK FROM datum) AS week_of_year,
		EXTRACT(YEAR FROM datum + INTERVAL '1 day') || TO_CHAR(datum + INTERVAL '1 day', '"-W"WW-') || EXTRACT(DOW FROM datum) AS week_of_year_id,
		EXTRACT(WEEK FROM datum) AS week_of_year_iso,
		EXTRACT(ISOYEAR FROM datum) || TO_CHAR(datum, '"-W"IW-') || EXTRACT(ISODOW FROM datum) AS week_of_year_iso_id
		FROM (	SELECT	'2024-11-09'::DATE + SEQUENCE.DAY AS datum
		FROM	GENERATE_SERIES(0, 21) AS SEQUENCE (DAY)
		GROUP BY SEQUENCE.DAY) DQ
		ORDER BY 1;
		""".strip()
	print(sql)
	with engine.connect() as conn:
		result = conn.execute(text(sql))
		for row in result.fetchall():
			print(row)
	return


def quarter(dt: datetime) -> int:
	return (dt.month - 1) // 3 + 1


def week_number_of_month(date_value):
     return (date_value.isocalendar()[1] - date_value.replace(day=1).isocalendar()[1] + 1)


if __name__ == "__main__":
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
	# print(f"DB_URL: {_db_uri}")
	engine = create_engine(_db_uri)

	init()
	main()
	eoj()
