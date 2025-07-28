import pandas as pd
import numpy as np
import os
import uuid
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64
from openpyxl import Workbook
from openpyxl.drawing.image import Image
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import BarChart, PieChart, Reference
from openpyxl.chart.marker import DataPoint
import logging

logger = logging.getLogger(__name__)

class ReportGenerator:
    def __init__(self):
        self.reports_dir = "reports"
        os.makedirs(self.reports_dir, exist_ok=True)
        
    def generate_excel_report(self, task_data: list, region_data: list, filename: str) -> str:
        """
        Generate simplified Excel report with task assignment and region analysis with embedded charts
        """
        try:
            # Create unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_filename = f"task_analysis_report_{timestamp}.xlsx"
            report_path = os.path.join(self.reports_dir, report_filename)
            
            # Create workbook
            wb = Workbook()
            
            # Remove default sheet
            wb.remove(wb.active)
            
            # Create the two main sheets as requested
            self._create_task_assignment_sheet(wb, task_data)
            self._create_region_analysis_sheet(wb, region_data)
            
            # Save workbook
            wb.save(report_path)
            
            logger.info(f"Simplified report generated successfully: {report_path}")
            return report_path
            
        except Exception as e:
            logger.error(f"Error generating Excel report: {str(e)}")
            raise Exception(f"Failed to generate report: {str(e)}")
    
    def _create_task_assignment_sheet(self, wb: Workbook, task_data: list):
        """Create Task Assignment sheet with embedded chart"""
        ws = wb.create_sheet("Task Assignment Analysis", 0)
        
        # Header styling
        header_font = Font(bold=True, size=12, color="FFFFFF")
        header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
        
        # Title
        ws['A1'] = "TASK ASSIGNMENT ANALYSIS"
        ws['A1'].font = Font(bold=True, size=16)
        ws['A1'].fill = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")
        ws['A1'].font = Font(bold=True, size=16, color="FFFFFF")
        ws.merge_cells('A1:C1')
        
        # Report date
        ws['A3'] = "Report Generated:"
        ws['B3'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Headers for task assignment table
        ws['A5'] = "Task Assignment"
        ws['A5'].font = header_font
        ws['A5'].fill = header_fill
        
        ws['B5'] = "How Many"
        ws['B5'].font = header_font
        ws['B5'].fill = header_fill
        
        # Add percentage column
        ws['C5'] = "Percentage"
        ws['C5'].font = header_font
        ws['C5'].fill = header_fill
        
        # Calculate total tasks for percentage
        total_tasks = sum(item['How_Many'] for item in task_data) if task_data else 0
        
        # Data rows
        for row, item in enumerate(task_data, start=6):
            ws[f'A{row}'] = item['Task_Assignment']
            ws[f'B{row}'] = item['How_Many']
            percentage = (item['How_Many'] / total_tasks * 100) if total_tasks > 0 else 0
            ws[f'C{row}'] = f"{percentage:.1f}%"
        
        # Create embedded chart
        if len(task_data) > 0:
            chart = BarChart()
            chart.title = "Task Assignment Distribution"
            chart.x_axis.title = "Task Type"
            chart.y_axis.title = "Number of Tasks"
            chart.height = 15  # Adjust chart height
            chart.width = 20   # Adjust chart width
            
            # Use top 10 tasks for better chart readability
            chart_data_length = min(len(task_data), 10)
            data_ref = Reference(ws, min_col=2, min_row=5, max_row=5+chart_data_length)
            categories_ref = Reference(ws, min_col=1, min_row=6, max_row=5+chart_data_length)
            
            chart.add_data(data_ref, titles_from_data=True)
            chart.set_categories(categories_ref)
            
            # Position chart to the right of the data
            ws.add_chart(chart, "E5")
        
        # Auto-adjust column widths
        self._adjust_column_widths(ws)
    
    def _create_region_analysis_sheet(self, wb: Workbook, region_data: list):
        """Create Region Analysis sheet with embedded chart"""
        ws = wb.create_sheet("Region Analysis")
        
        # Header styling
        header_font = Font(bold=True, size=12, color="FFFFFF")
        header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
        
        # Title
        ws['A1'] = "REGION ANALYSIS"
        ws['A1'].font = Font(bold=True, size=16)
        ws['A1'].fill = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")
        ws['A1'].font = Font(bold=True, size=16, color="FFFFFF")
        ws.merge_cells('A1:C1')
        
        # Report date
        ws['A3'] = "Report Generated:"
        ws['B3'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Headers for region table
        ws['A5'] = "Region"
        ws['A5'].font = header_font
        ws['A5'].fill = header_fill
        
        ws['B5'] = "How Many Tasks"
        ws['B5'].font = header_font
        ws['B5'].fill = header_fill
        
        # Add percentage column
        ws['C5'] = "Percentage"
        ws['C5'].font = header_font
        ws['C5'].fill = header_fill
        
        # Calculate total tasks for percentage
        total_tasks = sum(item['How_Many_Tasks'] for item in region_data) if region_data else 0
        
        # Data rows
        for row, item in enumerate(region_data, start=6):
            ws[f'A{row}'] = item['REGION']
            ws[f'B{row}'] = item['How_Many_Tasks']
            percentage = (item['How_Many_Tasks'] / total_tasks * 100) if total_tasks > 0 else 0
            ws[f'C{row}'] = f"{percentage:.1f}%"
        
        # Create embedded chart
        if len(region_data) > 0:
            chart = BarChart()
            chart.title = "Tasks by Region"
            chart.x_axis.title = "Region"
            chart.y_axis.title = "Number of Tasks"
            chart.height = 15  # Adjust chart height
            chart.width = 20   # Adjust chart width
            
            data_ref = Reference(ws, min_col=2, min_row=5, max_row=len(region_data)+5)
            categories_ref = Reference(ws, min_col=1, min_row=6, max_row=len(region_data)+5)
            
            chart.add_data(data_ref, titles_from_data=True)
            chart.set_categories(categories_ref)
            
            # Position chart to the right of the data
            ws.add_chart(chart, "E5")
        
        # Auto-adjust column widths
        self._adjust_column_widths(ws)
    
    def _adjust_column_widths(self, ws):
        """Auto-adjust column widths for better readability"""
        for column in ws.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            ws.column_dimensions[column_letter].width = adjusted_width

# Legacy function for backward compatibility
def generate_excel_report(task_data: list, region_data: list, filename: str) -> str:
    """Legacy function wrapper for simplified report generation"""
    generator = ReportGenerator()
    return generator.generate_excel_report(task_data, region_data, filename)