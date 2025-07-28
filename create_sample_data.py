#!/usr/bin/env python3
"""
Create sample Excel data for testing the simplified task analysis system
"""
import csv
import json

# Sample data based on the user's provided format
sample_data = [
    {
        "REGION": "Southern Region",
        "TASK ASSIGNED": "Meter Servicing",
        "EXACT LOCATION": "Muchungucha",
        "CUSTOMER CONNECTION NUMBER": "1509000792"
    },
    {
        "REGION": "Southern Region", 
        "TASK ASSIGNED": "Meter Servicing",
        "EXACT LOCATION": "Muchungucha",
        "CUSTOMER CONNECTION NUMBER": "02312893"
    },
    {
        "REGION": "Northern Region",
        "TASK ASSIGNED": "Leak Repair",
        "EXACT LOCATION": "Karura",
        "CUSTOMER CONNECTION NUMBER": "1234567"
    },
    {
        "REGION": "Eastern Region",
        "TASK ASSIGNED": "Valve Replacement", 
        "EXACT LOCATION": "Embakasi",
        "CUSTOMER CONNECTION NUMBER": "9876543"
    },
    {
        "REGION": "Southern Region",
        "TASK ASSIGNED": "Meter Relocation",
        "EXACT LOCATION": "Karen",
        "CUSTOMER CONNECTION NUMBER": "5555555"
    },
    {
        "REGION": "Northern Region",
        "TASK ASSIGNED": "Meter Servicing",
        "EXACT LOCATION": "Kasarani",
        "CUSTOMER CONNECTION NUMBER": "7777777"
    },
    {
        "REGION": "Eastern Region",
        "TASK ASSIGNED": "Leak Repair",
        "EXACT LOCATION": "Donholm",
        "CUSTOMER CONNECTION NUMBER": "8888888"
    },
    {
        "REGION": "Western Region",
        "TASK ASSIGNED": "Meter Servicing",
        "EXACT LOCATION": "Kangemi",
        "CUSTOMER CONNECTION NUMBER": "9999999"
    },
    {
        "REGION": "Southern Region",
        "TASK ASSIGNED": "Valve Replacement",
        "EXACT LOCATION": "Langata",
        "CUSTOMER CONNECTION NUMBER": "1111111"
    },
    {
        "REGION": "Northern Region",
        "TASK ASSIGNED": "Meter Servicing",
        "EXACT LOCATION": "Githurai",
        "CUSTOMER CONNECTION NUMBER": "2222222"
    }
]

def create_csv_file():
    """Create a CSV file with sample data"""
    with open('/workspace/sample_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        if sample_data:
            fieldnames = sample_data[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(sample_data)
    print("Created sample_data.csv")

def analyze_data():
    """Simple analysis of the sample data"""
    # Task assignment analysis
    task_counts = {}
    region_counts = {}
    
    for row in sample_data:
        task = row["TASK ASSIGNED"]
        region = row["REGION"]
        
        task_counts[task] = task_counts.get(task, 0) + 1
        region_counts[region] = region_counts.get(region, 0) + 1
    
    print("\n=== TASK ASSIGNMENT ANALYSIS ===")
    print("Task Assignment\t\tHow Many")
    print("-" * 40)
    for task, count in sorted(task_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"{task:<20}\t{count}")
    
    print("\n=== REGION ANALYSIS ===")
    print("Region\t\t\tHow Many Tasks")
    print("-" * 40)
    for region, count in sorted(region_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"{region:<20}\t{count}")
    
    # Create summary JSON
    summary = {
        "task_data": [{"Task_Assignment": k, "How_Many": v} for k, v in sorted(task_counts.items(), key=lambda x: x[1], reverse=True)],
        "region_data": [{"REGION": k, "How_Many_Tasks": v} for k, v in sorted(region_counts.items(), key=lambda x: x[1], reverse=True)]
    }
    
    with open('/workspace/sample_analysis.json', 'w') as f:
        json.dump(summary, f, indent=2)
    print("\nCreated sample_analysis.json")
    
    return summary

if __name__ == "__main__":
    create_csv_file()
    summary = analyze_data()
    print(f"\nTotal task types: {len(summary['task_data'])}")
    print(f"Total regions: {len(summary['region_data'])}")
    print(f"Total tasks: {sum(item['How_Many'] for item in summary['task_data'])}")