import re
import csv

input_file = 'input.txt'
output_file = 'output.csv'

# Flag: csak a "Testcases (None)" után kezdünk dolgozni
start_parsing = False

results = []

with open(input_file, encoding='utf-8') as f:
    lines = f.readlines()

cp_name = None

for line in lines:
    line = line.strip()
    # Addig keresünk, amíg meg nem találjuk a start kulcssort
    if not start_parsing:
        if line.startswith("Testcases (None)"):
            start_parsing = True
        continue

    # Új CP kezdete, ami egy hosszú sor (és a sor első szava a CP neve)
    if line and not line.startswith(("reporting_", "status-detail_", "AND")):
        # A CP neve az első szó
        cp_name = line.split()[0]

    # KPI sorokat keresünk - csak akkor, ha már van CP
    if cp_name and (("inbetween" in line) or ("not inbetween" in line)):
        # Regex a KPI-hoz és az adatokhoz:
        # például: reporting_ebm_60m_ebm-server-name-1_up-ebm-stats_up-ebm-events([125842.62]) inbetween 110000 and 140000 AND
        m = re.match(r"([^\(]+)\(\[([^\]]+)\]\)\s+(inbetween|not inbetween)\s+([-\d.]+)\s+and\s+([-\d.]+)", line)
        if m:
            kpi = m.group(1).strip()
            actual_value = m.group(2).strip()
            result = "PASS" if m.group(3) == "inbetween" else "FAIL"
            range_min = m.group(4).strip()
            range_max = m.group(5).strip()
            results.append([cp_name, kpi, actual_value, result, range_min, range_max])

# Írás CSV-be
with open(output_file, "w", newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["CP", "KPI", "Actual value", "Result", "Range min", "Range max"])
    writer.writerows(results)

print(f"Kész! Eredmény: {output_file}")
