from datetime import datetime, timedelta
import sys

try:
    weeks_num = int(sys.argv[4])
except Exception:
    weeks_num = 4000

birth = datetime(year=int(sys.argv[1]), month=int(sys.argv[2]), day=int(sys.argv[3]))
year_birth = birth.year
start = datetime(year=year_birth + 1, month=1, day=1)
now = datetime.now()

char_done = "*"
str_month_done = f" {"*" * 4}"
str_year_done = str_month_done * 12
char_undone = "."
str_month_undone = f" {"." * 4}"
str_year_undone = str_month_undone * 12

print("      JAN  FEB  MAR  APR  MAY  JUN  JUL  AUG  SEP  OCT  NOV  DEC")
week_birth = birth.day // 7
row_start = f"{str_month_undone * (birth.month - 1)} {char_undone * week_birth}{char_done * (4 - week_birth)}{str_month_done * (12 - birth.month)}"
print(f"{year_birth}{row_start}")

for idx in range(now.year - start.year):
    print(f"{year_birth + 1 + idx}{str_year_done}")

week_now = now.day // 7
row_cur = f"{str_month_done * (now.month - 1)} {char_done * week_now}{char_undone * (4 - week_now)}{str_month_undone * (12 - now.month)}"
print(f"{now.year}{row_cur}")

days_undone = weeks_num * 7 - (now - start).days
date_end = now + timedelta(days=days_undone)
years_undone = date_end.year - now.year
for idx in range(years_undone):
    print(f"{now.year + idx + 1}{str_year_undone}")
