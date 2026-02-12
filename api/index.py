from fastapi import FastAPI
from fastapi.responses import JSONResponse
import traceback
import sys
import os

# Initialize as None
app = None

try:
    # Attempt to load the main app
    from app.main import app as main_app
    app = main_app
except Exception as e:
    # Fallback to diagnostic app if main app fails
    diagnostic_app = FastAPI(title="EduNexia Diagnostic")
    error_msg = str(e)
    tb_msg = traceback.format_exc()

    @diagnostic_app.get("/api/v1/health")
    def health_check():
        return JSONResponse({
            "status": "error",
            "message": "Main app failed to load",
            "error": error_msg,
            "traceback": tb_msg,
            "python_version": sys.version,
            "cwd": os.getcwd(),
            "path": sys.path
        })
    
    @diagnostic_app.get("/api/v1")
    def root_check():
        return health_check()

    @diagnostic_app.get("/{full_path:path}")
    def catch_all(full_path: str):
        return health_check()

    app = diagnostic_app
