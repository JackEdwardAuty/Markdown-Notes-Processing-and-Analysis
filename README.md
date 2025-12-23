# Markdown-Notes-Processing-and-Analysis
This is a personal project that tackles extracting meaningful data from my personal Obsidian vault. In my vault I have tracked medication, meal and sleep times and some other specifics through multiple daily notes templates. Data Extraction and some Transformation handled with Python. Excel, Tableau, PowerBI for visualisation and further analysis.

## Introduction

Over the past few years I have been using the popular Markdown editor, Obsidian, to keep track of medically useful information about myself. This has been useful to check for example whether I have taken my medication today or when I last ate.

## Visualisation & Analysis

Here is a screenshot of the final Tableau Dashboard used in my graduation:
![Tableau Dashboard Screenshot](https://github.com/JackEdwardAuty/Markdown-Notes-Processing-and-Analysis/blob/main/Tableau%20Dashboard.png)

Here is a [link to the live dashboard](https://public.tableau.com/views/TableauVisualisationExplore/MedicationTimingWakePatternsandAdheranceStreaks), GitHub doesn't allow embed.

## The usefulness of the Obsidian Vault

An Obsidian vault is essentially a library of markdown files that can be used for whatever purpose the user desires. By default, Obsidian follows standard Markdown format and provides useful tools through core and community plugins such as Backlinks, Templates and Daily Notes which I used extensively when creating the source dataset for this project, along with a Graph View which gives a visual representation of how the vault files link together.

## Process (Overview)

 - Extract
   - Over 1500 Markdown files down to just 2, using custom File-Handling approach and regex table extraction
 - Transform
   - Exclude null rows,
   - Seven additional regex patterns to normalise
     - Non-standard dosage values, dose multiplication, unit Extraction
     - Mid-points from time ranges and Comma delimited row duplication
     - Private row flagging for public/private output split
 - Load
   - Calculated fields by processing output 2 CSV files through additional Python scripts (in folder)
   - Loaded into Tableau and linked on primary key 'filename'
   
 - Verify (Integrity + Validity)
   - Manual and programmatic verification

 - Visualise
   - [Tableau Dashboard created](https://public.tableau.com/views/TableauVisualisationExplore/MedicationTimingWakePatternsandAdheranceStreaks)
 - Analyse
   - Dose Time against Wake Time Using RUNNING_SUM method
     - Found that most consistently took XR medication at 8 AM and 9 AM
     - More likely to take (late-day) Ritalin IR the earlier I woke up
   - Count Daily Meds by Hour Taken
     - Stayed consistent with Fexofenadine whether woke up too late for Ritalin XR
     - Confirmation of 8-9 AM consistency

   - Variation in Dose Hour
     - Box-and-Whisker showing distribution

   - Streak Counter by Band
     - Longest XR medication streak was 29 days in a row
     - Ritalin IR was rarely taken multiple days in a row
   - Med Streak by Wake Hour
     - Longest runs (most consistent distribution) occurs when I wake between 8-10am

 - Potential Future Steps
   - Implement Meal Time Extraction 
     - Analyse how long from serving did I start eating, how long to finish
       - Any relationship between longer between serving and starting, and length taken?
     - Any relationship between wake time and meal distribution?
     - How about between medication adherance and meal distribution and length?

### Extract

There are over 1500 markdown files in my `mobile-notes-dataset` from which to extract data, My process and approach has evolved since the beginning, and thus there are different templates used and information to extract between different time periods. This means that not only will I have to implement a specific data extraction script for each area data is tracked for, but that those scripts must be able to handle the different forms used between templates without breaking or giving faulty data.

### Transform & Load

Once the data has been succesfully extracted from the 1500~ markdown files into just three CSV files, `medication.csv`, `wake_time.csv` and `dietary.csv`, these files can then undergo transformation into usable form using either Excel (manual), PowerBI (step-wise) or with my choice - Python.

The necessary transformations implemented are:
- Filters/deletes rows with blank/null values in essential fields (e.g. missing drug name, time, or dosage)
- Normalises medication dosage from non-standard formats:
  - `2x18mg` → `36mg` (multiplicative parsing)
  - `1 (tab)` → drug-specific mg (e.g. Paracetamol=`500mg`, Fexofenadine=`120mg`)
  - `1.5x 500mg` → `750mg`
  - Handles ml units or no units (assumes standard dose)
    - Handle string units by pulling into new column
- Splits comma-separated times into multiple rows, meta info should be used to adjust dosage:
  - `15:25, 19:40` → two rows with same dosage
  - `17:15, 21:35 (half)` → duplicates row, applies half dosage to second time
- Converts time ranges to midpoint:
  - `09:45-50` → `09:47`
- Flags non-standard formats or errors in new `notes` column:
  - e.g. `nonstd:08;00` for input errors like semicolons
  - Enables manual review of edge cases
- Ensures data validity/integrity via continuous verification against expectations
 
Prepares clean tables for import into PowerBI/Tableau visualisation.

To implement these Transformations, I introduce three new methods:
 - `parse_dosage_string(dosage_str, factor=1.0)`
 - `parse_time_value(time_str)`
 - `split_times_to_rows(dataframe)`


## Loading (then extracting) the Data from the markdown mobile-notes-dataset

The first step in my project is to load the markdown files from their non-standard folder structure, handling duplicates and empty templates, ensuring all files in the dataset are utilised and imported for use in further programmatic handling.

### File Handling Approach

Libraries: `os`, `re`, `pandas`, `pathlib`

Methods: 
 - `list_md_files(folder)`

### Defining Communal Methods

Libraries: above + `datetime`

Methods:
 - `full_path(mobile_notes_directory, file)`
 - `read_file(full_path)`
 - `extract_date(filename)`
 - `find_section_positions(content, header_regex)`
 - `extract_table_lines(lines, start_idx, end_idx = None)`
 - `parse_markdown_table(table_lines)`
 - `get_file_info(file)`
 - `process_file_headers(date, filename, folder, content, lines)`

## Extracting the Wake Times from the Dataset

Methods:
 - `extract_wake_times(section_headers, file_info)`

Expected Output:

    '[{'Sleep': '~',
       'Wake': '14:45',
       'Time': '',
       'Quality': 'Decent',
       'date': '2025-11-30',
       'filename': '2025-11-30.md',
       'folder': '2025-11',
       'section_type': 'Wake+Sleep'}]'

## Extracting Medication Details from the Dataset

Methods:
 - `extract_med_times(section_headers, file_info)`

Expected Output:

    '[{'Time': '17:09',
       'Medication': 'Ritalin IR',
       'Dosage': '5mg',
       'date': '2025-11-30',
       'filename': '2025-11-30.md',
       'folder': '2025-11',
       'section_type': 'Prescription'},
      {'Time': '17:09',
       'Medication': 'Fexofenadine',
       'Dosage': '120mg',
       'date': '2025-11-30',
       'filename': '2025-11-30.md',
       'folder': '2025-11',
       'section_type': 'OTC'}]'

## Extract Meal Details from the Dataset

> Left for a future project iteration, priority is skills demonstration.

## Outputting to CSV

 - Output script utilising `Pandas` `Dataframe` `.to_csv`

Expected Output:

    Processing 1513 markdown files...
    
    Saved wake_time.csv with 118 rows
    
    Saved medication.csv with 901 rows

## Transforming the Dataset

Methods:
 - `parse_dosage(dosage_str, factor=1.0)`
 - `parse_time_value(time_str)`
 - `split_times_to_rows(dataframe)`
 
## Process Medication CSV file to give new outputs

Methods:
 - `handle_transformations(input_file, output_file_personal, output_file_public)`

Expected Output:

    📖 Reading /content/drive/MyDrive/Colab Notebooks/Markdown Processing Dataset/Output/medication.csv...
    
    901 rows before splitting
    
        SKIP unparsed dosage: Amount at time Time
        SKIP unparsed dosage: ------ at time ----
        SKIP unparsed dosage: Dosage at time Time
        SKIP unparsed dosage: --------- at time ------
        SKIP unparsed dosage: Amount at time Time
        SKIP unparsed dosage: ------ at time ----
        SKIP unparsed dosage: Dosage at time Time
        SKIP unparsed dosage: Amount at time Time
        SKIP unparsed dosage: 23:27 at time 23:20
        SKIP unparsed dosage: 660 EPA, 440 DHA, 1100mg Omega 3 at time 14:20
        
    ✅ 962 rows after splitting
    Split 62 multi-time rows
    7 rows with notes/flags
    
    💾 Saved full to /content/drive/MyDrive/Colab Notebooks/Markdown Processing Dataset/Output/medication_expanded_private.csv
    💾 Saved public set to /content/drive/MyDrive/Colab Notebooks/Markdown Processing Dataset/Output/medication_expanded_public.csv

    🔍 First 10 rows preview:
    Time                                       Medication Dosage  Amount Unit Notes
    03:30                                      Ritalin IR    5mg     5.0   mg      
    03:30                                    Fexofenadine  120mg   120.0   mg      
    00:10                                      Ritalin IR    5mg     5.0   mg      
    00:10                                    Fexofenadine  120mg   120.0   mg      
    04:00                                     Paracetamol 1000mg  1000.0   mg      
    03:37                                 Magnesium Oxide  500mg   500.0   mg      
    15:00 Flu Plus (phenylephrine, paracetamol, caffeine)  2tabs     2.0 tabs      
    10:40                                      Ritalin XR   36mg    36.0   mg      
    08:55                                    Fexofenadine  120mg   120.0   mg      
    13:15                                      Ritalin XR   36mg    36.0   mg      
