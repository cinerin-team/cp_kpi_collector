import re


def extract_kpi_entries(line, cp_name, build):
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
        entries.append([build, cp_name, kpi, actual_value, result, range_min, range_max])
    return entries

def process(input_string):
    start_parsing = False
    results = []
    cp_name = None

    for line in input_string:
        line = line.rstrip()
        if not start_parsing:
            for m in re.finditer(
                    r'Build ID is ([A-Z0-9]+)', line
            ):
                build = m.group(1)
            if line.startswith("Testcases (None)"):
                start_parsing = True
            continue

        # Szóközök eltávolítása az elejéről, hogy biztosan felismerjük a CP-t
        stripped_line = line.lstrip()
        if stripped_line.startswith("TC"):
            cp_name = stripped_line.split()[0]
            results.extend(extract_kpi_entries(line, cp_name, build))
        elif cp_name:
            results.extend(extract_kpi_entries(line, cp_name, build))
    return results
