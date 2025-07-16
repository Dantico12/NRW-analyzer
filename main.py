from fastapi import FastAPI, UploadFile, File, Request, HTTPException, BackgroundTasks
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, FileResponse, JSONResponse
from utils.file_processor import ExcelProcessor
from utils.report_generator import ReportGenerator
import os
import uuid
import logging
from typing import Dict, Any
import json
from datetime import datetime
import asyncio
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Excel Data Analyzer",
    description="Analyze Excel data with region and task breakdowns",
    version="2.0.0"
)

# Mount static files - this serves CSS, JS, and other static assets
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Create necessary directories
UPLOAD_DIR = "uploads"
REPORTS_DIR = "reports"
for directory in [UPLOAD_DIR, REPORTS_DIR]:
    os.makedirs(directory, exist_ok=True)

# Initialize processors
excel_processor = ExcelProcessor()
report_generator = ReportGenerator()

# In-memory storage for processed data (consider using Redis in production)
processed_data: Dict[str, Dict[str, Any]] = {}

@app.get("/")
async def home(request: Request):
    """Home page with file upload form"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload")
async def upload_file(request: Request, file: UploadFile = File(...)):
    """Handle file upload and processing"""
    try:
        # Validate file type
        if not file.filename.endswith(('.xlsx', '.xls')):
            raise HTTPException(
                status_code=400, 
                detail="Invalid file type. Please upload Excel files (.xlsx, .xls) only."
            )
        
        # Check file size (limit to 10MB)
        file_content = await file.read()
        if len(file_content) > 10 * 1024 * 1024:  # 10MB
            raise HTTPException(
                status_code=400,
                detail="File size too large. Maximum file size is 10MB."
            )
        
        # Save uploaded file
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            f.write(file_content)
        
        logger.info(f"File uploaded: {file.filename}")
        
        # Process data
        try:
            region_data, task_data, service_data, charts = excel_processor.process_excel(file_path)
        except Exception as e:
            logger.error(f"Error processing file: {str(e)}")
            raise HTTPException(
                status_code=400,
                detail=f"Error processing Excel file: {str(e)}"
            )
        
        # Generate unique token for this session
        token = str(uuid.uuid4())
        
        # Store processed data
        processed_data[token] = {
            "region_data": region_data,
            "task_data": task_data,
            "service_data": service_data,
            "charts": charts,
            "filename": file.filename,
            "upload_time": datetime.now().isoformat(),
            "file_path": file_path
        }
        
        logger.info(f"Data processed successfully for token: {token}")
        
        # Clean up old uploaded file
        try:
            os.remove(file_path)
        except:
            pass
        
        return RedirectResponse(url=f"/preview?token={token}", status_code=303)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in upload: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error during file upload")

@app.get("/preview")
async def preview_data(request: Request, token: str):
    """Preview processed data with charts"""
    data = processed_data.get(token)
    if not data:
        return RedirectResponse("/", status_code=303)
    
    try:
        return templates.TemplateResponse("preview.html", {
            "request": request,
            "token": token,
            "region_data": data["region_data"],
            "task_data": data["task_data"],
            "service_data": data["service_data"],
            "charts": data["charts"],
            "filename": data["filename"],
            "upload_time": data["upload_time"]
        })
    except Exception as e:
        logger.error(f"Error in preview: {str(e)}")
        raise HTTPException(status_code=500, detail="Error displaying preview")

@app.get("/api/data/{token}")
async def get_data_api(token: str):
    """API endpoint to get processed data as JSON"""
    data = processed_data.get(token)
    if not data:
        raise HTTPException(status_code=404, detail="Data not found")
    
    return JSONResponse({
        "region_data": data["region_data"],
        "task_data": data["task_data"],
        "service_data": data["service_data"],
        "filename": data["filename"],
        "upload_time": data["upload_time"]
    })

@app.get("/download/excel/{token}")
async def download_excel_report(token: str):
    """Download Excel report with charts"""
    data = processed_data.get(token)
    if not data:
        raise HTTPException(status_code=404, detail="Data not found")
    
    try:
        # Generate Excel report
        report_path = report_generator.generate_excel_report(
            data["region_data"],
            data["task_data"],
            data["service_data"],
            data["filename"]
        )
        
        # Get filename for download
        filename = os.path.basename(report_path)
        
        return FileResponse(
            path=report_path,
            filename=filename,
            media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        
    except Exception as e:
        logger.error(f"Error generating Excel report: {str(e)}")
        raise HTTPException(status_code=500, detail="Error generating Excel report")

@app.get("/download/charts/{token}")
async def download_charts_data(token: str):
    """Download charts data as JSON"""
    data = processed_data.get(token)
    if not data:
        raise HTTPException(status_code=404, detail="Data not found")
    
    return JSONResponse({
        "charts": data["charts"],
        "filename": data["filename"]
    })

@app.post("/regenerate/{token}")
async def regenerate_report(token: str):
    """Regenerate report for existing data"""
    data = processed_data.get(token)
    if not data:
        raise HTTPException(status_code=404, detail="Data not found")
    
    try:
        # Generate new report
        report_path = report_generator.generate_excel_report(
            data["region_data"],
            data["task_data"],
            data["service_data"],
            data["filename"]
        )
        
        return JSONResponse({
            "message": "Report regenerated successfully",
            "download_url": f"/download/excel/{token}"
        })
        
    except Exception as e:
        logger.error(f"Error regenerating report: {str(e)}")
        raise HTTPException(status_code=500, detail="Error regenerating report")

@app.delete("/data/{token}")
async def delete_data(token: str):
    """Delete processed data"""
    if token in processed_data:
        del processed_data[token]
        return JSONResponse({"message": "Data deleted successfully"})
    else:
        raise HTTPException(status_code=404, detail="Data not found")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return JSONResponse({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "active_sessions": len(processed_data)
    })

@app.get("/stats")
async def get_stats():
    """Get application statistics"""
    return JSONResponse({
        "total_sessions": len(processed_data),
        "upload_directory_size": sum(
            os.path.getsize(os.path.join(UPLOAD_DIR, f)) 
            for f in os.listdir(UPLOAD_DIR) 
            if os.path.isfile(os.path.join(UPLOAD_DIR, f))
        ) if os.path.exists(UPLOAD_DIR) else 0,
        "reports_directory_size": sum(
            os.path.getsize(os.path.join(REPORTS_DIR, f)) 
            for f in os.listdir(REPORTS_DIR) 
            if os.path.isfile(os.path.join(REPORTS_DIR, f))
        ) if os.path.exists(REPORTS_DIR) else 0
    })

# Additional endpoint to serve individual CSS/JS files if needed
@app.get("/css/{file_path:path}")
async def serve_css(file_path: str):
    """Serve CSS files with proper content type"""
    css_file_path = os.path.join("static", file_path)
    if os.path.exists(css_file_path) and file_path.endswith('.css'):
        return FileResponse(css_file_path, media_type="text/css")
    raise HTTPException(status_code=404, detail="CSS file not found")

@app.get("/js/{file_path:path}")
async def serve_js(file_path: str):
    """Serve JavaScript files with proper content type"""
    js_file_path = os.path.join("static", file_path)
    if os.path.exists(js_file_path) and file_path.endswith('.js'):
        return FileResponse(js_file_path, media_type="application/javascript")
    raise HTTPException(status_code=404, detail="JavaScript file not found")

async def cleanup_old_data():
    """Clean up old data periodically"""
    current_time = datetime.now()
    expired_tokens = []
    
    for token, data in processed_data.items():
        upload_time = datetime.fromisoformat(data["upload_time"])
        if (current_time - upload_time).total_seconds() > 3600:  # 1 hour
            expired_tokens.append(token)
    
    for token in expired_tokens:
        del processed_data[token]
    
    logger.info(f"Cleaned up {len(expired_tokens)} expired sessions")

@app.on_event("startup")
async def startup_event():
    """Application startup event"""
    logger.info("Excel Data Analyzer started")
    logger.info(f"Static files directory: {os.path.abspath('static')}")
    logger.info(f"Templates directory: {os.path.abspath('templates')}")
    
    # Check if static directory exists
    if not os.path.exists("static"):
        logger.warning("Static directory not found! Creating it...")
        os.makedirs("static", exist_ok=True)
    
    # Check if templates directory exists
    if not os.path.exists("templates"):
        logger.warning("Templates directory not found! Creating it...")
        os.makedirs("templates", exist_ok=True)
    
    # Schedule periodic cleanup
    asyncio.create_task(periodic_cleanup())

async def periodic_cleanup():
    """Periodic cleanup task"""
    while True:
        await asyncio.sleep(3600)  # Run every hour
        await cleanup_old_data()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000, 
        log_level="info",
        reload=True
    )