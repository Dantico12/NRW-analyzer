import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Tuple, Any
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json
import plotly

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ExcelProcessor:
    def __init__(self):
        self.df = None
        
    def process_excel(self, file_path: str) -> Tuple[List[Dict], List[Dict], Dict]:
        """
        Process Excel file and return simplified data for task assignments and regions only
        """
        try:
            # Load the Excel file
            logger.info(f"Loading Excel file: {file_path}")
            self.df = pd.read_excel(file_path)
            logger.info(f"Loaded {len(self.df)} rows and {len(self.df.columns)} columns")
            
            # Clean the data
            self.df = self._clean_data()
            
            # Process only task assignment and region data
            task_data = self._process_task_assignment_data()
            region_data = self._process_region_data()
            
            # Generate charts
            charts = self._generate_charts(task_data, region_data)
            
            return task_data, region_data, charts
            
        except Exception as e:
            logger.error(f"Error processing Excel file: {str(e)}")
            raise Exception(f"Failed to process Excel file: {str(e)}")
    
    def _clean_data(self) -> pd.DataFrame:
        """Clean and prepare the data - simplified version"""
        df = self.df.copy()
        
        # Replace missing values
        df = df.replace(-9, np.nan)
        df = df.replace('', np.nan)
        
        # Clean column names
        df.columns = df.columns.str.strip()
        
        # Look for task assignment and region columns
        region_col = None
        task_col = None
        
        # Find region column
        for col in df.columns:
            if 'region' in col.lower():
                region_col = col
                break
        
        # Find task assignment column (focusing on general task assignments)
        for col in df.columns:
            if 'task' in col.lower() and 'assign' in col.lower() and 'general' not in col.lower():
                # Skip specific task columns, focus on general task assignment
                if any(specific in col.lower() for specific in ['meter servicing', 'relocation', 'replacement']):
                    continue
                task_col = col
                break
        
        if not region_col:
            raise ValueError("No region column found. Please ensure your Excel file has a 'REGION' column.")
        
        if not task_col:
            raise ValueError("No task assignment column found. Please ensure your Excel file has a 'TASK ASSIGNED' column.")
        
        # Standardize column names
        df['REGION'] = df[region_col]
        df['TASK_ASSIGNED'] = df[task_col]
        
        # Remove rows with missing critical data
        df = df.dropna(subset=['REGION', 'TASK_ASSIGNED'])
        
        logger.info(f"Cleaned data: {len(df)} rows remaining")
        return df
    
    def _process_task_assignment_data(self) -> List[Dict]:
        """Process task assignment data - simplified to focus on general tasks"""
        try:
            # Count task assignments
            task_counts = (
                self.df['TASK_ASSIGNED']
                .value_counts()
                .reset_index()
            )
            task_counts.columns = ['Task_Assignment', 'How_Many']
            
            # Sort by count descending
            task_counts = task_counts.sort_values('How_Many', ascending=False)
            
            logger.info(f"Processed {len(task_counts)} task types")
            return task_counts.to_dict('records')
            
        except Exception as e:
            logger.error(f"Error processing task data: {str(e)}")
            return []
    
    def _process_region_data(self) -> List[Dict]:
        """Process region-wise task count data"""
        try:
            # Group by region and count tasks
            region_summary = (
                self.df.groupby('REGION', observed=True)
                .agg({
                    'TASK_ASSIGNED': 'count',
                })
                .reset_index()
                .rename(columns={'TASK_ASSIGNED': 'How_Many_Tasks'})
            )
            
            # Sort by total tasks descending
            region_summary = region_summary.sort_values('How_Many_Tasks', ascending=False)
            
            logger.info(f"Processed {len(region_summary)} regions")
            return region_summary.to_dict('records')
            
        except Exception as e:
            logger.error(f"Error processing region data: {str(e)}")
            return []
    
    def _generate_charts(self, task_data: List[Dict], region_data: List[Dict]) -> Dict:
        """Generate simplified charts for task assignments and regions"""
        charts = {}
        
        try:
            # Task Assignment Bar Chart
            if task_data:
                tasks = [item['Task_Assignment'] for item in task_data[:10]]  # Top 10
                counts = [item['How_Many'] for item in task_data[:10]]
                
                fig_tasks = px.bar(
                    x=counts,
                    y=tasks,
                    orientation='h',
                    title="Task Assignment Distribution",
                    labels={'x': 'Number of Tasks', 'y': 'Task Type'}
                )
                fig_tasks.update_layout(
                    height=500,
                    showlegend=False,
                    title_font_size=16,
                    margin=dict(l=150)  # More space for task names
                )
                charts['task_assignment_bar'] = json.dumps(fig_tasks, cls=plotly.utils.PlotlyJSONEncoder)
                
                # Task Assignment Pie Chart
                fig_tasks_pie = px.pie(
                    values=counts,
                    names=tasks,
                    title="Task Assignment Distribution (Pie Chart)"
                )
                fig_tasks_pie.update_layout(height=500)
                charts['task_assignment_pie'] = json.dumps(fig_tasks_pie, cls=plotly.utils.PlotlyJSONEncoder)
            
            # Region Analysis Bar Chart
            if region_data:
                regions = [item['REGION'] for item in region_data]
                region_counts = [item['How_Many_Tasks'] for item in region_data]
                
                fig_regions = px.bar(
                    x=regions,
                    y=region_counts,
                    title="Tasks by Region",
                    labels={'x': 'Region', 'y': 'Number of Tasks'}
                )
                fig_regions.update_layout(
                    height=400,
                    showlegend=False,
                    title_font_size=16
                )
                charts['region_bar'] = json.dumps(fig_regions, cls=plotly.utils.PlotlyJSONEncoder)
                
                # Region Pie Chart
                fig_regions_pie = px.pie(
                    values=region_counts,
                    names=regions,
                    title="Regional Task Distribution"
                )
                fig_regions_pie.update_layout(height=400)
                charts['region_pie'] = json.dumps(fig_regions_pie, cls=plotly.utils.PlotlyJSONEncoder)
                
        except Exception as e:
            logger.error(f"Error generating charts: {str(e)}")
        
        return charts

# Legacy function for backward compatibility
def process_excel(file_path: str):
    """Legacy function wrapper"""
    processor = ExcelProcessor()
    task_data, region_data, charts = processor.process_excel(file_path)
    return task_data, region_data