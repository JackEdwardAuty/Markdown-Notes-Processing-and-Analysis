import pandas as pd
meds = pd.read_csv('medication_expanded_public.csv')

# Dose frequency mapping
dose_map = {'1':'Daily', '2':'2x Daily', '0.5':'Half', '3':'3x', '1.5':'1.5x'}
meds['dose_freq'] = meds['Amount'].astype(str).map(dose_map).fillna('Other')

# Streak prep
meds = meds.sort_values('date')
meds['meds_today'] = meds.groupby('date')['Medication'].transform('count') > 0
meds.to_csv('meds_viz_ready.csv', index=False)
