#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# models.py - Saturday, November 26, 2022
""" Creating a date dimension """
__version__ = "0.1.0-dev0"

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
Base = declarative_base(metadata=sa.MetaData(schema=schema))

__MODULE__ = os.path.splitext(os.path.basename(__file__))[0]


class DateDim(Base):
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

