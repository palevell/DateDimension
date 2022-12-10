# coding: utf-8
from sqlalchemy import BigInteger, Boolean, CHAR, Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class DimDate(Base):
    __tablename__ = 'dim_date'

    id = Column(Integer, primary_key=True)
    date_id = Column(Date, nullable=False, unique=True)
    epoch = Column(BigInteger, nullable=False)
    day_suffix = Column(String(4), nullable=False)
    day_name = Column(String(9), nullable=False)
    day_of_week = Column(Integer, nullable=False)
    day_of_week_iso = Column(Integer, nullable=False)
    day_of_month = Column(Integer, nullable=False)
    day_of_quarter = Column(Integer, nullable=False)
    day_of_year = Column(Integer, nullable=False)
    week_id = Column(String(7), nullable=False)
    week_id_iso = Column(String(7), nullable=False)
    week_name = Column(String(3), nullable=False)
    week_name_iso = Column(String(3), nullable=False)
    week_of_month = Column(Integer, nullable=False)
    week_of_year = Column(Integer, nullable=False)
    week_of_year_id = Column(CHAR(10), nullable=False)
    week_of_year_iso = Column(Integer, nullable=False)
    week_of_year_iso_id = Column(CHAR(10), nullable=False)
    month_of_year = Column(Integer, nullable=False)
    month_name = Column(String(9), nullable=False)
    month_abbr = Column(CHAR(3), nullable=False)
    quarter_of_year = Column(Integer, nullable=False)
    quarter_name = Column(String(9), nullable=False)
    quarter_id = Column(CHAR(6), nullable=False)
    yyyy = Column(Integer, nullable=False, index=True)
    week_from = Column(Date, nullable=False)
    week_thru = Column(Date, nullable=False, index=True)
    week_from_iso = Column(Date, nullable=False)
    week_thru_iso = Column(Date, nullable=False)
    month_from = Column(Date, nullable=False)
    month_thru = Column(Date, nullable=False, index=True)
    quarter_from = Column(Date, nullable=False)
    quarter_thru = Column(Date, nullable=False)
    year_from = Column(Date, nullable=False)
    year_thru = Column(Date, nullable=False)
    mmyyyy = Column(CHAR(6), nullable=False)
    mmddyyyy = Column(CHAR(10), nullable=False)
    is_weekend = Column(Boolean, nullable=False)

