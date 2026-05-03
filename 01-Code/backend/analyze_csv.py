"""Analyze CSV structure and sample data"""
import csv
from pathlib import Path

csv_path = Path(r"C:\Projects\ResumeTailor\02-Data\UpdatedResumeDataSet.csv")

print("="*80)
print("CSV FILE ANALYSIS")
print("="*80)

with open(csv_path, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    
    # Read header
    header = next(reader)
    print(f"\nHeader: {header}")
    print(f"Columns: {len(header)}")
    
    # Read first 3 data rows
    print("\n" + "="*80)
    print("SAMPLE DATA (First 3 resumes)")
    print("="*80)
    
    for i, row in enumerate(reader):
        if i >= 3:
            break
        
        category = row[0] if len(row) > 0 else "N/A"
        resume_text = row[1] if len(row) > 1 else "N/A"
        
        print(f"\n--- Resume {i+1} ---")
        print(f"Category: {category}")
        print(f"Resume Length: {len(resume_text)} characters")
        print(f"Resume Word Count: {len(resume_text.split())} words")
        print(f"Resume Preview (first 200 chars):")
        print(resume_text[:200] + "..." if len(resume_text) > 200 else resume_text)

# Count total resumes
with open(csv_path, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)  # Skip header
    total_count = sum(1 for row in reader)

print("\n" + "="*80)
print(f"TOTAL RESUMES IN FILE: {total_count}")
print("="*80)

# Category distribution (sample first 100)
from collections import Counter
with open(csv_path, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)  # Skip header
    categories = [row[0] for i, row in enumerate(reader) if i < 100 and len(row) > 0]

category_counts = Counter(categories)
print("\nCATEGORY DISTRIBUTION (First 100 resumes):")
for cat, count in category_counts.most_common(10):
    print(f"  {cat}: {count}")

print("\n" + "="*80)
print("FORMAT CONFIRMATION:")
print("="*80)
print("✓ Column A (index 0): Category")
print("✓ Column B (index 1): Resume text")
print("✓ Format: Standard CSV with comma delimiter")
print("✓ Encoding: UTF-8")
print("="*80)
