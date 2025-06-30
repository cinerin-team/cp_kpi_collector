import re


def extract_kpi_entries(line, cp_name, build, job, tcid):
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
        entries.append([build, job, tcid, cp_name, kpi, actual_value, result, range_min, range_max])
    return entries

def process(log_folder):
    with open(log_folder + "/test_details.txt", encoding='utf-8') as f2:
        lines = f2.readlines()

    for line in lines:
        line = line.rstrip()
        for m in re.finditer(
                r'\s*Testcase id: ([A-Z0-9\.]+)', line
        ):
            tcid = m.group(1)
        for m in re.finditer(
                r'\s*Job id: ([0-9]+)', line
        ):
            job = m.group(1)

    with open(log_folder + "/verdict.log", encoding='utf-8') as f:
        lines = f.readlines()

    start_parsing = False
    results = []
    cp_name = None

    for line in lines:
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
            results.extend(extract_kpi_entries(line, cp_name, build, job, tcid))
        elif cp_name:
            results.extend(extract_kpi_entries(line, cp_name, build, job, tcid))
    return results
