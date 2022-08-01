import pandas as pd
from collections import defaultdict
from functools import partial
import re

violations_re = r'(?P<code>\d+)\. (?P<desc>[^|]+) |'
DESC_IGNORE_LIST = []
#     "CRITICAL VIOLATION",
#     "CRITICAL VIOLATION 7-38-005A.",
#     "CRITICAL VIOLATION:7-38-005(A)",
#     "(CRITICAL 7-38-005A)",
#     "CRITICAL CITATION ISSUED, 7-38-005(A).",
#     "CRITICAL VIOLATION 7-38-005(A)",
#     "Critical violation 7-38-005(a).",
#     "CRITICAL VIOLATION 7-38-005A",
#     "CRITICAL VIOLATION: 7-38-005(A)",
#     "SERIOUS VIOLATION",
#     "(CRITICAL 7-38-005A).",
#     "CRITICAL",
#     "CITATION ISSUED #7-38-005(A).",
#     "CRITICAL CITATION ISSUED 7-38-005 (A).",
#     "SERIOUS VIOLATION 7-38-005A.",
#     "CRITICAL CITATION ISSUED",
#     "Critical citation issued 7-38-005(A).",
#     "CRITICAL CITATION ISSUED 7-38-005(A)",
#     "CITATION ISSUED.",
#     "MUST",
#     "MUST PROVIDE.",
#     "NO CITATION",
#     "CITATION",
#     "NO CITATION ISSUED.",
#     "MUST CLEAN AND",
#     "NO CITATION.",
#     "MUST CLEAN AND MAINTAIN",
#     "CRITICAL CITATION ISSUED 7-38-005(A).",
#     "CRITICAL VIOLATION 7-38-005 (A)",
#     "CRITICAL VIOLATION 7-38-005(A).",
#     "CRITICAL VIOLATION 7-38-005B.",
#     "CRITICAL VIOLATION:7-38-005(A).",
#     "VIOLATION CORRECTED.",
#     "VIOLATION CORRECTED AND ABATED.",
#     "SERIOUS VIOLATION CORRECTED",
#     "CRITICAL VIOLATION: 7-38-005(A).",
#     "CITATION ISSUED",
#     "SERIOUS CITATION ISSUED.",
#     "SERIOUS VIOLATION CORRECTED.",
#     "CRITICAL CITATION ISSUED 7-38-005.",
#     "CRITICAL VIOLATION 7-38-005 (A).",
#     "CRTICAL VIOLATION 7-38-005A",
#     "CITATION ISSUED #7-38-005(A)",
#     "CITATION ISSUED CRITICAL",
#     "CORRECTED",
#     "COURT DATE 11.18.10, 400 W SUPERIOR, ROOM 112, 10 AM.",
#     "CRITICAL 7-38-005 (A) ISSUED.",
#     "CRITICAL 7-38-005(A) ISSUED.",
#     "CRITICAL 7-38-005(A).",
#     "CRITICAL CITATION #7-38-005(A).",
#     "CRITICAL CITATION 7-38-005(A)",
#     "CRITICAL CITATION ISSUED #7-38-005(A).",
#     "CRITICAL CITATION ISSUED 7-38-005(A.",
#     "CRITICAL CITATION ISSUED, 7-38-005(A)",
#     "CRITICAL CITATION ISSUED, 7-38-005[A].",
#     "CRITICAL CITATION ISSUED.",
#     "CRITICAL CITATION ISSUED. 7-38-005(A).",
#     "CRITICAL VIOLATION 7-38-005",
#     "CRITICAL VIOLATION 7-38-005 (B).",
#     "CRITICAL VIOLATION 7-38-005.",
#     "CRITICAL VIOLATION 7-38-005(A) ISSUED.",
# ]

def pull_violations(violations_dict, row):
    violations_col = row['Violations']
    cleaned_violations_col = re.sub("\s+", " ", str(violations_col))
    cleaned_violations_col = cleaned_violations_col.replace("- Comments", "|")
    
    match_info = re.finditer(violations_re, cleaned_violations_col)
    acc = ""
    for match in match_info:
        code = match.group('code')
        desc = match.group('desc')
        if code and desc:
            if desc not in DESC_IGNORE_LIST:
                violations_dict[code].add(desc)
                acc += f"{code}: {desc}\n"
    return acc

if __name__ == "__main__":
    df = pd.read_csv('Food_Inspections.csv')
    violations = defaultdict(set)
    df['pulled_violations'] = df.apply(partial(pull_violations, violations), axis=1)
    df.to_csv('cleaned_violations.csv')
    codes = sorted(violations.keys())
    print("code\tdescription")
    for code in codes:
        for desc in violations[code]:
            print(f"{code}\t{desc}")
