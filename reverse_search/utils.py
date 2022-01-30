import csv
import sys


maxInt = sys.maxsize

while True:
    # decrease the maxInt value by factor 10
    # as long as the OverflowError occurs.

    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)


def csv_from_tsv(filename, output_filename):
    with open(filename) as tf:
        reader = csv.DictReader(tf, delimiter="\t")
        with open(output_filename, "w", newline=str()) as cf:
            writer = csv.DictWriter(cf, fieldnames=reader.fieldnames)
            writer.writeheader()
            for row in reader:
                for k, v in row.items():
                    if v == r"\N":
                        row[k] = None
                writer.writerow(row)
