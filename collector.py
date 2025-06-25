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
    # Több KPI is lehet egy sorban, vesszővel vagy "AND"-del elválasztva
    entries = []
    # Minden KPI-mintát kigyűjtünk a sorból
    # Példa regex: reporting_ebm_60m_...([érték]) inbetween 11 and 22
    # vagy ... not inbetween ...
    for m in re.finditer(r"([^\(]+)\(\[([^\]]+)\]\)\s+(inbetween|not inbetween)\s+([-\d.]+)\s+and\s+([-\d.]+)", line):
        kpi = m.group(1).strip()
        actual_value = m.group(2).strip()
        # Eredményt most a value és a tartomány alapján számoljuk:
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
    line = line.strip()
    if not start_parsing:
        if line.startswith("Testcases (None)"):
            start_parsing = True
        continue

    # Csak olyan sor, amely " TC"-vel kezdődik, lehet CP (figyelj a szóközre!)
    if line.startswith("TC"):
        cp_name = line.split()[0]
        # Ebben a sorban lehetnek KPI-k is:
        results.extend(extract_kpi_entries(line, cp_name))
    elif cp_name:
        # Egyéb KPI sorok:
        results.extend(extract_kpi_entries(line, cp_name))

with open(output_file, "w", newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["CP", "KPI", "Actual value", "Result", "Range min", "Range max"])
    writer.writerows(results)

print(f"Kész! Eredmény: {output_file}")
