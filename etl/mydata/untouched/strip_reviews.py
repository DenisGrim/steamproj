"""
def appIDTotalGet():
    results = []
    with open("reviews.csv", "r", encoding="utf-8") as f:
        next(f)  # skip header
        i = 1
        for line in f:
            parts = line.split(",")
            app_id = parts[0].strip('"')
            total = parts[5].strip('"')
            results.append((app_id, total))
            print(i)
            i += 1
    return results
    
    #import pandas as pd
    #df = pd.DataFrame(results, columns=["app_id", "total"])
""" 
import re

def appIDTotalGet():
    results = []
    with open("reviews.csv", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Remove newlines that are inside quoted fields
    content = re.sub(r'"[^"]*"', lambda m: m.group().replace('\n', ' '), content)
    
    lines = content.split('\n')
    for line in lines[1:]:  # skip header
        if not line.strip():
            continue
        parts = line.split(',')
        if len(parts) < 6:
            continue
        app_id = parts[0].strip('"')
        positives = parts[3].strip('"')
        total = parts[5].strip('"')
        results.append((app_id, positives, total))
    
    return results
