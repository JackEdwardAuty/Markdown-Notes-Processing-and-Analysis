import pandas as pd

# Load your meds file
meds = pd.read_csv("medication_expanded_public.csv")

# Your actual column names
date_col = "date"
med_col = "Medication"

# Parse dates
meds[date_col] = pd.to_datetime(meds[date_col], dayfirst=True)

# Build dense daily date range
all_days = pd.DataFrame({
    "Date": pd.date_range(meds[date_col].min(), meds[date_col].max(), freq="D")
})

# Flag Ritalin XR / IR days
meds["Ritalin_Taken"] = meds[med_col].isin(["Ritalin IR"]).astype(int)

# Aggregate to daily counts
daily = (
    meds.groupby(date_col, as_index=False)["Ritalin_Taken"]
        .sum()
        .rename(columns={date_col: "Date"})
)

# Join onto scaffold so missing days become 0
daily = all_days.merge(daily, on="Date", how="left")
daily["Ritalin_Taken"] = daily["Ritalin_Taken"].fillna(0).astype(int)

daily.to_csv("ritalin_IR_daily_tableau.csv", index=False)
print("Written ritalin_IR_daily_tableau.csv")
