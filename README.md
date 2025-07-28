# Simplified Task Analysis System

A streamlined application for analyzing task assignments and regional distribution from Excel data.

## What It Does

This simplified system focuses on two main analyses:

1. **Task Assignment Analysis**: Counts and analyzes different task types (like "Meter Servicing") showing:
   - Task Assignment name
   - How Many tasks of each type
   - Percentage distribution

2. **Region Analysis**: Analyzes task distribution by regions showing:
   - Region name
   - How Many Tasks in each region
   - Percentage distribution

## Features

- ✅ **Simplified Data Processing**: Focuses only on task assignments and regions
- ✅ **No Raw Data Confirmation**: Directly processes and shows results
- ✅ **Excel Reports**: Generates Excel files with embedded charts
- ✅ **Visual Charts**: Interactive charts for both task and region analysis
- ✅ **Clean Interface**: Simple upload and results display

## How to Use

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Application
```bash
python main.py
```

The application will start on `http://localhost:8000`

### 3. Upload Your Excel File
- Open your browser and go to `http://localhost:8000`
- Upload an Excel file (.xlsx or .xls)
- Your file should have columns for:
  - `REGION` (or similar) - for regional analysis
  - `TASK ASSIGNED` (or similar) - for task assignment analysis

### 4. View Results
- The system will automatically process your data
- You'll see:
  - Summary overview with counts
  - Task Assignment table and chart
  - Region Analysis table and chart
  - Download options for Excel reports

### 5. Download Reports
- **Excel Report**: Complete report with embedded charts
- **Charts Data**: JSON data for the charts

## File Structure

```
/workspace/
├── main.py                 # Main FastAPI application
├── utils/
│   ├── file_processor.py   # Simplified data processing
│   └── report_generator.py # Excel report generation
├── templates/
│   ├── index.html          # Upload page
│   └── results.html        # Results display
├── requirements.txt        # Dependencies
└── README.md              # This file
```

## Excel File Requirements

Your Excel file should contain:

- **Region Column**: Any column with "region" in the name (case-insensitive)
- **Task Assignment Column**: Any column with "task" and "assign" in the name (case-insensitive)

Example columns that will work:
- `REGION`, `Region`, `REGION_NAME`
- `TASK ASSIGNED`, `Task Assignment`, `TASK_ASSIGNED`

## Sample Output

### Task Assignment Analysis
| Task Assignment | How Many | Percentage |
|----------------|----------|------------|
| Meter Servicing | 45 | 65.2% |
| Leak Repair | 15 | 21.7% |
| Valve Replacement | 9 | 13.1% |

### Region Analysis
| Region | How Many Tasks | Percentage |
|--------|---------------|------------|
| Southern Region | 32 | 46.4% |
| Northern Region | 23 | 33.3% |
| Eastern Region | 14 | 20.3% |

## API Endpoints

- `GET /` - Upload page
- `POST /upload` - File upload and processing
- `GET /results?token={token}` - View results
- `GET /download/excel/{token}` - Download Excel report
- `GET /api/data/{token}` - Get data as JSON

## Changes Made from Original System

This simplified version:

1. **Removed complex service analysis** - focuses only on general task assignments
2. **Removed raw data confirmation** - directly shows processed results
3. **Simplified data structure** - only task assignments and regions
4. **Streamlined Excel reports** - two main sheets with embedded charts
5. **Cleaner interface** - focused on the essential functionality

The system now provides exactly what you requested: simple analysis of task assignments and regions with Excel reports containing embedded graphs.
