import configparser
import csv

from functions import process

used_config = 'TC37548.5.6.2.config'

config = configparser.ConfigParser()
config.read(used_config)

log_folder = config['files']['log_folder']
output_file = config['files']['output_file']

with open(log_folder + "/verdict.log", encoding='utf-8') as f:
    lines = f.readlines()

results = process(log_folder)

with open(output_file, "w", newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["Build", "Job", "Test Case Id", "CP", "KPI", "Actual value", "Result", "Range min", "Range max"])
    writer.writerows(results)

print(f"Kész! Eredmény: {output_file}")
