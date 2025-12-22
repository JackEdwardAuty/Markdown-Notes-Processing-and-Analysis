import pandas as pd
wake = pd.read_csv('wake_time.csv')
meds = pd.read_csv('medication_expanded_public.csv')  # or medication_full.csv

# Ensure consistent filename (strip paths)
wake['filename_clean'] = wake['filename'].str.split('/').str[-1]
meds['filename_clean'] = meds['filename'].str.split('/').str[-1]

# Date standardization
wake['date'] = pd.to_datetime(wake['date'], errors='coerce')
meds['date'] = pd.to_datetime(meds['date'], errors='coerce')

# Save for Tableau
wake.to_csv('wake_tableau.csv', index=False)
meds.to_csv('meds_tableau.csv', index=False)
