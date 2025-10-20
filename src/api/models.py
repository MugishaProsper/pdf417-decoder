"""Pydantic models for API requests and responses."""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class BarcodeResult(BaseModel):
    """Barcode decoding result."""
    data: str = Field(..., description="Decoded barcode data")
    type: str = Field(..., description="Barcode type (PDF417)")
    quality: int = Field(..., description="Detection quality score")
    preprocess_method: str = Field(..., description="Preprocessing method used")
    rect: Dict[str, int] = Field(..., description="Bounding rectangle")
    polygon: List[Dict[str, int]] = Field(..., description="Polygon points")


class DecodeResponse(BaseModel):
    """Response for decode endpoint."""
    success: bool = Field(..., description="Whether decoding was successful")
    count: int = Field(..., description="Number of barcodes found")
    results: List[BarcodeResult] = Field(..., description="Decoded barcodes")
    cache_hit: bool = Field(False, description="Whether result was from cache")
    filename: str = Field(..., description="Original filename")


class QualityMetric(BaseModel):
    """Quality metric details."""
    score: float = Field(..., description="Metric score (0-1)")
    status: str = Field(..., description="Status description")
    message: str = Field(..., description="Human-readable message")


class QualityAnalysisResponse(BaseModel):
    """Response for quality analysis endpoint."""
    success: bool = Field(..., description="Whether analysis was successful")
    filename: str = Field(..., description="Original filename")
    overall_score: float = Field(..., description="Overall quality score (0-1)")
    overall_quality: str = Field(..., description="Overall quality rating")
    resolution: Dict[str, Any] = Field(..., description="Resolution analysis")
    contrast: Dict[str, Any] = Field(..., description="Contrast analysis")
    sharpness: Dict[str, Any] = Field(..., description="Sharpness analysis")
    noise: Dict[str, Any] = Field(..., description="Noise analysis")
    brightness: Dict[str, Any] = Field(..., description="Brightness analysis")
    issues: List[str] = Field(..., description="Detected issues")
    recommendations: List[str] = Field(..., description="Recommendations")


class HealthResponse(BaseModel):
    """Response for health check endpoint."""
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")
    cache_enabled: bool = Field(..., description="Whether caching is enabled")


class CacheStatsResponse(BaseModel):
    """Response for cache stats endpoint."""
    success: bool = Field(..., description="Whether request was successful")
    total_entries: int = Field(..., description="Total cache entries")
    valid_entries: int = Field(..., description="Valid cache entries")
    expired_entries: int = Field(..., description="Expired cache entries")
    total_size_bytes: int = Field(..., description="Total cache size in bytes")
    total_size_mb: float = Field(..., description="Total cache size in MB")


class ErrorResponse(BaseModel):
    """Error response."""
    detail: str = Field(..., description="Error message")
