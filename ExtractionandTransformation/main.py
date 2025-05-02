import requests
from bs4 import BeautifulSoup
import csv
import json
from datetime import datetime
import io

initial_html_file = "https://bitbucket.org/cityhive/jobs/raw/master/integration-eng/integration-entryfile.html"
local_file_path = "inventory_export_sample_exercise.csv"


# Ask if you want to store the file locally
def get_store_locally_option():
    while True:
        store_locally_input = input("Do you want to store the file locally? (yes/no): ").strip().lower()
        if store_locally_input in ['yes', 'no']:
            return store_locally_input == 'yes'
        else:
            print("Invalid input. Please answer with 'yes' or 'no'.")


store_locally = get_store_locally_option()


# Process each line and implement the required sections
def process_line(line, itemnums) -> dict:
    tags = []

    # Section 7: Date check FIRST — early exit to save memory and time
    last_sold_str = str(line.get("Last_Sold", "")).strip()
    try:
        last_sold_date = datetime.strptime(last_sold_str, "%Y-%m-%d %H:%M:%S.%f")
        if last_sold_date.year != 2020:
            return None
    except ValueError:
        print("Non-relevant. Were not sold during 2020 ")
        return None

    # Section 3
    line["Department"] = str(line.get("Dept_ID", "")).strip()

    # Section 4
    itemnum = str(line.get("ItemNum", "")).strip()
    if not itemnum.isdigit() or len(itemnum) <= 5:
        line["ItemNum"] = ""
        line["internal_id"] = f'biz_id_{str(line.get("RowID", "")).strip()}'

    # Section 5
    try:
        cost = float(line.get("Cost", 0))
        price = float(line.get("Price", 0))

        if price > 0:
            margin = (price - cost) / price
            increase_percent = 0.07 if margin > 0.30 else 0.09
            new_price = round(price * (1 + increase_percent), 2)
            line["Price"] = f"{new_price:.2f}"
            # Section 9, assuming that the new margin is required to be used for the decision
            if margin > 0.30:
                tags.append("high_margin")
            elif margin < 0.30:
                tags.append("low_margin")
    except (ValueError, TypeError):
        # If cost or price isn't a valid number, just skip the update
        pass

    # Section 6
    item_name = str(line.get("ItemName", "")).strip()
    item_extra = str(line.get("ItemName_Extra", "")).strip()
    line["name"] = f"{item_name} {item_extra}"

    # Section 8
    properties = {
        "department": str(line.get("Dept_ID", "")).strip(),
        "vendor": str(line.get("Vendor_Number", "")).strip(),
        "description": str(line.get("Description_dup1", "")).strip(),
        # Decided to use Description_dup1 instead of Description_dup because it provides more unique values and less NULL
    }
    line["properties"] = json.dumps(properties)

    # Section 9 - Add 'duplicate_sku' to tags column
    if itemnum and itemnum in itemnums:
        tags.append("duplicate_sku")
    else:
        itemnums.add(itemnum)

    line["tags"] = ", ".join(tags)

    return line


# Get URL to download the CSV file
def get_s3_csv_url(html_url):
    response = requests.get(html_url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    bucket_tag = soup.find(id="bucket-value")
    region_tag = soup.find(id="region-value")
    object_tag = soup.find(id="object-value")

    if not bucket_tag or not region_tag or not object_tag:
        raise ValueError("Missing HTML elements (bucket, region, or object path)")

    bucket = bucket_tag.text.strip()
    region = region_tag["data-region"]

    path_spans = object_tag.find_all("span", class_="path", recursive=True)
    object_key_parts = [span.get_text(strip=True) for span in path_spans if not span.find("span")]
    object_key = "/".join(object_key_parts)

    return f"https://{bucket}.s3.{region}.amazonaws.com/{object_key}"


def download_csv_from_s3(s3_url, store_local, file_path=None):
    response = requests.get(s3_url)
    response.raise_for_status()
    csv_content = response.content.decode('utf-8')

    # Store the CSV locally or return as a stream
    if store_local:
        with open(file_path, "w") as f:
            f.write(csv_content)

        csv_stream = open(file_path)
        print(f"CSV file saved to {file_path}")
    else:
        csv_stream = io.StringIO(csv_content)
        print(f"CSV file loaded as a stream")
    return csv_stream


# Handle duplicate column names by adding a "_dupN"
def get_unique_fieldnames(reader):
    # Initialize a dictionary to track column names and their counts
    fieldnames = reader.fieldnames
    column_count = {}

    # Iterate over the fieldnames and add a suffix to duplicates
    for i, col in enumerate(fieldnames):
        if col in column_count:
            column_count[col] += 1
            fieldnames[i] = f"{col}_dup{column_count[col]}"
        else:
            column_count[col] = 0

    return fieldnames


def main():
    s3_url = get_s3_csv_url(initial_html_file)
    csv_stream = download_csv_from_s3(s3_url, store_locally, local_file_path)

    reader = csv.DictReader(csv_stream, delimiter='|')

    # Get the unique fieldnames
    modified_fieldnames = get_unique_fieldnames(reader)

    reader = csv.DictReader(csv_stream, delimiter='|', fieldnames=modified_fieldnames)

    next(reader)  # Skip the --- line

    # First pass to count ItemNum occurrences
    itemnums = set()
    output = []
    headers = set()

    # Process each row in the CSV
    for line in reader:
        processed = process_line(line, itemnums)
        if processed:
            print(processed)
            output.append(processed)
            # Add new columns to the headers
            headers.update(processed.keys())

    # Write the processed data to a new CSV file
    with open("output.csv", "w", newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(output)

    csv_stream.close()
    print("Finished!")


if __name__ == "__main__":
    main()
