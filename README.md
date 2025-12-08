# Markdown-Notes-Processing-and-Analysis
This is a personal project that tackles extracting meaningful data from my personal Obsidian vault. In my vault I have tracked medication, meal and sleep times and some other specifics through multiple daily notes templates. Data Extraction and some Transformation handled with Python. Excel, Tableau, PowerBI for visualisation and further analysis.

## Introduction

Over the past few years I have been using the popular Markdown editor, Obsidian, to keep track of medically useful information about myself. This has been useful to check for example whether I have taken my medication today or when I last ate.

The usefulness of the Obsidian Vault~

capitalise on the skills learnt through this Just-IT Data Skills Bootcamp in order to consolidate the source dataset, extracting three key tables (medication, diet, sleep quality) of consolidated information for further analysis.

    Extract
    Transform
    Load
    Verify (Integrity + Validity)
    can analyse how long from serving did I start eating, how long to finish (any relationship between longer between serving and starting, and length taken)

## Extract

There are over 1500 markdown files in my 'mobile-notes-dataset' from which to extract data, My process and approach has evolved since the beginning, and thus there are different templates used and information to extract between different time periods. This means that not only will I have to implement a specific data extraction script for each area data is tracked for, but that those scripts must be able to handle the different forms used between templates without breaking or giving faulty data.
Transform & Load

Once the data has been succesfully extracted from the 1500~ markdown files into just three csv files, medication.csv, wake_time.csv and dietary.csv, these tables can then be imported into either Excel or PowerBI for transform the extracted data into a usable form. Some of the transformations that I will need to do include:

    filter/delete rows with blank/null values for essential fields
    handle non-standard inputs for time field and dosage field in medication table
        time field contains multiple csv delimmited times
            duplicate row for each time listed
            ensure duplicated rows have correct dosages, sometimes 1/2 or 3/2 initial
        dosage field contains units, non-standard measurements such as 1 tablet
            handle dosage multiplication such that only numerical value multiplied
            handle units, either pull into column if can consolidate or find other solution
    continously verify data validity and integrity against expectations, until all non-standard values are handled
    consider filling in missing meal times using images
        consider how to handle meals with only times vs ones with all ingredients

At this stage it will become clear what other transformations need to be carried out before Loading the data into PowerBI or Tableau for visualisation purposes.
