# Markdown-Notes-Processing-and-Analysis
This is a personal project that tackles extracting meaningful data from my personal Obsidian vault. In my vault I have tracked medication, meal and sleep times and some other specifics through multiple daily notes templates. Data Extraction and some Transformation handled with Python. Excel, Tableau, PowerBI for visualisation and further analysis.

## Introduction

Over the past few years I have been using the popular Markdown editor, Obsidian, to keep track of medically useful information about myself. This has been useful to check for example whether I have taken my medication today or when I last ate.

## Visualisation & Analysis

![Tableau Dashboard Screenshot](link_to_screenshot)

![Tableau Dashboard Embed](link_to_embed)

## The usefulness of the Obsidian Vault

An Obsidian vault is essentially a library of markdown files that can be used for whatever purpose the user desires. By default, Obsidian follows standard Markdown format and provides useful tools through core and community plugins such as Backlinks, Templates and Daily Notes which I used extensively when creating the source dataset for this project, along with a Graph View which gives a visual representation of how the vault files link together.

 - Extract
 - Transform
 - Load
 - Verify (Integrity + Validity)
 - Visualise
 - Analyse
    - can analyse how long from serving did I start eating, how long to finish (any relationship between longer between serving and starting, and length taken)

## Extract

There are over 1500 markdown files in my 'mobile-notes-dataset' from which to extract data, My process and approach has evolved since the beginning, and thus there are different templates used and information to extract between different time periods. This means that not only will I have to implement a specific data extraction script for each area data is tracked for, but that those scripts must be able to handle the different forms used between templates without breaking or giving faulty data.

## Transform & Load

Once the data has been succesfully extracted from the 1500~ markdown files into just three csv files, 'medication.csv', 'wake_time.csv' and 'dietary.csv', these tables can then be imported into either Excel or PowerBI for transform the extracted data into a usable form. Some of the transformations that I will need to do include:

 - filter/delete rows with blank/null values for essential fields
 - handle non-standard inputs for time field and dosage field in medication table
    - time field contains multiple csv delimmited times
       - duplicate row for each time listed
       - ensure duplicated rows have correct dosages, sometimes 1/2 or 3/2 initial
    - dosage field contains units, non-standard measurements such as 1 tablet
       - handle dosage multiplication such that only numerical value multiplied
       - handle units, either pull into column if can consolidate or find other solution
 - continously verify data validity and integrity against expectations, until all non-standard values are handled
 - consider filling in missing meal times using images
    - consider how to handle meals with only times vs ones with all ingredients

At this stage it will become clear what other transformations need to be carried out before Loading the data into PowerBI or Tableau for visualisation purposes.

## Loading (then extracting) the Data from the markdown mobile-notes-dataset

The first step in my project is to load the markdown files from their non-standard folder structure, handling duplicates and empty templates, ensuring all files in the dataset are utilised and imported for use in further programmatic handling.

### File Handling Approach

Libraries: os, re, pandas, pathlib

Methods: 
 - 'list_md_files(folder)'

### Defining Communal Methods

Libraries: above + datetime

Methods:
 - full_path(mobile_notes_directory, file)
 - read_file(full_path)
 - extract_date(filename)
 - find_section_positions(content, header_regex)
 - extract_table_lines(lines, start_idx, end_idx = None)
 - parse_markdown_table(table_lines)
 - get_file_info(file)
 - process_file_headers(date, filename, folder, content, lines)

## Extracting the Wake Times from the Dataset

Methods:
 - extract_wake_times(section_headers, file_info)

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
 - extract_med_times(section_headers, file_info)

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

 - Output script utilising Pandas Dataframe '.to_csv'

Expected Output:
    Processing 1513 markdown files...
    Saved wake_time.csv with 118 rows
    Saved medication.csv with 901 rows

## Transforming the Dataset

Methods:
 - parse_dosage(dosage_str, factor=1.0)
 - parse_time_value(time_str)
 - split_times_to_rows(dataframe)
 
## Process Medication CSV file to give new outputs

Methods:
 - handle_transformations(input_file, output_file_personal, output_file_public)

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
