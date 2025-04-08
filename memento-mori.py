#!/usr/bin/env python3

import calendar
import datetime
import functools
import os
import sys
import time
from typing import Final, Generator, Iterable, Mapping, NamedTuple


CALENDAR_MONTH_ABBR: Final = calendar.month_abbr[1:]
MONTHS_IN_YEAR: Final = len(CALENDAR_MONTH_ABBR)
WEEKS_IN_MONTH: Final = 4
DAYS_IN_WEEK: Final = len(calendar.day_name)


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


type STATUS_WEEK = bool
type STATUS_MONTH = Generator[STATUS_WEEK]
type STATUS_YEAR = Generator[STATUS_MONTH]

RENDER_CHARS: Final[Mapping[STATUS_WEEK, str]] = {
    False: "\u2592",
    True: "\u00b7",
}


def compute_calendar(
    *,
    begin: datetime.datetime,
    end: datetime.datetime,
    now: datetime.datetime,
) -> Generator[STATUS_YEAR]:
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

    yield from (
        compute_calendar_year(
            week_begin=week_begin,
            week_end=week_end,
            week_now=week_now,
            year=year,
        )
        for year in range(begin.year, end.year + 1)
    )


def compute_calendar_year(
    *,
    week_begin: Week,
    week_end: Week,
    week_now: Week,
    year: int,
) -> STATUS_YEAR:
    yield from (
        compute_calendar_month(
            week_begin=week_begin,
            week_end=week_end,
            week_now=week_now,
            year=year,
            month=month,
        )
        for month in range(MONTHS_IN_YEAR)
    )


def compute_calendar_month(
    *,
    week_begin: Week,
    week_end: Week,
    week_now: Week,
    year: int,
    month: int,
) -> STATUS_MONTH:
    yield from (
        compute_calendar_week(
            week_begin=week_begin,
            week_end=week_end,
            week_now=week_now,
            week_cur=Week(
                year=year,
                month=month,
                week_in_month=week,
            ),
        )
        for week in range(WEEKS_IN_MONTH)
    )


def compute_calendar_week(
    *,
    week_begin: Week,
    week_end: Week,
    week_now: Week,
    week_cur: Week,
) -> STATUS_WEEK:
    return week_cur < week_begin or week_cur > week_now or week_cur > week_end


def render_calendar(
    *,
    years: Iterable[STATUS_YEAR],
    year_begin: int,
    labels: bool,
    delay: float,
) -> None:
    if labels:
        print(
            functools.reduce(
                lambda s, m: f"{s}  {m.upper()}",
                CALENDAR_MONTH_ABBR,
                "    ",
            )
        )

    render_week = functools.partial(
        print,
        end="",
        flush=delay > 0.0,
    )

    for label, year in enumerate(
        iterable=years,
        start=year_begin,
    ):
        if labels:
            print(label, end=" ")

        for month in year:
            for week_done in month:
                render_week(
                    RENDER_CHARS[week_done],
                )
                time.sleep(delay)

            print(end=" ")

        print()


if __name__ == "__main__":
    WEEKS: Final = int(
        os.environ.get(
            "WEEKS",
            "4000",
        )
    )
    assert 0 < WEEKS <= 400_000

    LABELS: Final = bool(
        os.environ.get("LABELS"),
    )

    DELAY: Final = float(
        os.environ.get(
            "DELAY",
            "0.0",
        ),
    )
    assert DELAY >= 0.0

    YEAR_BEGIN, MONTH_BEGIN, DAY_BEGIN = map(
        lambda s: int(s),
        sys.argv[1:4],
    )

    BEGIN: Final = datetime.datetime(
        year=YEAR_BEGIN,
        month=MONTH_BEGIN,
        day=DAY_BEGIN,
    )

    render_calendar(
        years=compute_calendar(
            begin=BEGIN,
            end=BEGIN + datetime.timedelta(days=WEEKS * DAYS_IN_WEEK),
            now=datetime.datetime.now(),
        ),
        year_begin=BEGIN.year,
        labels=LABELS,
        delay=DELAY,
    )
