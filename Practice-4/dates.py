from datetime import datetime, date, timedelta

now = datetime.now()

#Exercise 1: subtract five days
five_days_ago = now - timedelta(days=5)
print("Current date:     ", now.strftime("%Y-%m-%d"))
print("Five days ago:    ", five_days_ago.strftime("%Y-%m-%d"))

#Exercise 2: yesterday, today, tomorrow
today = date.today()
print("Yesterday:", today - timedelta(days=1))
print("Today:    ", today)
print("Tomorrow: ", today + timedelta(days=1))

#Exercise 3: drop microseconds
print("With microseconds:   ", now)
print("Without microseconds:", now.replace(microsecond=0))

#Exercise 4: difference in seconds
d1 = datetime(2026, 1, 1, 0, 0, 0)
d2 = datetime(2026, 1, 2, 12, 30, 0)
diff = d2 - d1
print("Difference in seconds:", diff.total_seconds())
