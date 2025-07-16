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
        self.region_data = None
        self.task_data = None
        self.service_data = None
        
    def process_excel(self, file_path: str) -> Tuple[List[Dict], List[Dict], List[Dict], Dict]:
        """
        Process Excel file and return structured data for regions, tasks, and services
        """
        try:
            # Load the Excel file
            logger.info(f"Loading Excel file: {file_path}")
            self.df = pd.read_excel(file_path)
            logger.info(f"Loaded {len(self.df)} rows and {len(self.df.columns)} columns")
            
            # Clean the data
            self.df = self._clean_data()
            
            # Process different data categories
            region_data = self._process_region_data()
            task_data = self._process_task_data()
            service_data = self._process_service_data()
            
            # Generate charts
            charts = self._generate_charts()
            
            return region_data, task_data, service_data, charts
            
        except Exception as e:
            logger.error(f"Error processing Excel file: {str(e)}")
            raise Exception(f"Failed to process Excel file: {str(e)}")
    
    def _clean_data(self) -> pd.DataFrame:
        """Clean and prepare the data"""
        df = self.df.copy()
        
        # Replace missing values and negative indicators
        df = df.replace(-9, np.nan)
        df = df.replace('', np.nan)
        
        # Clean column names
        df.columns = df.columns.str.strip()
        
        # Ensure we have the required columns
        required_columns = ['REGION', 'TASK ASSIGNED']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            # Try to find similar column names
            available_cols = df.columns.tolist()
            logger.warning(f"Missing columns: {missing_columns}")
            logger.info(f"Available columns: {available_cols}")
            
            # Try to map common variations
            column_mapping = {}
            for col in df.columns:
                if 'region' in col.lower():
                    column_mapping['REGION'] = col
                elif 'task' in col.lower() and 'assign' in col.lower():
                    column_mapping['TASK ASSIGNED'] = col
            
            # Apply mapping
            for standard_name, actual_name in column_mapping.items():
                if standard_name in missing_columns:
                    df[standard_name] = df[actual_name]
                    missing_columns.remove(standard_name)
            
            if missing_columns:
                raise ValueError(f"Required columns not found: {missing_columns}")
        
        # Remove rows with missing critical data
        df = df.dropna(subset=['REGION', 'TASK ASSIGNED'])
        
        logger.info(f"Cleaned data: {len(df)} rows remaining")
        return df
    
    def _process_region_data(self) -> List[Dict]:
        """Process region-wise data"""
        try:
            # Group by region and count tasks
            region_summary = (
                self.df.groupby('REGION', observed=True)
                .agg({
                    'TASK ASSIGNED': 'count',
                })
                .reset_index()
                .rename(columns={'TASK ASSIGNED': 'total_tasks'})
            )
            
            # Sort by total tasks descending
            region_summary = region_summary.sort_values('total_tasks', ascending=False)
            
            logger.info(f"Processed {len(region_summary)} regions")
            return region_summary.to_dict('records')
            
        except Exception as e:
            logger.error(f"Error processing region data: {str(e)}")
            return []
    
    def _process_task_data(self) -> List[Dict]:
        """Process task assignment data"""
        try:
            # Count task assignments
            task_counts = (
                self.df['TASK ASSIGNED']
                .value_counts()
                .reset_index()
            )
            task_counts.columns = ['Task', 'Count']
            
            # Sort by count descending
            task_counts = task_counts.sort_values('Count', ascending=False)
            
            logger.info(f"Processed {len(task_counts)} task types")
            return task_counts.to_dict('records')
            
        except Exception as e:
            logger.error(f"Error processing task data: {str(e)}")
            return []
    
    def _process_service_data(self) -> List[Dict]:
        """Process service-specific data (meter servicing, gate valve fixing, etc.)"""
        try:
            # Find service-related columns
            service_columns = [col for col in self.df.columns if any(
                keyword in col.lower() for keyword in 
                ['meter', 'valve', 'pipe', 'connection', 'repair', 'maintenance', 'service']
            )]
            
            if not service_columns:
                logger.warning("No service-related columns found")
                return []
            
            service_data = []
            
            for region in self.df['REGION'].unique():
                region_df = self.df[self.df['REGION'] == region]
                
                region_services = {'region': region, 'services': []}
                
                # Count different service types in this region
                for service_col in service_columns:
                    if service_col in region_df.columns:
                        service_count = region_df[service_col].notna().sum()
                        if service_count > 0:
                            region_services['services'].append({
                                'service_type': service_col,
                                'count': int(service_count)
                            })
                
                if region_services['services']:
                    service_data.append(region_services)
            
            logger.info(f"Processed service data for {len(service_data)} regions")
            return service_data
            
        except Exception as e:
            logger.error(f"Error processing service data: {str(e)}")
            return []
    
    def _generate_charts(self) -> Dict:
        """Generate charts for the data"""
        charts = {}
        
        try:
            # Region distribution chart
            if self.df is not None:
                region_counts = self.df['REGION'].value_counts()
                
                # Bar chart for regions
                fig_region = px.bar(
                    x=region_counts.index,
                    y=region_counts.values,
                    title="Task Distribution by Region",
                    labels={'x': 'Region', 'y': 'Number of Tasks'}
                )
                fig_region.update_layout(
                    height=400,
                    showlegend=False,
                    title_font_size=16
                )
                charts['region_bar'] = json.dumps(fig_region, cls=plotly.utils.PlotlyJSONEncoder)
                
                # Pie chart for regions
                fig_region_pie = px.pie(
                    values=region_counts.values,
                    names=region_counts.index,
                    title="Task Distribution by Region (Pie Chart)"
                )
                fig_region_pie.update_layout(height=400)
                charts['region_pie'] = json.dumps(fig_region_pie, cls=plotly.utils.PlotlyJSONEncoder)
                
                # Task assignment chart
                task_counts = self.df['TASK ASSIGNED'].value_counts().head(10)
                fig_tasks = px.bar(
                    x=task_counts.values,
                    y=task_counts.index,
                    orientation='h',
                    title="Top 10 Task Types",
                    labels={'x': 'Count', 'y': 'Task Type'}
                )
                fig_tasks.update_layout(
                    height=500,
                    showlegend=False,
                    title_font_size=16
                )
                charts['task_bar'] = json.dumps(fig_tasks, cls=plotly.utils.PlotlyJSONEncoder)
                
                # Combined region-task heatmap
                if len(self.df) > 0:
                    pivot_data = pd.crosstab(self.df['REGION'], self.df['TASK ASSIGNED'])
                    if not pivot_data.empty:
                        fig_heatmap = px.imshow(
                            pivot_data.values,
                            x=pivot_data.columns,
                            y=pivot_data.index,
                            title="Task Distribution Heatmap by Region",
                            aspect="auto"
                        )
                        fig_heatmap.update_layout(
                            height=600,
                            title_font_size=16
                        )
                        charts['heatmap'] = json.dumps(fig_heatmap, cls=plotly.utils.PlotlyJSONEncoder)
                
        except Exception as e:
            logger.error(f"Error generating charts: {str(e)}")
        
        return charts

# Legacy function for backward compatibility
def process_excel(file_path: str):
    """Legacy function wrapper"""
    processor = ExcelProcessor()
    region_data, task_data, service_data, charts = processor.process_excel(file_path)
    return region_data, task_data