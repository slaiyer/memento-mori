#!/usr/bin/env python3

import calendar
import datetime
import functools
import os
import sys
from typing import Annotated, Final, NamedTuple


CALENDAR_MONTH_ABBR: Final = calendar.month_abbr[1:]
MONTHS_IN_YEAR: Final = len(CALENDAR_MONTH_ABBR)
WEEKS_IN_MONTH: Final = 4
DAYS_IN_WEEK: Final = len(calendar.day_name)

RENDER_CHARS: Final = [
    "\u2592",
    "\u00b7",
]

type STATUS_MONTH = Annotated[
    list[bool],
    WEEKS_IN_MONTH,
]
type STATUS_YEAR = Annotated[
    list[STATUS_MONTH],
    MONTHS_IN_YEAR,
]
type STATUS_LIFE = list[STATUS_YEAR]


def compute_calendar(
    *,
    begin: datetime.datetime,
    end: datetime.datetime,
    now: datetime.datetime,
) -> STATUS_LIFE:
    week_begin: Final = Week(
        year=begin.year,
        month=begin.month,
        week_in_month=Week.get_week_num(day=begin.day),
    )
    week_end: Final = Week(
        year=end.year,
        month=end.month,
        week_in_month=Week.get_week_num(day=end.day),
    )
    week_now: Final = Week(
        year=now.year,
        month=now.month,
        week_in_month=Week.get_week_num(day=now.day),
    )

    status_life: Final[STATUS_LIFE] = []

    for year in range(begin.year, end.year + 1):
        status_year: STATUS_YEAR = []

        for month in range(1, MONTHS_IN_YEAR + 1):
            status_month: STATUS_MONTH = []

            for week in range(WEEKS_IN_MONTH):
                week_cur = Week(
                    year=year,
                    month=month,
                    week_in_month=week,
                )

                status_month.append(
                    week_cur < week_begin or week_cur > week_now or week_cur > week_end
                )

            status_year.append(status_month)

        status_life.append(status_year)

    return status_life


def render_calendar(
    *,
    status_life: STATUS_LIFE,
    begin: datetime.datetime,
    labels: bool,
) -> None:
    if labels:
        print(
            functools.reduce(
                lambda s, m: f"{s}  {m.upper()}",
                CALENDAR_MONTH_ABBR,
                "    ",
            )
        )

    for idx, year in enumerate(status_life):
        if labels:
            print(
                begin.year + idx,
                end=" ",
            )

        for month in year:
            for week_done in month:
                print(
                    RENDER_CHARS[week_done],
                    end="",
                )

            print(" ", end="")

        print()


class Week(NamedTuple):
    year: int
    month: int
    week_in_month: int

    @staticmethod
    def get_week_num(
        *,
        day: int,
    ) -> int:
        return min(
            day // DAYS_IN_WEEK,
            WEEKS_IN_MONTH,
        )


if __name__ == "__main__":
    WEEKS: Final = int(
        os.environ.get(
            "WEEKS",
            "4000",
        )
    )
    assert 0 < WEEKS <= 400_000

    LABELS: Final = bool(
        os.environ.get("LABELS", ""),
    )

    YEAR, MONTH, DAY = map(
        lambda s: int(s),
        sys.argv[1:4],
    )

    BEGIN: Final = datetime.datetime(
        year=YEAR,
        month=MONTH,
        day=DAY,
    )

    END: Final = BEGIN + datetime.timedelta(days=WEEKS * DAYS_IN_WEEK)

    render_calendar(
        status_life=compute_calendar(
            begin=BEGIN,
            end=END,
            now=datetime.datetime.now(),
        ),
        begin=BEGIN,
        labels=LABELS,
    )
