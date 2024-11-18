#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# models.py - Saturday, November 26, 2022
""" Creating a date dimension """
__version__ = "0.2.3-dev0"

import os, sys
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from glob import glob
from os.path import exists, expanduser, join

import sqlalchemy as sa
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.orm import backref
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy.orm.collections import attribute_mapped_collection

from config import Config

schema = Config.DB_SCHEMA
engine = sa.create_engine(Config.SQLALCHEMY_DATABASE_URI)
metadata = sa.MetaData(bind=engine, schema=schema)
Base = declarative_base(metadata=metadata)

__MODULE__ = os.path.splitext(os.path.basename(__file__))[0]


class DimDate(Base):
    __tablename__ = 'dim_date'

    id = sa.Column(sa.Integer, primary_key=True)
    date_id = sa.Column(sa.Date, nullable=False, unique=True)
    epoch = sa.Column(sa.BigInteger, nullable=False)
    day_suffix = sa.Column(sa.String(4), nullable=False)
    day_name = sa.Column(sa.String(9), nullable=False)
    day_of_week = sa.Column(sa.Integer, nullable=False)
    day_of_week_iso = sa.Column(sa.Integer, nullable=False)
    day_of_month = sa.Column(sa.Integer, nullable=False)
    day_of_quarter = sa.Column(sa.Integer, nullable=False)
    day_of_year = sa.Column(sa.Integer, nullable=False)
    week_id = sa.Column(sa.String(7), nullable=False)
    week_id_iso = sa.Column(sa.String(7), nullable=False)
    week_name = sa.Column(sa.String(3), nullable=False)
    week_name_iso = sa.Column(sa.String(3), nullable=False)
    week_of_month = sa.Column(sa.Integer, nullable=False)
    week_of_year = sa.Column(sa.Integer, nullable=False)
    week_of_year_id = sa.Column(sa.CHAR(10), nullable=False)
    week_of_year_iso = sa.Column(sa.Integer, nullable=False)
    week_of_year_iso_id = sa.Column(sa.CHAR(10), nullable=False)
    month_of_year = sa.Column(sa.Integer, nullable=False)
    month_name = sa.Column(sa.String(9), nullable=False)
    month_abbr = sa.Column(sa.CHAR(3), nullable=False)
    quarter_of_year = sa.Column(sa.Integer, nullable=False)
    quarter_name = sa.Column(sa.String(9), nullable=False)
    quarter_id = sa.Column(sa.CHAR(6), nullable=False)
    yyyy = sa.Column(sa.Integer, nullable=False, index=True)
    week_from = sa.Column(sa.Date, nullable=False)
    week_thru = sa.Column(sa.Date, nullable=False, index=True)
    week_from_iso = sa.Column(sa.Date, nullable=False)
    week_thru_iso = sa.Column(sa.Date, nullable=False)
    month_from = sa.Column(sa.Date, nullable=False)
    month_thru = sa.Column(sa.Date, nullable=False, index=True)
    quarter_from = sa.Column(sa.Date, nullable=False)
    quarter_thru = sa.Column(sa.Date, nullable=False)
    year_from = sa.Column(sa.Date, nullable=False)
    year_thru = sa.Column(sa.Date, nullable=False)
    mmyyyy = sa.Column(sa.CHAR(6), nullable=False)
    mmddyyyy = sa.Column(sa.CHAR(10), nullable=False)
    is_weekend = sa.Column(sa.Boolean, nullable=False)
    # schema="public"


class DateDim2(Base):
    __tablename__ = "dim_date_dev"
    id = sa.Column(sa.Integer, nullable=False, primary_key=True)
    date_id = sa.Column(sa.Date, nullable=False, unique=True)

    def __str__(self):
        return self.date_id

    def __repr__(self):
        return f"<DateDim({self.date_id})>"


@dataclass
class DateInfo:
    pass


if __name__ == '__main__':
    _run_dt = datetime.now().astimezone().replace(microsecond=0)
    _run_utc = _run_dt.astimezone(timezone.utc).replace(tzinfo=None)
    _fdate = _run_dt.strftime("%Y-%m-%d")
    _fdatetime = _run_dt.strftime("%Y%m%d_%H%M%S")

