"""FastAPI server for PDF417 barcode decoding."""

import os
import tempfile
from pathlib import Path
from typing import Optional, List
import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException, Query, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from ..decoder import decode_pdf417_from_image
from ..quality_analyzer import analyze_image_quality
from ..cache import get_cache
from ..logger import setup_logger, get_logger
from .models import (
    DecodeResponse, BarcodeResult, QualityAnalysisResponse,
    HealthResponse, CacheStatsResponse, ErrorResponse
)

# Setup logging
setup_logger(level="INFO", console=True)
logger = get_logger(__name__)

# Create FastAPI app
app = FastAPI(
    title="PDF417 Decoder API",
    description="REST API for decoding PDF417 barcodes from images",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize cache
cache = get_cache()


def cleanup_temp_file(file_path: str):
    """Clean up temporary file."""
    try:
        if os.path.exists(file_path):
            os.unlink(file_path)
            logger.debug(f"Cleaned up temp file: {file_path}")
    except Exception as e:
        logger.warning(f"Error cleaning up temp file {file_path}: {e}")


@app.get("/", response_model=dict)
async def root():
    """Root endpoint."""
    return {
        "message": "PDF417 Decoder API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        cache_enabled=True
    )


@app.post("/decode", response_model=DecodeResponse)
async def decode_barcode(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    use_cache: bool = Query(True, description="Use caching"),
    show_preview: bool = Query(False, description="Show preview (not supported in API)")
):
    """
    Decode PDF417 barcode from uploaded image.
    
    Args:
        file: Image file to decode
        use_cache: Whether to use caching
        show_preview: Show preview (not supported in API mode)
        
    Returns:
        Decoded barcode results
    """
    temp_file = None
    
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type: {file.content_type}. Must be an image."
            )
        
        # Save uploaded file to temp location
        suffix = Path(file.filename).suffix
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            content = await file.read()
            tmp.write(content)
            temp_file = tmp.name
        
        logger.info(f"Processing uploaded file: {file.filename}")
        
        # Check cache first
        results = None
        cache_hit = False
        
        if use_cache:
            results = cache.get(temp_file)
            if results:
                cache_hit = True
                logger.info("Cache hit for uploaded file")
        
        # Decode if not cached
        if results is None:
            results = decode_pdf417_from_image(temp_file, show_preview=False)
            
            # Cache results
            if use_cache and results:
                cache.set(temp_file, results)
        
        # Convert results to response model
        barcode_results = []
        for result in results:
            barcode_results.append(BarcodeResult(
                data=result['data'],
                type=str(result['type']),
                quality=result['quality'],
                preprocess_method=result['preprocess_method'],
                rect={
                    'left': result['rect'].left,
                    'top': result['rect'].top,
                    'width': result['rect'].width,
                    'height': result['rect'].height
                },
                polygon=[{'x': p.x, 'y': p.y} for p in result['polygon']]
            ))
        
        # Schedule cleanup
        background_tasks.add_task(cleanup_temp_file, temp_file)
        
        return DecodeResponse(
            success=True,
            count=len(barcode_results),
            results=barcode_results,
            cache_hit=cache_hit,
            filename=file.filename
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error decoding barcode: {e}", exc_info=True)
        
        # Cleanup on error
        if temp_file:
            background_tasks.add_task(cleanup_temp_file, temp_file)
        
        raise HTTPException(
            status_code=500,
            detail=f"Error processing image: {str(e)}"
        )


@app.post("/analyze", response_model=QualityAnalysisResponse)
async def analyze_quality(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    """
    Analyze image quality for barcode detection.
    
    Args:
        file: Image file to analyze
        
    Returns:
        Quality analysis results
    """
    temp_file = None
    
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type: {file.content_type}. Must be an image."
            )
        
        # Save uploaded file to temp location
        suffix = Path(file.filename).suffix
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            content = await file.read()
            tmp.write(content)
            temp_file = tmp.name
        
        logger.info(f"Analyzing quality of: {file.filename}")
        
        # Analyze quality
        analysis = analyze_image_quality(temp_file)
        
        # Schedule cleanup
        background_tasks.add_task(cleanup_temp_file, temp_file)
        
        return QualityAnalysisResponse(
            success=True,
            filename=file.filename,
            overall_score=analysis['overall_score'],
            overall_quality=analysis['overall_quality'],
            resolution=analysis['resolution'],
            contrast=analysis['contrast'],
            sharpness=analysis['sharpness'],
            noise=analysis['noise'],
            brightness=analysis['brightness'],
            issues=analysis['issues'],
            recommendations=analysis['recommendations']
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing quality: {e}", exc_info=True)
        
        # Cleanup on error
        if temp_file:
            background_tasks.add_task(cleanup_temp_file, temp_file)
        
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing image: {str(e)}"
        )


@app.get("/cache/stats", response_model=CacheStatsResponse)
async def get_cache_stats():
    """Get cache statistics."""
    try:
        stats = cache.get_stats()
        return CacheStatsResponse(
            success=True,
            **stats
        )
    except Exception as e:
        logger.error(f"Error getting cache stats: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error getting cache stats: {str(e)}"
        )


@app.delete("/cache")
async def clear_cache():
    """Clear all cache entries."""
    try:
        count = cache.clear()
        return {
            "success": True,
            "message": f"Cleared {count} cache entries"
        }
    except Exception as e:
        logger.error(f"Error clearing cache: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error clearing cache: {str(e)}"
        )


def start_server(host: str = "0.0.0.0", port: int = 8000, reload: bool = False):
    """
    Start the FastAPI server.
    
    Args:
        host: Host to bind to
        port: Port to bind to
        reload: Enable auto-reload for development
    """
    logger.info(f"Starting PDF417 Decoder API server on {host}:{port}")
    uvicorn.run(
        "src.api.server:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )


if __name__ == "__main__":
    start_server(reload=True)
