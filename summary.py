import operator
import pandas as pd
from collections import Counter
from tabulate import tabulate

def get_top_10_facility_types(df):
    primary_facility_type_counts = Counter(df['Facility Type'].explode())
    secondary_facility_type_counts = Counter(df['Facility Type Secondary'].explode())
    facility_type_counts = primary_facility_type_counts + secondary_facility_type_counts
    types_and_counts = facility_type_counts.most_common(10)
    return [key for (key, _) in types_and_counts]

def get_risk_counts_for_facility_types(df, facility_types):
    risk_counts = {}
    for facility_type in facility_types:
        selection = df[(df['Facility Type'] == facility_type) | (df['Facility Type Secondary'] == facility_type)]
        risk_counts[facility_type] = Counter(selection['Risk'].explode())
    return risk_counts

def summarize_risk(risk_counts):
    table = []
    for facility_type, counter in risk_counts.items():
        row = [facility_type]
        tot = counter[1] + counter[2] + counter[3]
        if tot == 0:
            continue
        for lvl in range(1, 4):
            row.append(counter[lvl] / tot)
        table.append(row)
    return tabulate(table, headers=["Facility Type", "Risk 1 %", "Risk 2 %", "Risk 3 %"], floatfmt=".2f")

def avg_risk(risk_counts):
    table = []
    for facility_type, counter in risk_counts.items():
        row = [facility_type]
        tot = sum([counter[lvl] for lvl in range(1,4)])
        if tot:
            row.append(sum(map(operator.mul, [1, 2, 3], [counter[lvl] for lvl in range(1,4)])) / tot)
            table.append(row)
    return tabulate(table, headers=["Facility Type", "Avg Risk"], floatfmt=".2f")



if __name__ == "__main__":
    df = pd.read_csv('Food-Inspections-csv.csv')
    top_10_facility_types = get_top_10_facility_types(df)
    risk_counts = get_risk_counts_for_facility_types(df, top_10_facility_types)
    print(avg_risk(risk_counts))