import calendar
import datetime
import functools
import sys

try:
    weeks_num = int(sys.argv[4])
except Exception:
    weeks_num = 4000

birth = datetime.datetime(year=int(sys.argv[1]), month=int(sys.argv[2]), day=int(sys.argv[3]))
year_birth = birth.year
start = datetime.datetime(year=year_birth + 1, month=1, day=1)
now = datetime.datetime.now()

months_in_year = 12
weeks_in_month = 4
days_in_week = 7

char_done = "*"
str_month_done = f" {"*" * weeks_in_month}"
str_year_done = str_month_done * months_in_year
char_undone = "."
str_month_undone = f" {"." * weeks_in_month}"
str_year_undone = str_month_undone * months_in_year

print(functools.reduce(lambda s, m: f"{s}  {m.upper()}", calendar.month_abbr[1:], "    "))
week_birth = birth.day // days_in_week
row_start = f"{str_month_undone * (birth.month - 1)} {char_undone * week_birth}{char_done * (weeks_in_month - week_birth)}{str_month_done * (months_in_year - birth.month)}"
print(f"{year_birth}{row_start}")

for idx in range(now.year - start.year):
    print(f"{year_birth + 1 + idx}{str_year_done}")

week_now = now.day // days_in_week
row_cur = f"{str_month_done * (now.month - 1)} {char_done * week_now}{char_undone * (weeks_in_month - week_now)}{str_month_undone * (months_in_year - now.month)}"
print(f"{now.year}{row_cur}")

days_undone = weeks_num * days_in_week - (now - start).days
date_end = now + datetime.timedelta(days=days_undone)
years_undone = date_end.year - now.year
for idx in range(years_undone):
    print(f"{now.year + idx + 1}{str_year_undone}")
