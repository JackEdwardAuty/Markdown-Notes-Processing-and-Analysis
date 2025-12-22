import pandas as pd

daily = pd.read_csv("ritalin_IR_daily_tableau.csv")
daily["Date"] = pd.to_datetime(daily["Date"])

daily = daily.sort_values("Date")

# Ritalin_Taken is 0/1 int
streak = 0
streaks = []
for taken in daily["Ritalin_Taken"]:
    if taken > 0:
        streak += 1
    else:
        streak = 0
    streaks.append(streak)

daily["Ritalin_Streak"] = streaks

daily.to_csv("ritalin_IR_streak_tableau.csv", index=False)
print("Written ritalin_streak_tableau.csv")
