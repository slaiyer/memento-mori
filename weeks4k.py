import calendar
import datetime
import functools
import os
import sys


weeks_num = int(os.environ.get("WEEKS", "4000"))
labels = bool(os.environ.get("LABELS", ""))

birth = datetime.datetime(year=int(sys.argv[1]), month=int(sys.argv[2]), day=int(sys.argv[3]))
start = datetime.datetime(year=birth.year + 1, month=1, day=1)
now = datetime.datetime.now()
assert(birth < now)

months_in_year = 12
weeks_in_month = 4
days_in_week = 7

char_done = "\u2588"
str_month_done = f" {char_done * weeks_in_month}"
str_year_done = str_month_done * months_in_year
char_undone = "\u00B7"
str_month_undone = f" {char_undone * weeks_in_month}"
str_year_undone = str_month_undone * months_in_year

if labels:
    print(functools.reduce(lambda s, m: f"{s}  {m.upper()}", calendar.month_abbr[1:], "    "))

week_birth = birth.day // days_in_week
week_now = now.day // days_in_week
row_start = f"{str_month_undone * (birth.month - 1)} {char_undone * week_birth}{char_done * (weeks_in_month - week_birth)}"
if now.year == birth.year:
    row_start += f"{str_month_done * (now.month - birth.month - 1)} {char_done * week_now}{char_undone * (weeks_in_month - week_now)}{str_month_undone * (months_in_year - now.month)}"
else:
    row_start += f"{str_month_done * (months_in_year - birth.month)}"

if labels:
    print(birth.year, end="")
print(row_start)

for idx in range(now.year - start.year):
    if labels:
        print(birth.year + 1 + idx, end="")
    print(str_year_done)

if now.year != birth.year:
    row_cur = f"{str_month_done * (now.month - 1)} {char_done * week_now}{char_undone * (weeks_in_month - week_now)}{str_month_undone * (months_in_year - now.month)}"
    if labels:
        print(now.year, end="")
    print(row_cur)

days_undone = weeks_num * days_in_week - (now - start).days
date_end = now + datetime.timedelta(days=days_undone)
years_undone = date_end.year - now.year
for idx in range(years_undone):
    if labels:
        print(now.year + 1 + idx, end="")
    print(str_year_undone)
