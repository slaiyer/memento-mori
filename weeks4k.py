#!/usr/bin/env python3

import calendar
import datetime
import functools
import os
import sys
import typing


def main(argv: list[str]) -> None:
    weeks = int(os.environ.get("WEEKS", "4000"))
    labels = bool(os.environ.get("LABELS", ""))

    begin = datetime.datetime(year=int(argv[0]), month=int(argv[1]), day=int(argv[2]))
    end = begin + datetime.timedelta(days=weeks * DAYS_IN_WEEK)
    now = datetime.datetime.now()

    week_begin = Week(begin.year, begin.month, Week.get_week_num(begin.day))
    week_end = Week(end.year, end.month, Week.get_week_num(end.day))
    week_now = Week(now.year, now.month, Week.get_week_num(now.day))

    if labels:
        print(
            functools.reduce(
                lambda s, m: f"{s}  {m.upper()}", calendar.month_abbr[1:], "    "
            )
        )

    for year in range(begin.year, end.year + 1):
        if labels:
            print(year, end=" ")

        for month in range(1, 13):
            for week in range(0, 4):
                week_cur = Week(year, month, week)
                if week_cur > week_now or week_cur > week_end or week_cur < week_begin:
                    print(CHAR_UNDONE, end="")
                else:
                    print(CHAR_DONE, end="")
            print(end=" ")
        print()


class Week(typing.NamedTuple):
    year: int
    month: int
    week_in_month: int

    @staticmethod
    def get_week_num(day: int) -> int:
        return min(day // DAYS_IN_WEEK, WEEKS_IN_MONTH)


WEEKS_IN_MONTH = 4
DAYS_IN_WEEK = 7

CHAR_DONE = "\u2588"
CHAR_UNDONE = "\u00b7"


if __name__ == "__main__":
    main(sys.argv[1:])
