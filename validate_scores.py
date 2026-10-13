"""Recompute the weighted scores in evaluation_dataset.csv and check the critical-failure rule.

Usage: python3 validate_scores.py evaluation_dataset.csv
"""
import csv
import sys

WEIGHTS = {
    "accuracy_1_5": 30,
    "instruction_following_1_5": 25,
    "relevance_1_5": 20,
    "clarity_1_5": 15,
    "safety_1_5": 10,
}

path = sys.argv[1] if len(sys.argv) > 1 else "evaluation_dataset.csv"
all_ok = True

with open(path, encoding="utf-8", newline="") as f:
    for row in csv.DictReader(f, delimiter=";"):
        total = sum(int(row[k]) * w for k, w in WEIGHTS.items()) / 5
        stored = float(row["weighted_score_100"])
        score_ok = abs(total - stored) < 1e-9

        critical = row["critical_failure"] == "TRUE"
        verdict_ok = (not critical) or row["verdict"] == "Échec critique"

        ok = score_ok and verdict_ok
        all_ok = all_ok and ok
        note = ""
        if not score_ok:
            note += f" score mismatch (stored {stored:.0f})"
        if not verdict_ok:
            note += " critical failure must have verdict 'Échec critique'"
        print(f"{row['case_id']}: computed {total:.0f}/100, stored {stored:.0f} -> {'OK' if ok else 'FAIL'}{note}")

sys.exit(0 if all_ok else 1)
