#!/usr/bin/env python3

import calendar
import datetime
import functools
import os
import sys
import time
from typing import Final, Generator, Iterable, Mapping, NamedTuple, Sequence


type STATUS_WEEK = bool
type STATUS_MONTH = Generator[STATUS_WEEK]
type STATUS_YEAR = Generator[STATUS_MONTH]

CALENDAR_MONTH_ABBR: Final = calendar.month_abbr[1:]
MONTHS_IN_YEAR: Final = len(CALENDAR_MONTH_ABBR)
WEEKS_IN_MONTH: Final = 4
DAYS_IN_WEEK: Final = len(calendar.day_name)
RENDER_CHARS: Final = {
    False: "\u2592",
    True: "\u00b7",
}


def main() -> None:
    weeks: Final = int(
        os.environ.get(
            "WEEKS",
            "4000",
        )
    )
    assert 0 < weeks <= 400_000

    labels: Final = bool(
        os.environ.get("LABELS"),
    )

    delay: Final = float(
        os.environ.get(
            "DELAY",
            "0.0",
        ),
    )
    assert delay >= 0.0

    year_begin, month_begin, day_begin = map(
        lambda s: int(s),
        sys.argv[1:4],
    )

    begin: Final = datetime.datetime(
        year=year_begin,
        month=month_begin,
        day=day_begin,
    )

    calendar: Final = compute_calendar(
        begin=begin,
        end=begin + datetime.timedelta(days=weeks * DAYS_IN_WEEK),
        now=datetime.datetime.now(),
        days_in_week=DAYS_IN_WEEK,
        weeks_in_month=WEEKS_IN_MONTH,
        months_in_year=MONTHS_IN_YEAR,
    )

    render_calendar(
        years=calendar,
        year_begin=begin.year,
        labels=labels,
        header=CALENDAR_MONTH_ABBR,
        delay=delay,
        render_chars=RENDER_CHARS,
    )


class Week(NamedTuple):
    year: int
    month: int
    week_in_month: int

    @staticmethod
    def get_week_num(
        *,
        day: int,
        days_in_week: int,
        weeks_in_month: int,
    ) -> int:
        return min(
            day // days_in_week,
            weeks_in_month,
        )


def compute_calendar(
    *,
    begin: datetime.datetime,
    end: datetime.datetime,
    now: datetime.datetime,
    days_in_week: int,
    weeks_in_month: int,
    months_in_year: int,
) -> Generator[STATUS_YEAR]:
    get_week_num: Final = functools.partial(
        Week.get_week_num,
        days_in_week=days_in_week,
        weeks_in_month=weeks_in_month,
    )

    week_begin: Final = Week(
        year=begin.year,
        month=begin.month,
        week_in_month=get_week_num(day=begin.day),
    )
    week_end: Final = Week(
        year=end.year,
        month=end.month,
        week_in_month=get_week_num(day=end.day),
    )
    week_now: Final = Week(
        year=now.year,
        month=now.month,
        week_in_month=get_week_num(day=now.day),
    )

    yield from (
        compute_calendar_year(
            week_begin=week_begin,
            week_end=week_end,
            week_now=week_now,
            year=year,
            weeks_in_month=weeks_in_month,
            months_in_year=months_in_year,
        )
        for year in range(begin.year, end.year + 1)
    )


def compute_calendar_year(
    *,
    week_begin: Week,
    week_end: Week,
    week_now: Week,
    year: int,
    weeks_in_month: int,
    months_in_year: int,
) -> STATUS_YEAR:
    yield from (
        compute_calendar_month(
            week_begin=week_begin,
            week_end=week_end,
            week_now=week_now,
            year=year,
            month=month,
            weeks_in_month=weeks_in_month,
        )
        for month in range(months_in_year)
    )


def compute_calendar_month(
    *,
    week_begin: Week,
    week_end: Week,
    week_now: Week,
    year: int,
    month: int,
    weeks_in_month: int,
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
        for week in range(weeks_in_month)
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
    header: Sequence[str],
    delay: float,
    render_chars: Mapping[STATUS_WEEK, str],
) -> None:
    if labels:
        print(
            functools.reduce(
                lambda s, m: f"{s}  {m.upper()}",
                header,
                "    ",
            )
        )

    render_week: Final = functools.partial(
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
                    render_chars[week_done],
                )
                time.sleep(delay)

            print(end=" ")

        print()


if __name__ == "__main__":
    main()
