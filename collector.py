import csv

from configs import log_folder, output_file
from functions import process

with open(log_folder + "/verdict.log", encoding='utf-8') as f:
    lines = f.readlines()

results = process(lines)

with open(output_file, "w", newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["Build", "CP", "KPI", "Actual value", "Result", "Range min", "Range max"])
    writer.writerows(results)

print(f"Kész! Eredmény: {output_file}")
