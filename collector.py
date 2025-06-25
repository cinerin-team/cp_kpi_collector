import re
import csv

input_file = 'input.txt'
output_file = 'output.csv'

start_parsing = False
results = []

with open(input_file, encoding='utf-8') as f:
    lines = f.readlines()

cp_name = None

def extract_kpi_entries(line, cp_name):
    entries = []
    # Az összes kpi([érték]) ... inbetween/not inbetween mintát megkeressük
    for m in re.finditer(
        r'([a-zA-Z0-9_-]+)\(\[([^\]]+)\]\)\s+(inbetween|not inbetween)\s+([-\d.]+)\s+and\s+([-\d.]+)', line
    ):
        kpi = m.group(1).strip()  # csak a KPI név
        actual_value = m.group(2).strip()
        try:
            val = float(actual_value)
            minval = float(m.group(4))
            maxval = float(m.group(5))
            result = "PASS" if minval <= val <= maxval else "FAIL"
        except Exception:
            result = "FAIL"
        range_min = m.group(4).strip()
        range_max = m.group(5).strip()
        entries.append([cp_name, kpi, actual_value, result, range_min, range_max])
    return entries

for line in lines:
    line = line.rstrip()
    if not start_parsing:
        if line.startswith("Testcases (None)"):
            start_parsing = True
        continue

    # Szóközök eltávolítása az elejéről, hogy biztosan felismerjük a CP-t
    stripped_line = line.lstrip()
    if stripped_line.startswith("TC"):
        cp_name = stripped_line.split()[0]
        results.extend(extract_kpi_entries(line, cp_name))
    elif cp_name:
        results.extend(extract_kpi_entries(line, cp_name))

with open(output_file, "w", newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["CP", "KPI", "Actual value", "Result", "Range min", "Range max"])
    writer.writerows(results)

print(f"Kész! Eredmény: {output_file}")
