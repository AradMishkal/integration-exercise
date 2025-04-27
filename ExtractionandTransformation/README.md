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
   - Store_ID
   - Store_ID_dup1
   - Store_ID_dup2
   - Store_ID_dup3
   - Store_ID_dupN

   and so on for other duplicate columns

2. As part of the data integrity check, additional logic was implemented:
   - For duplicated fields (e.g., Store_ID, Store_ID_dup2, Store_ID_dup5, Store_ID_dup6), the script counts how many unique (distinct) values each column contains.
   - This helped compare columns and identify which one had more distinct information, indicating where better data quality exists.

## Data analysis summary
```
NULL counts for duplicate fields (grouped):

Field group: ItemNum
  ItemNum: 0 NULL values
  ItemNum_dup1: 2338 NULL values
  ItemNum_dup2: 3 NULL values
  ItemNum_dup3: 2491 NULL values
  ItemNum_dup4: 2493 NULL values
  ItemNum_dup5: 2295 NULL values

Field group: Store_ID
  Store_ID: 1 NULL values
  Store_ID_dup1: 2338 NULL values
  Store_ID_dup2: 3 NULL values
  Store_ID_dup3: 2491 NULL values
  Store_ID_dup4: 2493 NULL values
  Store_ID_dup5: 1 NULL values
  Store_ID_dup6: 1 NULL values
  Store_ID_dup7: 2295 NULL values

Field group: Price
  Price: 1 NULL values
  Price_dup1: 2491 NULL values

Field group: Dept_ID
  Dept_ID: 1 NULL values
  Dept_ID_dup1: 1 NULL values

Field group: Dirty
  Dirty: 1 NULL values
  Dirty_dup1: 1 NULL values

Field group: BarTaxInclusive
  BarTaxInclusive: 1 NULL values
  BarTaxInclusive_dup1: 1 NULL values

Field group: AvailableOnline
  AvailableOnline: 1 NULL values
  AvailableOnline_dup1: 1 NULL values

Field group: RowID
  RowID: 1 NULL values
  RowID_dup1: 1 NULL values

Field group: Description
  Description: 2493 NULL values
  Description_dup1: 1 NULL values


Comparing unique values for duplicate fields. 
For example -
Dept_ID has 10 unique non-NULL values
Dept_ID_dup1 has 10 unique non-NULL values
```