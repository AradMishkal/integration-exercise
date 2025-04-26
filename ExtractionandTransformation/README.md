# Extraction and Transformation

This script downloads an inventory file from a link, processes it based on a list of rules, and saves a cleaned version to a CSV file.

## How to run

1. Install the required libraries on your IDE
2. Run the script: 'python process_inventory.py'
3. Once you run the code, it will ask you if you want to store the original file locally, give yes/no input
4. The script applies all required processing rules and saves the final clean data as 'output.csv'

## Notes

1. During the initial parsing of the CSV, duplicate column headers were identified.
Instead of overwriting or losing information, the script renames duplicates automatically by appending suffixes like:

Store_ID

Store_ID_dup1

Store_ID_dup2

Store_ID_dup3

Store_ID_dupN

...and so on for other duplicate columns

2. As part of the data integrity check, additional logic was implemented:

For duplicated fields (e.g., Store_ID, Store_ID_dup2, Store_ID_dup5, Store_ID_dup6), the script counts:

How many unique (distinct) values each column contains.

This helped compare columns and identify which one had more distinct information, indicating where better data quality exists.

3. I noticed the file path parts like '_utils' and 'inventory_export_sample_exercise.csv' needed a '/' between them
I updated the code to grab all the correct <span> parts and join them with '/', building the full S3 path properly.