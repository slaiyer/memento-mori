import calendar
import datetime
import functools
import os
import sys
import typing


WEEKS = int(os.environ.get("WEEKS", "4000"))
LABELS = bool(os.environ.get("LABELS", ""))

WEEKS_IN_MONTH = 4
DAYS_IN_WEEK = 7

BEGIN = datetime.datetime(
    year=int(sys.argv[1]), month=int(sys.argv[2]), day=int(sys.argv[3])
)
END = BEGIN + datetime.timedelta(days=WEEKS * DAYS_IN_WEEK)
NOW = datetime.datetime.now()


class Week(typing.NamedTuple):
    year: int
    month: int
    week_in_month: int

    @staticmethod
    def get_week_num(day: int) -> int:
        return min(day // DAYS_IN_WEEK, WEEKS_IN_MONTH)


WEEK_BEGIN = Week(BEGIN.year, BEGIN.month, Week.get_week_num(BEGIN.day))
WEEK_END = Week(END.year, END.month, Week.get_week_num(END.day))
WEEK_NOW = Week(NOW.year, NOW.month, Week.get_week_num(NOW.day))

CHAR_DONE = "\u2588"
CHAR_UNDONE = "\u00b7"

if LABELS:
    print(
        functools.reduce(
            lambda s, m: f"{s}  {m.upper()}", calendar.month_abbr[1:], "    "
        )
    )

for year in range(BEGIN.year, END.year + 1):
    if LABELS:
        print(year, end=" ")

    for month in range(1, 13):
        for week in range(0, 4):
            week_cur = Week(year, month, week)
            if week_cur > WEEK_NOW or week_cur > WEEK_END or week_cur < WEEK_BEGIN:
                print(CHAR_UNDONE, end="")
            else:
                print(CHAR_DONE, end="")
        print(end=" ")
    print()
