#!/usr/bin/env python3

import calendar
import datetime
import functools
import os
import sys
from typing import Final, NamedTuple


CALENDAR_MONTH_ABBR: Final = calendar.month_abbr[1:]
WEEKS_IN_MONTH: Final = 4
DAYS_IN_WEEK: Final = 7

CHAR_DONE: Final = "\u2592"
CHAR_UNDONE: Final = "\u00b7"


def main(argv: list[str]) -> None:
    weeks: Final = int(os.environ.get("WEEKS", "4000"))
    assert 0 < weeks <= 400_000
    labels: Final = bool(os.environ.get("LABELS", ""))

    begin: Final = datetime.datetime(
        year=int(argv[0]), month=int(argv[1]), day=int(argv[2])
    )
    end: Final = begin + datetime.timedelta(days=weeks * DAYS_IN_WEEK)
    now: Final = datetime.datetime.now()

    week_begin: Final = Week(begin.year, begin.month, Week.get_week_num(begin.day))
    week_end: Final = Week(end.year, end.month, Week.get_week_num(end.day))
    week_now: Final = Week(now.year, now.month, Week.get_week_num(now.day))

    if labels:
        print(
            functools.reduce(
                lambda s, m: f"{s}  {m.upper()}", CALENDAR_MONTH_ABBR, "    "
            )
        )

    for year in range(begin.year, end.year + 1):
        if labels:
            print(year, end=" ")

        for month in range(1, len(CALENDAR_MONTH_ABBR) + 1):
            for week in range(WEEKS_IN_MONTH):
                week_cur = Week(year, month, week)
                print(
                    CHAR_UNDONE
                    if week_cur > week_now
                    or week_cur > week_end
                    or week_cur < week_begin
                    else CHAR_DONE,
                    end="",
                )
            print(end=" ")
        print()


class Week(NamedTuple):
    year: int
    month: int
    week_in_month: int

    @staticmethod
    def get_week_num(day: int) -> int:
        return min(day // DAYS_IN_WEEK, WEEKS_IN_MONTH)


if __name__ == "__main__":
    main(sys.argv[1:])
