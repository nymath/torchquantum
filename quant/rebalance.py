from abc import ABCMeta, abstractmethod
from pandas_market_calendars import get_calendar
import itertools
from collections import defaultdict


class Calendar(object, metaclass=ABCMeta):
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        self.exchange = 'SSE'
        self.calendar = get_calendar(self.exchange)
        self.trade_dates = self.calendar.valid_days(start_date=self.start_date, end_date=self.end_date)
        self.trade_dates = self.trade_dates.tz_convert(None)

    def create_monthly_groups(self):
        rlt = defaultdict(list)
        for key, value in zip(self.trade_dates, [(x.year, x.month) for x in self.trade_dates]):
            rlt[value].append(key)
        return rlt

    def create_weekly_groups(self):
        rlt = defaultdict(list)
        for key, value in zip(self.trade_dates, [(x.year, x.week) for x in self.trade_dates]):
            rlt[value].append(key)
        return rlt


class Weekly(object):
    def __init__(self, start_date, end_date, *args):
        self.start_date = start_date
        self.end_date = end_date
        self.args = args
        self.trade_dates = None
        self._create_trade_dates()

    def _create_trade_dates(self):
        calendar = Calendar(self.start_date, self.end_date)
        self.trade_dates = calendar.create_weekly_groups()
        self.trade_dates = [x[i] for x in self.trade_dates.items() for i in self.args]


class Monthly(object):
    def __init__(self, start_date, end_date, *args):
        self.start_date = start_date
        self.end_date = end_date
        self.args = args
        self.trade_dates = None
        self._create_trade_dates()

    def _create_trade_dates(self):
        calendar = Calendar(self.start_date, self.end_date)
        self.trade_dates = calendar.create_monthly_groups()
        self.trade_dates = [x[i] for x in self.trade_dates.items() for i in self.args]

