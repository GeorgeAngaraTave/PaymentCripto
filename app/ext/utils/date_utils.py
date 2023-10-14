# -*- coding: utf-8 -*-

from datetime import datetime, timedelta, date
from app.config.local_settings import STDR_UTC_HOUR
from dateutil.relativedelta import relativedelta
import calendar


class DateUtils:

    @staticmethod
    def get_timestamp():
        now = datetime.utcnow() - timedelta(hours=STDR_UTC_HOUR)
        timestamp = now.strftime('%Y%m%d%H%M%S')
        return timestamp

    @staticmethod
    def today(format_date=None, type_format='str'):
        format_date = '%Y-%m-%d' if format_date is None else format_date
        now = datetime.utcnow() - timedelta(hours=STDR_UTC_HOUR)

        if type_format is 'str':
            current_date = now.strftime(format_date)
            return current_date
        elif type_format is 'date':
            return now
        return None

    @staticmethod
    def get_current_time():
        now = datetime.utcnow() - timedelta(hours=STDR_UTC_HOUR)
        current_time = now.strftime('%Y-%m-%d %H:%M:%S')
        return current_time

    @staticmethod
    def compare_dates(init_date=None, end_date=None, compare='eq'):
        if init_date is None:
            return None
        if end_date is None:
            return None
        try:
            _init = datetime.strptime(init_date, '%Y-%m-%d')
            _end = datetime.strptime(end_date, '%Y-%m-%d')

            if compare is 'eq':
                if _init == _end:
                    return True
                else:
                    return False
            elif compare is 'gr':
                if _init > _end:
                    return True
                else:
                    return False
            elif compare is 'le':
                if _init < _end:
                    return True
                else:
                    return False
            elif compare is 'gt':
                if _init >= _end:
                    return True
                else:
                    return False
            elif compare is 'lt':
                if _init <= _end:
                    return True
                else:
                    return False
        except Exception as e:
            print("compare_dates Exception: an invalid date has been entered")
            print("compare_dates Exception:", e.message)
            return None
        return None

    @staticmethod
    def fix_time(_time=None):
        n_time = None

        if _time is None:
            return None

        try:
            _init = datetime.strptime(str(_time), '%H:%M:%S')
            n_time = datetime.strftime(_init, '%H:%M')
            return n_time
        except Exception:
            # print "fix_time: Exception can not convert using H:M:S"
            try:
                _init = datetime.strptime(str(_time), '%H:%M')
                n_time = datetime.strftime(_init, '%H:%M')
                return n_time
            except Exception:
                # print "fix_time: can not convert this time format", _time
                return None
            return None

    @staticmethod
    def compare_times(init_time=None, end_time=None, compare='eq'):
        if init_time is None:
            return None

        if end_time is None:
            return None

        init_time = DateUtils.fix_time(init_time)
        if init_time is None:
            return None

        end_time = DateUtils.fix_time(end_time)
        if end_time is None:
            return None

        _init = datetime.strptime(init_time, '%H:%M')
        _end = datetime.strptime(end_time, '%H:%M')

        if compare is 'eq':
            if _init == _end:
                return True
            else:
                return False
        if compare is 'gt':
            if _init >= _end:
                return True
            else:
                return False

    @staticmethod
    def day_of_week(init_date):
        if init_date is None:
            return None

        y, m, d = init_date.split('-')
        week_day = date(int(y), int(m), int(d)).weekday()
        calendar_day = calendar.day_name[week_day]
        return {'calendar_day': calendar_day, 'week_day': (week_day + 1)}

    @staticmethod
    def to_date(current_date, current_format, new_format=None):
        if current_date is None:
            return None

        if current_format is None:
            return None

        new_format = '%Y-%m-%d' if new_format is None else new_format

        try:
            _date = datetime.strptime(current_date, current_format)
            new_date = _date.strftime(new_format)
            return new_date
        except Exception:
            return None

    @staticmethod
    def add_months(add_months=1, init_date=None):
        added_months = None
        if init_date is None:
            next_month = date.today() + relativedelta(months=+add_months)
            added_months = datetime.strftime(next_month, "%Y-%m-%d")
        else:
            next_month = datetime.strptime(init_date, '%Y-%m-%d') + relativedelta(months=+add_months)
            added_months = datetime.strftime(next_month, "%Y-%m-%d")
        return added_months

    @staticmethod
    def add_days(current_date, num_days=None):

        if current_date is None:
            return None

        if num_days is None:
            return None

        try:
            _init = datetime.strptime(current_date, '%Y-%m-%d')
            resp = _init + timedelta(days=num_days)
            early_date = datetime.strftime(resp, '%Y-%m-%d')

            if early_date is None:
                return None
            return early_date
        except Exception as e:
            print("add_days Exception:", e.message)
            return None

    @staticmethod
    def get_next_month(init_date=None):

        if init_date is None:
            return None

        try:
            y1, m1, d1 = init_date.split('-')
            _initd = date(int(y1), int(m1), int(d1))

            new_month = _initd + datetime.timedelta(days=calendar.monthrange(_initd.year, _initd.month)[1])
            next_month = datetime.datetime.strftime(new_month, "%Y-%m-%d")

            return next_month
        except Exception as e:
            print("get_next_month Exception:", e.message)
            return None
